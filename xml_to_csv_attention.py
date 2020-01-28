""" This is xml to csv converter script to convert all xml files into 1 csv files for attention ocr training """
import xml.etree.ElementTree as ET
import ast
import csv
import json
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import xmltodict
import pdb

#TODO : Please change all '#' path into real path

def file_name(path):
    if not os.path.exists(path):
        raise FileNotFoundError("%s doesn't exists" % path)

    with open(path, 'r') as xml_file:
        xml_data = xml_file.read()
        ordered_dict_data = xmltodict.parse(xml_data)
        json_dict_data = json.dumps(ordered_dict_data)
        dict_data = ast.literal_eval(json_dict_data)

    annotation_filename = dict_data['annotation']['filename']

    if isinstance(annotation_filename, dict):
        annotation_objects = [annotation_filename]
    
    return annotation_filename


def get_plate_coordinates(path):
    if not os.path.exists(path):
        raise FileNotFoundError("%s doesn't exists" % path)

    with open(path, 'r') as xml_file:
        xml_data = xml_file.read()
        ordered_dict_data = xmltodict.parse(xml_data)
        json_dict_data = json.dumps(ordered_dict_data)
        dict_data = ast.literal_eval(json_dict_data)

    annotation_objects = dict_data['annotation']['object']

    if isinstance(annotation_objects, dict):
        annotation_objects = [annotation_objects]

    plate_bounding_boxes = []
    for obj in annotation_objects:
        if obj['name'] == "plate":
            plate_bounding_boxes.append(obj['bndbox'])

    return plate_bounding_boxes


def get_all_letters(path):
    if not os.path.exists(path):
        raise FileNotFoundError("%s doesn't exists" % path)

    with open(path, 'r') as xml_file:
        xml_data = xml_file.read()
        ordered_dict_data = xmltodict.parse(xml_data)
        json_dict_data = json.dumps(ordered_dict_data)
        dict_data = ast.literal_eval(json_dict_data)

    annotation_objects = dict_data['annotation']['object']

    if isinstance(annotation_objects, dict):
        annotation_objects = [annotation_objects]
    n = len(annotation_objects)
    list_name = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X'
        , 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-']
    l = []
    for i in range(n):
        if annotation_objects[i]['name'] in list_name:
            l.append([annotation_objects[i]['name'], annotation_objects[i]['bndbox']])
    return l


def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo
    return sub_li


def number_of_plate(path):
    l = get_plate_coordinates(path)
    no_of_plate = len(l)
    return no_of_plate


def return_string_plate(path):
    l = get_plate_coordinates(path)
    no_of_plate = len(l)
    list_of_strings = []
    for i in range(no_of_plate):
        x_min = int(l[i]['xmin']) - 20
        y_min = int(l[i]['ymin']) - 20
        x_max = int(l[i]['xmax']) + 20
        y_max = int(l[i]['ymax']) + 20
        a = get_all_letters(path)
        b = []
        no_of_letters = len(a)
        for j in range(no_of_letters):
            if (int(a[j][1]['xmin']) >= int(x_min)) and (int(a[j][1]['xmax']) <= int(x_max)) and (
                    int(a[j][1]['ymin']) >= int(y_min)) and (int(a[j][1]['ymax']) <= int(y_max)):
                b.append([a[j][0], int(a[j][1]['xmin'])])
        a = Sort(b)
        empty_string = []
        for q in range(len(a)):
            empty_string.append(a[q][0])

        list_of_strings.append("".join(empty_string))
    return list_of_strings


def get_plate_final(path):
    if not os.path.exists(path):
        raise FileNotFoundError("%s doesn't exists" % path)

    with open(path, 'r') as xml_file:
        xml_data = xml_file.read()
        ordered_dict_data = xmltodict.parse(xml_data)
        json_dict_data = json.dumps(ordered_dict_data)
        dict_data = ast.literal_eval(json_dict_data)

    annotation_objects = dict_data['annotation']['object']

    if isinstance(annotation_objects, dict):
        annotation_objects = [annotation_objects]
    num_plates = number_of_plate(path)
    l_k = []
    for i in range(num_plates):
        try:
        	list = get_plate_coordinates(path)
        	xmin = list[i]['xmin']
        	ymin = list[i]['ymin']
        	xmax = list[i]['xmax']
        	ymax = list[i]['ymax']
        	file_name_ = file_name(path)
        	list_of_strings = return_string_plate(path)
        	a = list_of_strings[i]
        	l_k.append([file_name_, a, xmin, ymin, xmax, ymax])
        except KeyError:
        	continue
    return l_k



def main():
    list_l = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X'
        , 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-']
    lk = [['files', 'text', 'xmin', 'ymin', 'xmax', 'ymax']]
    image_path = "# Please put images processed path"
    print(image_path)
    #Print total number of files here
    i=0
    #start a counter from 0 and print it so we know which file we are currently processing
    for filename in os.listdir(image_path):
        try:
        	print(filename)
       #counter starts 
        	if not filename.endswith('.xml'): continue
        	fullname = os.path.join(image_path, filename)
        	a = get_plate_final(fullname)
        	while (len(a)!= 0):
            		lk.append(a.pop())
        	with open('#Please put saving path / #ALSOCSVNAME.csv','w', newline='') as fp: 
            		a = csv.writer(fp, delimiter=',')
            		a.writerows(lk)
        	i=i+1
        	print(i)
        except KeyError:
        	continue
    print('Successfully converted to csv from xml')

main()
