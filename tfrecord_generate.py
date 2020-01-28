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

def encoded_utf8_string(text, length, dic, null_char_id=5462):
    """
    Encode the string and also take care of null characters
    """
    char_ids_padded         = [null_char_id] * length
    char_ids_unpadded       = [null_char_id] * length(text)
    for i in range(len(text)):
        hash_id             = dic[text[i]]
        char_ids_padded[i]  = hash_id
        char_ids_unpadded[i]= hash_id

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