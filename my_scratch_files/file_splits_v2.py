import os
from glob import glob
import numpy as np
import tensorflow.compat.v1 as tf
from waymo_open_dataset import dataset_pb2 as open_dataset
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') #Images cannot be displayed without this line
from utils import get_dataset

def show_camera_image(camera_image):
    plt.imshow(tf.image.decode_jpeg(camera_image.image))
    plt.title(open_dataset.CameraName.Name.Name(camera_image.name))
    plt.show()

filenames = glob(os.path.join("/data/waymo/", 'segment*.tfrecord'))

#check for unique trips
trips = []
for file in filenames:
    trips.append(file.split('/')[-1])

#plt.figure(figsize=(25, 20))
trips_sort = sorted(trips)
i_glob  = 0

#Open File Identifier
f = open("trip_description.txt","w")
f.write("#**filenumber**\t**file_name**\t**Object Density**\t**Light**\t**Weather**\n")
f.write("#Key:: Object Density = Low (Suburb/Highway), High (City)\n")
f.write("#Key:: Light = Night, Day\n")
f.write("#Key:: Weather = Bad (Rain/Adverse), Fair\n")

list_questions=["Object Density. Options = Low (Suburb/Highway), High (City):: ",
               "Light. Options = Night, Day:: ",
               "Weather. Options = Bad (Rain/Adverse), Fair:: "]

for check in trips_sort:
    user_input = [""] * 4
    frames_path = "/data/waymo/"+check
    print(check)
    dataset = get_dataset(frames_path)
    i_image = 0
    
    for data in dataset:
        #print(data['image'])
        image = data['image'].numpy()
        image_name = data['filename'].numpy()
        print(image_name)
        plt.imshow(image)
        plt.title(image_name,fontsize=10)
        file_name=str(i_glob).zfill(3)+".png"
        user_input[0] = check
        
        for ii in range(len(user_input)-1):
            plt.savefig(file_name)
            print("current image file name = %s" %file_name)
            text_input = input("%s" %list_questions[ii])
            user_input[ii+1] = text_input.lower() #Make it lower case
        
        f.write("%d\t%s\t%s\t%s\t%s\n" %(i_glob,user_input[0],user_input[1],user_input[2],user_input[3],))
        f.flush() #Write immediately
        i_image +=1
        i_glob +=1
        if i_image > 0:
           break
f.close()