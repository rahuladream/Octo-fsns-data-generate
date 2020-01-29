"""
This code is forked from Attention chinease ocr
"""

import datasets.fsns as fsns

DEFAULT_DATASET_DIR = 'data/*/*'

DEFAULT_CONFIG = {
    'name':
        'MYDATASET',
    'splits': {
        'train': {
            'size': 8,
            'pattern': 'tfexample_train*'
        },
        'test': {
            'size': 2,
            'pattern': 'tfexample_test*'
        }
    },
    'charset_filename':
        'dict_classes.txt',
    'image_shape': (150, 600, 3),
    'num_of_views':
        1,
    'max_sequence_length':
        37,
    'null_code':
        64,
    'items_to_descriptions': {
        'image':
            'A [150 x 600 x 3] color image.',
        'label':
            'Characters codes.',
        'text':
            'A unicode string.',
        'length':
            'A length of the encoded text.',
        'num_of_views':
            'A number of different views stored within the image.'
    }
}


def get_split(split_name, dataset_dir=None, config=None):
  if not dataset_dir:
    dataset_dir = DEFAULT_DATASET_DIR
  if not config:
    config = DEFAULT_CONFIG

  return fsns.get_split(split_name, dataset_dir, config)