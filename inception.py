from keras.layers import Conv2D, MaxPool2D, \
    Dropout, Dense, Input, concatenate, AveragePooling2D, BatchNormalization, Activation
from keras.models import Model
from keras.regularizers import L2


def inception_module_without_bn(X,
                     filters_1x1,
                     filters_3x3_reduce,
                     filters_3x3,
                     filters_5x5_reduce,
                     filters_5x5,
                     filters_pool_proj,
                     name=None):
    conv_1x1 = Conv2D(filters_1x1, (1, 1), padding='same', activation='relu',kernel_regularizer=L2(0.0001),name = name + 'conv_1-1')(X)

    conv_3x3 = Conv2D(filters_3x3_reduce, (1, 1), padding='same', activation='relu',kernel_regularizer=L2(0.0001),name = name + 'conv_3-3_reduce')(X)
    conv_3x3 = Conv2D(filters_3x3, (3, 3), padding='same', activation='relu',kernel_regularizer=L2(0.0001),name = name + 'conv_3-3')(conv_3x3)

    conv_5x5 = Conv2D(filters_5x5_reduce, (1, 1), padding='same', activation='relu',kernel_regularizer=L2(0.0001),name = name + 'conv_5-5_reduce')(X)
    conv_5x5 = Conv2D(filters_5x5, (5, 5), padding='same', activation='relu',kernel_regularizer=L2(0.0001),name = name + 'conv_5-5')(conv_5x5)

    pool_proj = MaxPool2D((3, 3), strides=(1, 1), padding='same',name = name + '_max_pool')(X)
    pool_proj = Conv2D(filters_pool_proj, (1, 1), padding='same', activation='relu',kernel_regularizer=L2(0.0001),name = name + '_max_pool_reduce')(pool_proj)

    output = concatenate([conv_1x1, conv_3x3, conv_5x5, pool_proj], axis=3, name=name)

    return output

def inception_module_without_bn_without_weightdecay(X,
                     filters_1x1,
                     filters_3x3_reduce,
                     filters_3x3,
                     filters_5x5_reduce,
                     filters_5x5,
                     filters_pool_proj,
                     name=None):
    conv_1x1 = Conv2D(filters_1x1, (1, 1), padding='same', activation='relu',name = name + 'conv_1-1')(X)

    conv_3x3 = Conv2D(filters_3x3_reduce, (1, 1), padding='same', activation='relu',name = name + 'conv_3-3_reduce')(X)
    conv_3x3 = Conv2D(filters_3x3, (3, 3), padding='same', activation='relu',name = name + 'conv_3-3')(conv_3x3)

    conv_5x5 = Conv2D(filters_5x5_reduce, (1, 1), padding='same', activation='relu',name = name + 'conv_5-5_reduce')(X)
    conv_5x5 = Conv2D(filters_5x5, (5, 5), padding='same', activation='relu',name = name + 'conv_5-5')(conv_5x5)

    pool_proj = MaxPool2D((3, 3), strides=(1, 1), padding='same',name = name + '_max_pool')(X)
    pool_proj = Conv2D(filters_pool_proj, (1, 1), padding='same', activation='relu',name = name + '_max_pool_reduce')(pool_proj)

    output = concatenate([conv_1x1, conv_3x3, conv_5x5, pool_proj], axis=3, name=name)

    return output

