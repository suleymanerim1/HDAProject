#!/usr/bin/env python
# coding: utf-8

# Import Packages
import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras import Sequential
from keras import layers



# Load Datasets
def image_csv_match(image_path, csv_path):
    """
    Matches images in the specified directory with their corresponding features stored in a CSV file.

    Parameters:
        image_path (str): The directory containing the images.
        csv_path (str): The path to the CSV file containing the features.

    Returns:
        A tuple containing two lists:
            - A list of image file paths
            - A list of corresponding features
    """

    # Load the filenames of the images
    filenames = os.listdir(image_path)

    # Load the CSV file
    csv = np.loadtxt(csv_path, dtype=str, delimiter=",")

    # Get the list of IDs in the CSV file
    ids = csv[:, 0]

    # Initialize an empty array to store the images and the features
    image_file_list = []
    features = []
    # Iterate over the image filenames
    for filename in filenames:
        # Extract the ID from the filename
        id = filename.split(".")[0]

        # Check if the ID is in the CSV file
        if np.isin(id, ids):
            # Load the image
            file_path = os.path.join(image_path, filename)

            # Extract the corresponding features from the CSV file
            feature = csv[np.where(ids == id), 0:]

            # Append the image and the features to the array
            image_file_list.append(file_path)
            features.append(feature)

    # Convert the array to a NumPy array
    return image_file_list, np.array(features).squeeze()


def image_dataset_creator_from_path(image_file_list, Input_size=224):
    """
    Creates a dataset from a list of image file paths. The images are read, decoded, resized, and standardized.

    Parameters:
        image_file_list (list): A list of image file paths.

    Returns:
        A TensorFlow dataset containing the images.
        :param Input_size:
        :param image_file_list:
    """
    # Create a dataset from the list of image paths
    dataset = tf.data.Dataset.from_tensor_slices(image_file_list)

    # Define a function to read and decode an image
    def read_and_decode_image(image_path):
        # Read the image file
        image_string = tf.io.read_file(image_path)
        # Decode the image
        image = tf.image.decode_png(image_string, channels=1)
        # Resize the image
        image_resized = tf.image.resize(image, (Input_size, Input_size))
        # Standardized image
        image_standardized = tf.image.convert_image_dtype(
            image_resized, dtype=tf.float32)
        return image_standardized

    # Map the function over the dataset
    dataset = dataset.map(read_and_decode_image)

    return dataset


# Augmentation
#def data_augmentation(images):
#    # Randomly flip the images horizontally
#    seed = (1, 2)
#    images = tf.image.stateless_random_flip_left_right(images,seed)
#
#    # Randomly adjust the brightness of the images
#    seed = (1, 2)
#    images = tf.image.stateless_random_saturation(images, 0, 0.25,seed)
#
#    # Randomly adjust the contrast of the images
#    seed = (1, 2)
#    images = tf.image.stateless_random_contrast(images, 0, 0.25,seed)
#    return images

# Create a data augmentation stage with ing, rotations,translation, zooms, horizontal flipp
data_augmentation = Sequential(
    [
        layers.RandomRotation(0.2),
        layers.RandomTranslation(height_factor= 0.2,width_factor=0.2),
        layers.RandomZoom(0.2),
        layers.RandomFlip("horizontal")
    ]
)


# Create Dataset
AUTOTUNE = tf.data.AUTOTUNE


def create_dataset(dataset, batch_size, shuffle=False, augment=False, cache_file=None):
    """
    Creates a TensorFlow dataset from a given dataset. The dataset is shuffled, repeated indefinitely, 
    batched, and prefetched as specified. Optionally, the dataset can be augmented and cached.

    Parameters:
        dataset (tf.data.Dataset): The dataset to be transformed.
        batch_size (int): The batch size for the dataset.
        shuffle (bool, optional): Whether to shuffle the dataset. Defaults to False.
        augment (bool, optional): Whether to augment the dataset. Defaults to False.
        cache_file (str, optional): The file path to cache the dataset. Defaults to None.

    Returns:
        A TensorFlow dataset.
    """

    # Cache dataset
    if cache_file:
        dataset = dataset.cache(cache_file)

    # Shuffle
    if shuffle:
        dataset = dataset.shuffle(batch_size * 5)

    # Repeat the dataset indefinitely
    dataset = dataset.repeat()

    # Batch
    dataset = dataset.batch(batch_size=batch_size)

    if augment:
        dataset = dataset.map(lambda x, y: ((data_augmentation(x[0]),x[1]),y),
                              num_parallel_calls=AUTOTUNE)

    # Prefetch
    dataset = dataset.prefetch(buffer_size=AUTOTUNE)

    return dataset


# Visualize  Model Output
def print_memory_info():
    """
    Prints the current and peak memory usage of the notebook process in megabytes.
    """
    import psutil
    import os

    # Get the current and peak memory usage of the notebook process
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    print("\n")
    print("-----------------------------------------------")
    # Print the current and peak memory usage in megabytes
    print(f"Current memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {memory_info.peak_wset / 1024 / 1024:.2f} MB")
    print("-----------------------------------------------")
    print("\n")


def hist_graphs(hist):
    # Extract the history data
    loss = hist.history['loss']
    val_loss = hist.history['val_loss']

    # Set up the subplots
    fig, (ax1) = plt.subplots(1, 1, figsize=(12, 4))

    # Plot the loss for the training and validation sets
    ax1.plot(loss)
    ax1.plot(val_loss)
    ax1.set_title('Model loss')
    ax1.set_ylabel('Loss')
    ax1.set_xlabel('Epoch')
    ax1.legend(['Training', 'Validation'], loc='upper left')
    plt.ylim((0,50))

    plt.show()

