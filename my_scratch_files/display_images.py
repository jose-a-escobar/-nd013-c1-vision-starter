import tensorflow.compat.v1 as tf
import numpy as np
import matplotlib
matplotlib.use('TkAgg') #Images cannot be displayed without this line
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def display_instances(batch):
    """
    This function takes a batch from the dataset and display the image with 
    the associated bounding boxes.
    """
    # ADD CODE HERE
    #Color mapping of classes
    colormap = {1:[1,0,0], 2:[0,1,0], 4:[0,0,1]}
    
    small_batch = batch.take(20)
    for sample in small_batch:        
        image = sample['image'].numpy()
        print(sample['filename'])
        
        #get the size of the image
        width, height, _ = tf.shape(sample['image']).numpy()
        
        #create figure and axes
        fig, ax = plt.subplots()
        ax.imshow(image)
        
        #Get groundtruth boxes and classes
        bboxes  = sample['groundtruth_boxes']
        classes = sample['groundtruth_classes']
        
        #Create rectangular patches for each of the boxes
        for cl, bb in zip(classes,bboxes):
            #Get rectangle coordinates
            y1, x1, y2, x2 = bb.numpy()
            #Correct reactangle coordinates
            # ** width and height are the current image size
            # ** 1920 and 1080 are the orginal image size (*.tfrecord) 
            #    and 79 is the offset in the y-direction
            y1 = y1 * height * (height/1080) - 79
            y2 = y2 * height * (height/1080) - 79
            x1 = x1 * width  * (width/1920)
            x2 = x2 * width  * (width/1920)
            #Create and add rectangles to the image
            rec = Rectangle((x1,y1), x2 - x1, y2 - y1, facecolor='none',
                           edgecolor=colormap[cl.numpy()])
            ax.add_patch(rec)
                
        plt.show()
