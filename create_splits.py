import argparse
import glob
import os
import random

import numpy as np

from utils import get_module_logger


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the 
    same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /home/workspace/data/waymo
    """
    
    # TODO: Split the data present in `/home/workspace/data/waymo/training_and_validation` into train and val sets.
    # You should move the files rather than copy because of space limitations in the workspace.
    
    data_loc = "/home/workspace/data/waymo/training_and_validation" #file location
    #The data contained in the text files is located in the directory named my_scratch_files
    #The procedure to split trips is explained in the project report
    data_splits={"test":"my_scratch_files/test_split.txt","val":"my_scratch_files/validation_split.txt",
                "train":"my_scratch_files/training_split.txt"}
                
    #Function to read file data
    def read_data(file_loc):
        file1 = open('%s' %file_loc, 'r')
        lines = file1.readlines()
        trip_name = []
        for line in lines:
           if not line.startswith("#"):
              line_info = line.split('\t')
              trip_name.append(line_info[1].strip())
        trip_name = [x for x in trip_name if x] #Remove any empty list elements    
        return trip_name
    
    #Main funtion; read trips, create trip folder, moves files to trip folder
    for i_split in data_splits:
        print("Moving files to split: {}".format(i_split))
        #Read trips
        trips = [] #Clear array
        trips = read_data(data_splits[i_split]) #Trip data
        #Creates destination folder
        split_folder = "%s/%s" %(data_dir,i_split)
        os.mkdir(split_folder)
        #Moves files from original location to final destination
        for i_trip in trips:
            file_org  = "%s/%s" %(data_loc,i_trip)
            file_dest = "%s/%s" %(split_folder,i_trip)
            #print("file_org : {}".format(file_org))
            #print("file_dest: {}".format(file_dest))
            #shutil.move(file_org,file_dest)
            os.symlink(file_org,file_dest)
    
    
    

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--data_dir', required=True,
                        help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)