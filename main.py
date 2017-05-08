from keras.models import Sequential
from keras.layers import Conv2D, Activation, MaxPool2D, Dropout, Flatten, Dense, AvgPool2D

import dataset
import networks

from evaluation import precision, recall, f1_score

SIZE = 15
BATCH_SIZE = 64
QUEUE_SIZE = 20
EPOCHS = 10

def main():
    print("load full data into memory")
    data = dataset.getDataset()
    print("use date inside patch generator")
    lsg = dataset.LandslideGenerator(data, SIZE, BATCH_SIZE, 0.4, True)

    model = Sequential()
    model.add(Conv2D(32, (5, 5), input_shape=(SIZE, SIZE, 12)))
    model.add(Activation('relu'))
    model.add(Conv2D(16, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPool2D((1, 1), strides=(1, 1)))
    model.add(Dropout(0.25))

    # model.add(Dense(512, activation='relu', name='dense'))
    # model.add(Dropout(0.25))

    model.add(AvgPool2D((3, 3), strides=(1, 1)))
    model.add(Flatten(name="flatten"))

    model.add(Dense(1, name='last_layer'))
    model.add(Activation('sigmoid'))

    model.compile(optimizer="adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy", precision, recall, f1_score])

    model.fit_generator(lsg,
                        steps_per_epoch=10000,
                        epochs=EPOCHS,
                        verbose=True,
                        max_q_size=QUEUE_SIZE,
                        workers=1)
    
    model.save("./model.h5")


if __name__ == "__main__":
    main()
