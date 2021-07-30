import tensorflow as tf
import sys
#import numpy as np
#import cv2
from tensorflow.keras.callbacks import (
    ReduceLROnPlateau,
    EarlyStopping,
    ModelCheckpoint,
    TensorBoard
)
#from 
#from model_ready.train_model import (
#    YoloV3, yolo_anchors, yolo_anchor_masks
#)
import dataset



# size image size
# path_to_dataset 
# path_to_classes example ./data/coco.names
# num_classes

def main(_argv):
    # define model
    model = YoloV3(size, training=True, classes=num_classes)
    anchors = yolo_anchors
    anchor_masks = yolo_anchor_masks
    # load train dataset in tf.record format
    train_dataset = dataset.load_tfrecord_dataset(path_to_dataset, path_to_classes_file, size)
    train_dataset = train_dataset.shuffle(buffer_size=512)
    train_dataset = train_dataset.batch(batch_size)
    train_dataset = train_dataset.map(lambda x, y: (
        dataset.transform_images(x, size),
        dataset.transform_targets(y, anchors, anchor_masks, size)))
    train_dataset = train_dataset.prefetch(
        buffer_size=tf.data.experimental.AUTOTUNE)
    # load valid dataset in tf.record format
    val_dataset = dataset.load_tfrecord_dataset(
            val_dataset, path_to_classes_file, size)
    val_dataset = val_dataset.batch(batch_size)
    val_dataset = val_dataset.map(lambda x, y: (
        dataset.transform_images(x, size),
        dataset.transform_targets(y, anchors, anchor_masks, size)))

    # Configure the model 
    optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
    loss = [YoloLoss(anchors[mask], classes=num_classes)
            for mask in anchor_masks]
    model.compile(optimizer=optimizer, loss=loss)

    callbacks = [
            ReduceLROnPlateau(verbose=1),
            EarlyStopping(patience=3, verbose=1),
            ModelCheckpoint('checkpoints/yolov3_train_{epoch}.tf',
                            verbose=1, save_weights_only=True),
            TensorBoard(log_dir='logs')
        ]

    history = model.fit(train_dataset,
                            epochs=epochs,
                            callbacks=callbacks,
                            validation_data=val_dataset)


if __name__ == '__main__':
    try:
        sys.app.run(main)
    except SystemExit:
        pass
