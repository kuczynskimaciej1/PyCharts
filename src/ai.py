from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras import layers, models
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.metrics import Accuracy, CategoricalAccuracy, MeanSquaredError
import ai_global_var
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def teachEmbeddings(label):
    categories = ai_global_var.df[label].unique()
    num_categories = len(categories)
    embedding_dim = 10

    encoder = OneHotEncoder(sparse=False)
    label_encoded = encoder.fit_transform(ai_global_var.df[label].array.reshape(-1,1))

    X_train, X_test = train_test_split(label_encoded, test_size=0.2, random_state=42)

    model = models.Sequential([
        layers.Embedding(input_dim=num_categories, output_dim=embedding_dim),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(label_encoded.shape[1], activation='linear')
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=[Accuracy(), CategoricalAccuracy()])
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    checkpoint_path = f'models/spotify_recommendation_model_{label}.keras'
    model_checkpoint = ModelCheckpoint(checkpoint_path, save_best_only=True)
    history = model.fit(X_train, X_train, epochs=100, batch_size=16, validation_data=(X_test, X_test), callbacks=[early_stopping, model_checkpoint])
    model.save(f'models/spotify_recommendation_model_{label}.h5')
    print(model.summary())

    training_accuracy = history.history['accuracy']
    validation_accuracy = history.history['val_accuracy']
    training_cat_accuracy = history.history['categorical_accuracy']
    validation_cat_accuracy = history.history['val_categorical_accuracy']
    plt.plot(training_accuracy, label='Training Accuracy')
    plt.plot(validation_accuracy, label='Validation Accuracy')
    plt.plot(training_cat_accuracy, label='Training Cat Accuracy')
    plt.plot(validation_cat_accuracy, label='Validation Cat Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    label_embedding_output = model.predict(X_train)
    categories = categories.reshape((1, -1))
    label_embedding_output = np.concatenate([categories, label_embedding_output])
    label_embedding_output = label_embedding_output[:2, :]
    label_embedding_output = np.transpose(label_embedding_output)
    label_embedding_output = pd.DataFrame(label_embedding_output)

    return label_embedding_output


def trainEmbeddings():
    ai_global_var.artist_encoded = teachEmbeddings('Artist')
    ai_global_var.album_encoded = teachEmbeddings('Album')


def teach(features):
    X_train, X_test = train_test_split(features, test_size=0.2, random_state=42)

    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        #layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        #layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.Dense(features.shape[1], activation='linear')
    ])


    model.compile(optimizer='adam', loss='mean_squared_error', metrics=[MeanSquaredError(), CategoricalAccuracy()])
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    checkpoint_path = f'models/spotify_recommendation_model.keras'
    model_checkpoint = ModelCheckpoint(checkpoint_path, save_best_only=True)
    history = model.fit(X_train, X_train, epochs=100, batch_size=16, validation_data=(X_test, X_test), callbacks=[early_stopping, model_checkpoint])
    model.save('models/spotify_recommendation_model.h5')
    print(model.summary())

    training_accuracy = history.history['mean_squared_error']
    validation_accuracy = history.history['val_mean_squared_error']
    training_cat_accuracy = history.history['categorical_accuracy']
    validation_cat_accuracy = history.history['val_categorical_accuracy']
    plt.plot(training_accuracy, label='Training Accuracy')
    plt.plot(validation_accuracy, label='Validation Accuracy')
    plt.plot(training_cat_accuracy, label='Training Cat Accuracy')
    plt.plot(validation_cat_accuracy, label='Validation Cat Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


def teachNumerical(features):
    X_train, X_test = train_test_split(features, test_size=0.2, random_state=42)

    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        #layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        #layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.Dense(features.shape[1], activation='linear')
    ])


    model.compile(optimizer='adam', loss='mean_squared_error', metrics=[MeanSquaredError(), Accuracy()])
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    checkpoint_path = f'models/spotify_recommendation_model_mood.keras'
    model_checkpoint = ModelCheckpoint(checkpoint_path, save_best_only=True)
    history = model.fit(X_train, X_train, epochs=100, batch_size=16, validation_data=(X_test, X_test), callbacks=[early_stopping, model_checkpoint])
    model.save('models/spotify_recommendation_model_mood.h5')
    print(model.summary())

    training_accuracy = history.history['mean_squared_error']
    validation_accuracy = history.history['val_mean_squared_error']
    plt.plot(training_accuracy, label='Training Accuracy')
    plt.plot(validation_accuracy, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