def inception_module_with_bn(X,
                     filters_1x1,
                     filters_3x3_reduce,
                     filters_3x3,
                     filters_5x5_reduce,
                     filters_5x5,
                     filters_pool_proj,
                     name=None):

    conv_1x1 = Conv2D(filters_1x1, (1, 1), padding='same',kernel_regularizer=L2(0.0001),name = name + 'conv_1-1')(X)
    conv_1x1 = BatchNormalization(axis=3,name=name + 'batch_norm_1-1')(conv_1x1)
    conv_1x1 = Activation('relu',name=name + 'relu_1-1')(conv_1x1)

    conv_3x3 = Conv2D(filters_3x3_reduce, (1, 1), padding='same',kernel_regularizer=L2(0.0001),name = name + 'conv_3-3_reduce')(X)
    conv_3x3 = BatchNormalization(axis=3,name=name + 'batch_norm_3-3_reduce')(conv_3x3)
    conv_3x3 = Activation('relu',name=name + 'relu_3-3_reduce')(conv_3x3)
    conv_3x3 = Conv2D(filters_3x3, (3, 3), padding='same',kernel_regularizer=L2(0.0001),name = name + 'conv_3-3')(conv_3x3)
    conv_3x3 = BatchNormalization(axis=3,name=name + 'batch_norm_3-3')(conv_3x3)
    conv_3x3 = Activation('relu',name=name + 'relu_3-3')(conv_3x3)

    conv_5x5 = Conv2D(filters_5x5_reduce, (1, 1), padding='same',kernel_regularizer=L2(0.0001),name = name + 'conv_5-5_reduce')(X)
    conv_5x5 = BatchNormalization(axis=3,name=name + 'batch_norm_5-5_reduce')(conv_5x5)
    conv_5x5 = Activation('relu',name=name + 'relu_5-5_reduce')(conv_5x5)
    conv_5x5 = Conv2D(filters_5x5, (5, 5), padding='same',kernel_regularizer=L2(0.0001),name = name + 'conv_5-5')(conv_5x5)
    conv_5x5 = BatchNormalization(axis=3,name=name + 'batch_norm_5-5')(conv_5x5)
    conv_5x5 = Activation('relu',name=name + 'relu_5-5')(conv_5x5)

    pool_proj = MaxPool2D((3, 3), strides=(1, 1), padding='same',name = name + '_max_pool')(X)
    pool_proj = Conv2D(filters_pool_proj, (1, 1), padding='same',kernel_regularizer=L2(0.0001),name = name + '_max_pool_reduce')(pool_proj)
    pool_proj = BatchNormalization(axis=3,name=name + 'batch_norm_pool_reduce')(pool_proj)
    pool_proj = Activation('relu',name=name + 'relu_pool_reduce')(pool_proj)

    output = concatenate([conv_1x1, conv_3x3, conv_5x5, pool_proj], axis=3, name=name + 'concat')

    return output


def inception_module_without_weigth_decay(X,
                     filters_1x1,
                     filters_3x3_reduce,
                     filters_3x3,
                     filters_5x5_reduce,
                     filters_5x5,
                     filters_pool_proj,
                     name=None):

    conv_1x1 = Conv2D(filters_1x1, (1, 1), padding='same',name = name + 'conv_1-1')(X)
    conv_1x1 = BatchNormalization(axis=3,name=name + 'batch_norm_1-1')(conv_1x1)
    conv_1x1 = Activation('relu',name=name + 'relu_1-1')(conv_1x1)

    conv_3x3 = Conv2D(filters_3x3_reduce, (1, 1), padding='same',name = name + 'conv_3-3_reduce')(X)
    conv_3x3 = BatchNormalization(axis=3,name=name + 'batch_norm_3-3_reduce')(conv_3x3)
    conv_3x3 = Activation('relu',name=name + 'relu_3-3_reduce')(conv_3x3)
    conv_3x3 = Conv2D(filters_3x3, (3, 3), padding='same',name = name + 'conv_3-3')(conv_3x3)
    conv_3x3 = BatchNormalization(axis=3,name=name + 'batch_norm_3-3')(conv_3x3)
    conv_3x3 = Activation('relu',name=name + 'relu_3-3')(conv_3x3)

    conv_5x5 = Conv2D(filters_5x5_reduce, (1, 1), padding='same',name = name + 'conv_5-5_reduce')(X)
    conv_5x5 = BatchNormalization(axis=3,name=name + 'batch_norm_5-5_reduce')(conv_5x5)
    conv_5x5 = Activation('relu',name=name + 'relu_5-5_reduce')(conv_5x5)
    conv_5x5 = Conv2D(filters_5x5, (5, 5), padding='same',name = name + 'conv_5-5')(conv_5x5)
    conv_5x5 = BatchNormalization(axis=3,name=name + 'batch_norm_5-5')(conv_5x5)
    conv_5x5 = Activation('relu',name=name + 'relu_5-5')(conv_5x5)

    pool_proj = MaxPool2D((3, 3), strides=(1, 1), padding='same',name = name + '_max_pool')(X)
    pool_proj = Conv2D(filters_pool_proj, (1, 1), padding='same',name = name + '_max_pool_reduce')(pool_proj)
    pool_proj = BatchNormalization(axis=3,name=name + 'batch_norm_pool_reduce')(pool_proj)
    pool_proj = Activation('relu',name=name + 'relu_pool_reduce')(pool_proj)

    output = concatenate([conv_1x1, conv_3x3, conv_5x5, pool_proj], axis=3, name=name + 'concat')

    return output







