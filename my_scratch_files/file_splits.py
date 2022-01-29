import os
from glob import glob
import numpy as np
import tensorflow.compat.v1 as tf
from waymo_open_dataset import dataset_pb2 as open_dataset
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') #Images cannot be displayed without this line

def show_camera_image(camera_image):
    plt.imshow(tf.image.decode_jpeg(camera_image.image))
    plt.title(open_dataset.CameraName.Name.Name(camera_image.name))
    plt.show()

#filenames = print(glob.glob("/data/waymo/*.tfrecord"))
filenames = glob(os.path.join("/data/waymo/", '*.tfrecord'))

#check for unique trips
trips = []
for file in filenames:
    trips.append(file.split('/')[-1])

plt.figure(figsize=(25, 20))
trips_sort = sorted(trips)
for check in trips_sort:
    frames_path = "/data/waymo/"+check
    print(check)
    dataset = tf.data.TFRecordDataset(frames_path, compression_type='')
    i_image = 0
      
    for data in dataset:
        frame = open_dataset.Frame()
        print(data)
        frame.ParseFromString(bytearray(data.numpy()))
        print(len(frame.images))
        for image in frame.images:
    #        #print(image.camera_labels)
            show_camera_image(image)
            i_image +=1
            print(i_image)
        if i_image > len(frame.images):
           break
            
            
            
            
    #print(check)
    #plt.imshow(tf.image.decode_jpeg(dataset))
    #plt.show()

#unique_trips = np.unique(trips)
#print(len(trips))
#print(len(unique_trips))
    
# Using readlines()
#file1 = open('filenames.txt', 'r')
#Lines = file1.readlines()

#print(len(Lines))
#for line in Lines:
#    filename = line.split('/')[-1]
    #print(filename)
