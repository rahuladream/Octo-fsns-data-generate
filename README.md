# Octo-fsns-data-generate
Generating the dataset for fsns (attention ocr) Deep Networks, End-to-end Networks, Image Dataset, Multiview Dataset

Google officials did not say in this part carefully, only to a stackoverflow link, but This link is also not clear,and have some mistakes, so I wrote a code to generate FSNS format (JPG / PNG) tfrecord .

## about FSNS

FSNS dataset is a set of signs, from the streets of France, that bear street names. Some example images are shown in Figure 1. Each image carries four tiles of 150 × 150 pixels laid out horizontally, each of which contains a pre-detected street name sign, or random noise in the case that less than four independent views are available of the same physical sign