input_layer = Input(shape=(224, 224, 3))

X = Conv2D(64, (7, 7), padding='same', strides=(2, 2), activation='relu', name='conv_1_7x7/2')(input_layer)
X = MaxPool2D((3, 3), padding='same', strides=(2, 2), name='max_pool_1_3x3/2')(X)
X = Conv2D(64, (1, 1), padding='same', strides=(1, 1), activation='relu', name='conv_2a_3x3/1')(X)
X = Conv2D(192, (3, 3), padding='same', strides=(1, 1), activation='relu', name='conv_2b_3x3/1')(X)
X = MaxPool2D((3, 3), padding='same', strides=(2, 2), name='max_pool_2_3x3/2')(X)

X = inception_module_with_bn(X,
                     filters_1x1=64,
                     filters_3x3_reduce=96,
                     filters_3x3=128,
                     filters_5x5_reduce=16,
                     filters_5x5=32,
                     filters_pool_proj=32,
                     name='inception_3a')

X = inception_module_with_bn(X,
                     filters_1x1=128,
                     filters_3x3_reduce=128,
                     filters_3x3=192,
                     filters_5x5_reduce=32,
                     filters_5x5=96,
                     filters_pool_proj=64,
                     name='inception_3b')

X = MaxPool2D((3, 3), padding='same', strides=(2, 2), name='max_pool_3_3x3/2')(X)

X = inception_module_with_bn(X,
                     filters_1x1=192,
                     filters_3x3_reduce=96,
                     filters_3x3=208,
                     filters_5x5_reduce=16,
                     filters_5x5=48,
                     filters_pool_proj=64,
                     name='inception_4a')

X = inception_module_with_bn(X,
                     filters_1x1=160,
                     filters_3x3_reduce=112,
                     filters_3x3=224,
                     filters_5x5_reduce=24,
                     filters_5x5=64,
                     filters_pool_proj=64,
                     name='inception_4b')

X = inception_module_with_bn(X,
                     filters_1x1=128,
                     filters_3x3_reduce=128,
                     filters_3x3=256,
                     filters_5x5_reduce=24,
                     filters_5x5=64,
                     filters_pool_proj=64,
                     name='inception_4c')

X = inception_module_with_bn(X,
                     filters_1x1=112,
                     filters_3x3_reduce=144,
                     filters_3x3=288,
                     filters_5x5_reduce=32,
                     filters_5x5=64,
                     filters_pool_proj=64,
                     name='inception_4d')

X = inception_module_with_bn(X,
                     filters_1x1=256,
                     filters_3x3_reduce=160,
                     filters_3x3=320,
                     filters_5x5_reduce=32,
                     filters_5x5=128,
                     filters_pool_proj=128,
                     name='inception_4e')

X = MaxPool2D((3, 3), padding='same', strides=(2, 2), name='max_pool_4_3x3/2')(X)

X = inception_module_with_bn(X,
                     filters_1x1=256,
                     filters_3x3_reduce=160,
                     filters_3x3=320,
                     filters_5x5_reduce=32,
                     filters_5x5=128,
                     filters_pool_proj=128,
                     name='inception_5a')

X = inception_module_with_bn(X,
                     filters_1x1=384,
                     filters_3x3_reduce=192,
                     filters_3x3=384,
                     filters_5x5_reduce=48,
                     filters_5x5=128,
                     filters_pool_proj=128,
                     name='inception_5b')

X = AveragePooling2D(pool_size=(7, 7), strides=1, padding='valid', name='avg_pool_5_3X3/1')(X)

X = Dropout(0.4)(X)
X = Dense(1000, activation='relu', name='linear')(X)
X = Dense(1, name='output')(X)
#inceptiom_model = Model(input_layer, [X], name='googlenet')

#inceptiom_model.summary()
