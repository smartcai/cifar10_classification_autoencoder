# -*- coding: utf-8 -*-
"""dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IL8fWAgyI0k9Mz_2qmcOqi1LeOw28yBZ
"""

import random 
import numpy as np
import matplotlib.pyplot as plt
import skimage as sk

from keras.datasets import cifar10
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

def load_data(val_size, remove_classes=[], fraction=0.5, random_state=42):
    '''Returns train, validation and rest splits with respective one-hot encoded 
    target classifications and unique class names in cifar10


    Parameters:

    val_size(float): validation size as a fraction of train+val size

    remove_classes(list): list of classes whose samples to remove from train+val

    fraction (float): fraction of samples of classes in remove_classes to remove
    from train+val with respect of the size of each class in the dataset

    random_state(defaults to 42): random seed for train/val split


    Returns:

    x_train(4d array): training set 

    x_val(4d array): validation set

    x_test(4d array): test set

    y_train_ohe(2d array): one-hot encoded numpy array with classification 
    values for the training set x_train

    y_val_ohe(2d array): one-hot encoded numpy array with classification 
    values for the validation set x_val

    y_test_ohe(numpy array):  one-hot encoded numpy array with classification 
    values for the validation set x_test

    class_names(list): list with unique class names in cifar10

    '''
    (x_train_val, y_train_val), (x_test, y_test) = cifar10.load_data()
    class_names= load_class_names()

    x_train_val = x_train_val.astype('float32')
    x_test = x_test.astype('float32')

    samples_to_delete= [] 
    for c in remove_classes:
        samples= list(np.argwhere(y_train_val==class_names.index(c))[:,0])   
        samples_to_delete += random.sample(samples, k=int(fraction*len(samples)))
    
    x_train_val= np.delete(x_train_val,samples_to_delete,0)
    y_train_val= np.delete(y_train_val,samples_to_delete,0)
    
    x_train, x_val, y_train, y_val = train_test_split(x_train_val,
                                                      y_train_val,
                                                      test_size=val_size,
                                                      random_state=random_state)
    
    y_train_ohe = np_utils.to_categorical(y_train,len(class_names))
    y_test_ohe= np_utils.to_categorical(y_test,len(class_names))
    y_val_ohe = np_utils.to_categorical(y_val,len(class_names))

    return x_train, x_val , x_test, y_train_ohe, y_val_ohe, y_test_ohe, class_names

def load_class_names():
    '''Returns names of unique classes in cifar10'''
    return ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def normalize(x,max_value=None):
    '''Returns normalized numpy array x by dividing it by max_value or 255

    
    Parameters:

    x(4d array): 4d array to normalize

    max_value(int): value to use in the normalization (if 'None', 255 is used)


    Returns:

    4d array corresponding to normalized x 
    
    '''
    if max_value:
        print('Normalized by the maximum value of training set')
        return x/max_value
    else:
        return x/255

def normalize_splits(x_train, x_val, x_test):
    '''Returns normalized training, validation and test splits by maximum value
    x_train

    
    Parameters:

    x_train (numpy array): numpy array to normalize

    max_value(int): value to use in the normalization (if 'None', 255 is used)


    Returns:

    x/max_value or x/255(numpy array): normalized numpy array. 
    
    '''
    max_value= np.max(x_train)
    x_train= normalize(x_train, max_value)
    x_val= normalize(x_val, max_value)
    x_test= normalize(x_test, max_value)
    return x_train, x_val, x_test

def class_count(y,class_names):
    '''Counts the number of samples of each class in 2d array y


    Parameters:

    y(2d array): one-hot encoded 2d array with classification 
    values

    class_names(list): list with unique class names in dataset under study

    '''
    print('Number of samples:',y.shape[0])
    for i,c in enumerate(class_names):
            print(c,':',np.count_nonzero(y,axis=0)[i])

def class_count_splits(y_train,y_val,y_test,class_names):
    '''Counts the number of samples of each class in the training, validation 
    and test sets
    

    Parameters:

    y_train(2d array): one-hot encoded 2d array with classification 
    values for the training set

    y_val(2d array): one-hot encoded 2d array with classification 
    values for the validation set

    y_test(2d array):  one-hot encoded 2d array with classification 
    values for the validation set

    class_names(list): list with unique class names in dataset under study

    '''
    print('**Training data**')
    class_count(y_train,class_names)
    print('')
    print('**Validation data**')
    class_count(y_val,class_names)
    print('')
    print('**Test data**')
    class_count(y_test,class_names)

def load_and_norm(val_size=0.22, random_state=42):
    '''Returns normalized training, validation, and test splits with 50% of
    samples of classes bird, deer, and truck removed from train+validation


    Parameters:

    val_size(float): validation size as a fraction of train+val size

    random_state(defaults to 42): random seed for train/val split


    Returns:

    x_train_norm(4d array): 4d array with normalized training set 

    x_val_norm(4d array): 4d array with normalized validation set

    x_test_norm(4d array): 4d array with normalized test set

    y_train(2d array): one-hot encoded 2d array with classification 
    values for the training set

    y_val(2d array): one-hot encoded 2d array with classification 
    values for the validation set

    y_test(2d array):  one-hot encoded 2d array with classification 
    values for the validation set

    class_names(list): list with unique class names in cifar10

    '''
    (x_train, x_val,x_test, 
     y_train, y_val, y_test, 
    class_names) = load_data(remove_classes=['bird','deer','truck'],
                             val_size=val_size, random_state=random_state)
    
    x_train_norm, x_val_norm, x_test_norm= normalize_splits(x_train, 
                                                            x_val, 
                                                            x_test)
    class_count_splits(y_train,
                       y_val,
                       y_test,
                       class_names)

    return x_train_norm, x_val_norm, x_test_norm, y_train, y_val, y_test, class_names

def show_image_list(x, y, class_names, image_list):
    '''Plots a list of up to 20 images with class names, raises valuer error
    when number of images to plot is higher than 20


    Parameters:

    x(4d array): 4d array representing a set of images

    y(2d array): 4d array one-encoding classification of images in x

    class_names(list): list of unique classes in y with a matching order

    image_list(list): list of image indexes in x to plot

    '''
    if  len(image_list) > 20:
        raise ValueError('The number of images to plot cannot be higher than 20.')
    fig =plt.figure(figsize=(18,6))
    for i,index in enumerate(image_list):
        ax=fig.add_subplot(2,10,1+i,xticks=[],yticks=[])
        ax.set_title(class_names[sum(np.argwhere(y[index]==1)[0])])
        plt.imshow(x[index])
    plt.show()

def random_images(y,class_names):
    '''Returns indexes of randomly selected images, each one belonging to each 
     class in class_names

    Parameters:

    y(2d array): one-hot encoded numpy array with image classification values

    class_names(list): list of 

    '''
    y= y.argmax(axis=1)
    selected=[]
    for i,c in enumerate(class_names):
        sample= list(random.choice(np.argwhere(y==i)))
        selected+= sample
    return selected

def show_image(x, y, class_names):
    '''Plots a single image x with respective class name
    

    Parameters:

    x(3d array): 2d array representing an image

    y(2d array): 2d array representing one-hot encoded classification of x
    
    '''
    fig =plt.figure()
    plt.title(class_names[sum(np.argwhere(y==1)[0])])
    plt.imshow(x)
    plt.show()