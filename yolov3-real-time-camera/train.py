import tensorflow as tf
import sys

from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint


from train_model import dataset
from yolov3 import *



def main(size, classes, path_to_train_record, 
         path_to_val_record, path_to_file_names, buffer_size, batch_size, 
         path_to_weights, learning_rate, epochs):
    
    model = YoloV3(size = size, classes = classes, training = True)
    
    anchors = yolo_anchors
    anchor_masks = yolo_anchor_masks
    
    train_dataset = dataset.load_tfrecord_dataset(path_to_train_record, path_to_file_names, size)
    train_dataset = train_dataset.shuffle(buffer_size=buffer_size)
    train_dataset = train_dataset.batch(batch_size)
    train_dataset = train_dataset.map(lambda x, y: (transform_images(x, size), transform_targets(y, anchors, anchor_masks, size)))
    train_dataset = train_dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    
    val_dataset = dataset.load_tfrecord_dataset(path_to_val_record, path_to_file_names, size)
    val_dataset = val_dataset.batch(batch_size)
    val_dataset = val_dataset.map(lambda x, y: (transform_images(x, size), transform_targets(y, anchors, anchor_masks, size)))
    
    load_darknet_weights(model, path_to_weights)
    darknet = model.get_layer('yolo_darknet')
    freeze_all(darknet)
    
    optimizer = tf.keras.optimizers.Adam(lr = learning_rate)
    loss = [YoloLoss(anchors[mask], classes = classes) for mask in anchor_masks]
    model.compile(optimizer=optimizer, loss=loss)

    callbacks = [
            ReduceLROnPlateau(verbose=1),
            EarlyStopping(patience=3, verbose=1),
            ModelCheckpoint('weights/saved_modelname', save_weights_only=True)]
    
    history = model.fit(train_dataset, epochs = epochs, callbacks = callbacks, validation_data = val_dataset)

main(size = 416, classes = 80, path_to_train_record = 'E:/train.record', path_to_val_record = 'E:/test.record',
     path_to_file_names = 'E:/voc2012.names', buffer_size = 1, 
     batch_size = 1, path_to_weights = 'E:/yolov3.weights',
     learning_rate = 0.01, epochs = 20)


# https://github.com/zzh8829/yolov3-tf2/blob/master/train.py    
    


