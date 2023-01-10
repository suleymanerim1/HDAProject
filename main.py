# Import Packages
import tensorflow as tf
from tensorflow import keras
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os
import numpy as np
from IPython.display import Image

import cnn_models
import utils
import dnn_models

# Create train dataset
train_path = 'Bone Age Datasets\\train'
train_csv_path = 'Bone Age Datasets\\train.csv'

validation_path = 'Bone Age Datasets\\validation'
validation_csv_path = 'Bone Age Datasets\\validation.csv'

test_path = 'Bone Age Datasets\\test'
test_csv_path = 'Bone Age Datasets\\test.csv'

Input_Size = 224

train = (train_path, train_csv_path)
val = (validation_path, validation_csv_path)
test = (test_path, test_csv_path)
data_paths = [train, val, test]
datasets = []
for path in data_paths:
    # return images paths list and features (id,male,age)
    image_file_list, features = utils.image_csv_match(path[0], path[1])

    # create a tf.dataset of test images
    images_dataset = utils.image_dataset_creator_from_path(image_file_list, Input_Size)

    # get age from features
    age = (features[:, -1]).astype(float)
    # Create an age tf.dataset from the NumPy array
    age_dataset = tf.data.Dataset.from_tensor_slices(age)

    # get gender from features
    gender = (features[:, 1]).astype(int)
    # Create an age tf.dataset from the NumPy array
    gender_dataset = tf.data.Dataset.from_tensor_slices(gender)

    # Create a dataset of images zipped with age
    datasets.append(tf.data.Dataset.zip(((images_dataset, gender_dataset), age_dataset)))

train_dataset = datasets[0]
val_dataset = datasets[1]
test_dataset = datasets[2]

batch_size = 64
train_dataset = utils.create_dataset(train_dataset,
                                     batch_size=batch_size,
                                     shuffle=False,
                                     augment=False,
                                     cache_file='train_cache'
                                     )
val_dataset = utils.create_dataset(val_dataset,
                                   batch_size=batch_size,
                                   cache_file='validation_cache'
                                   )
test_dataset = utils.create_dataset(test_dataset,
                                    batch_size=batch_size,
                                    cache_file='test_cache')


print(train_dataset)
print(val_dataset)
print(test_dataset)


model = cnn_models.LeNet_Model((Input_Size, Input_Size, 3))

num_params = model.count_params()
print(f'Number of parameters: {num_params:,}\n')

utils.print_memory_info()
model.summary()

# Create a callback that will interrupt training when the validation loss stops improving
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, restore_best_weights=True)

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,
                              patience=5, min_lr=0.001,verbose=1)

epochs = 25
initial_lrate = 0.1

adam_optimizer = keras.optimizers.Adam(learning_rate=initial_lrate)
# Compile the model
model.compile(optimizer=adam_optimizer, loss=tf.keras.losses.MeanAbsoluteError(),
              metrics=tf.keras.metrics.mean_absolute_error)

# Train the model
hist = model.fit(train_dataset, epochs=500,
                 validation_data=val_dataset,
                 callbacks=[early_stopping, reduce_lr],
                 use_multiprocessing=True,
                 workers=os.cpu_count()
                 )

# Evaluate the model
test_mae = model.evaluate(test_dataset, workers=-1)
print('Test loss:', test_mae)

print("\n")
print("-----------------------------------------------")

utils.hist_graphs(hist)

# Save the model in HDF5 format
keras.models.save_model(model, './denememodel/model.h5')
np.save('./denememodel/dnn_history.npy', hist.history)
# Show the structure of the model through building blocks
keras.utils.plot_model(model, to_file='./denememodel/dnn_model.png')
Image("./denememodel/dnn_model.png")


# Restore the model from the HDF5 file
# model = tf.keras.models.load_model('./denememodel/model.h5')
# Get back the history
# history1=np.load('./denememodel/history1.npy',allow_pickle='TRUE').item()
