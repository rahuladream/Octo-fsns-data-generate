from random import shuffle
import numpy as np
import glob
import tensorflow as tf
import os,cv2,sys
import PIL.Image as Image

"""
Main moto to convert tf_convert from fsns record file
"""

dictionary_path = 'dict_classes.txt'
image_path      = 'data/*/*.jpg'
label_path      = 'data/*/*.txt'


def encode_utf8_string(text, length, dic, null_char_id=5462):
    """
    Encode the string and also take care of null characters
    """
    char_ids_padded            = [null_char_id]*length
    char_ids_unpadded          = [null_char_id]*len(text)
    for i in range(len(text)):
        hash_id              = dic[text[i]]
        char_ids_padded[i]   = hash_id
        char_ids_unpadded[i] = hash_id

    return char_ids_padded, char_ids_unpadded


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

dict_values = {}
with open(dictionary_path, encoding="utf8") as dict_file:
    for line in dict_file:
        (key, value) = line.strip.split('\t')
        dict_values[value] = int(key)
print(dict_values)

addrs_image = glob.glob(image_path)
addrs_label = glob.glob(label_path)
print(" address image len {} , address label len {}".format(len(addrs_image), len(addrs_label)))

tfrecord_writer  = tf.python_io.TFRecordWriter("tfexample_train") 

for j in range(0,int(len(addrs_image))):
    print('Train data: {}/{}'.format(j,int(len(addrs_image))))
    sys.stdout.flush()

    img             = Image.open(addrs_image[j])
    img             = img.resize((600, 150), Image.ANTIALIAS)
    np_data         = np.array(img)
    image_data      = img.tobytes()
    for text in open(addrs_label[j], encoding="utf"):
                 char_ids_padded, char_ids_unpadded = encode_utf8_string(
                            text=text,
                            dic=dict,
                            length=37,
                            null_char_id=5462)



    example = tf.train.Example(features=tf.train.Features(
                        feature={
                            'image/encoded'       : _bytes_feature(image_data),
                            'image/format'        : _bytes_feature(b"raw"),
                            'image/width'         : _int64_feature([np_data.shape[1]]),
                            'image/orig_width'    : _int64_feature([np_data.shape[1]]),
                            'image/class'         : _int64_feature(char_ids_padded),
                            'image/unpadded_class': _int64_feature(char_ids_unpadded),
                            'image/text'          : _bytes_feature(bytes(text, 'utf-8')),
                        }
                    ))
    tfrecord_writer.write(example.SerializeToString())
tfrecord_writer.close()

sys.stdout.flush()








