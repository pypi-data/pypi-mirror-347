def dlans(num):
    if(num == 1):
        print("""from tensorflow.keras.datasets import mnist 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Flatten 
import numpy as np 
from sklearn.metrics import accuracy_score 
(x_train, y_train), (x_test, y_test) = mnist.load_data() 
x_train, x_test = x_train / 255.0, x_test / 255.0 
model = Sequential([ 
Flatten(input_shape=(28, 28)), 
Dense(128, activation='relu'), 
Dense(64, activation='relu'), 
Dense(10, activation='softmax') 
]) 
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', 
metrics=['accuracy']) 
model.fit(x_train, y_train, epochs=5, batch_size=32) 
predictions = model.predict(x_test) 
predicted_labels = np.argmax(predictions, axis=1) 
print("Sample Predicted:", predicted_labels[:10]) 
print("Actual:", y_test[:10]) 
print("Overall Accuracy:", accuracy_score(y_test, predicted_labels)) """)

    elif(num == 2):
        print("""from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Flatten 
import numpy as np 
from sklearn.metrics import accuracy_score 
from tensorflow.keras.datasets import cifar10 
(x_train, y_train), (x_test, y_test) = cifar10.load_data() 
x_train, x_test = x_train / 255.0, x_test / 255.0 
y_train, y_test = y_train.flatten(), y_test.flatten() 
model = Sequential([ 
Flatten(input_shape=(32, 32, 3)), 
Dense(512, activation='relu'), 
Dense(256, activation='relu'), 
Dense(10, activation='softmax') 
]) 
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', 
metrics=['accuracy']) 
model.fit(x_train, y_train, epochs=5, batch_size=64) 
predictions = model.predict(x_test) 
predicted_labels = np.argmax(predictions, axis=1) 
print("Sample Predicted:", predicted_labels[:10]) 
print("Actual:", y_test[:10]) 
print("Overall Accuracy:", accuracy_score(y_test, predicted_labels)) """)

    elif(num == 3):
        print("""import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.losses import BinaryCrossentropy

inputs=np.array([[0,0],[0,1],[1,0],[1,1]],dtype=np.float32)
targets=np.array([[0],[1],[1],[0]],dtype=np.float32)

model=Sequential()
model.add(Dense(4,input_dim=2,activation='sigmoid'))
model.add(Dense(1,activation='sigmoid'))

model.compile(optimizer=SGD(learning_rate=0.1),loss=BinaryCrossentropy(),metrics=['accuracy'])
model.fit(inputs,targets,epochs=5000,verbose=0)

predictions=model.predict(inputs)
print("Input->predicted output")

for input_val,prediction in zip(inputs,predictions):
  print(f'{input_val}->{prediction[0]:.4f}')""")

    elif(num == 4):
        print("""import numpy as np 
import tensorflow as tf 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import mean_squared_error, r2_score 
from tensorflow.keras.datasets import boston_housing 
# Step 1: Load Boston housing dataset 
(x_train, y_train), (x_test, y_test) = boston_housing.load_data() 
# Step 2: Normalize the features 
scaler = StandardScaler() 
x_train = scaler.fit_transform(x_train) 
x_test = scaler.transform(x_test) 
# Step 3: Build the DNN model 
model = Sequential() 
model.add(Dense(64, input_dim=x_train.shape[1], activation='relu')) 
model.add(Dense(32, activation='relu')) 
model.add(Dense(1))  # Regression output 
model.compile(optimizer='adam', loss='mse') 
# Step 4: Train the model 
model.fit(x_train, y_train, epochs=100, batch_size=16, verbose=0) 
# Step 5: Predict and evaluate 
y_pred = model.predict(x_test) 
mse = mean_squared_error(y_test, y_pred) 
r2 = r2_score(y_test, y_pred) 
print("Predicted prices (first 5):", np.round(y_pred[:5].flatten(), 2)) 
print("Actual prices    (first 5):", y_test[:5]) 
print("Mean Squared Error:", round(mse, 2)) 
print("R² Score (Accuracy):", round(r2 * 100, 2), "%")""")

    elif(num == 5):
        print("""import tensorflow as tf 
from tensorflow import keras 
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Flatten, Conv2D 
import numpy as np 
from sklearn.metrics import accuracy_score 
import logging 
tf.get_logger().setLevel(logging.ERROR) 
EPOCHS = 7 
BATCH_SIZE = 32 
# Load MNIST dataset 
mnist_dataset = keras.datasets.mnist 
(train_images, train_labels), (test_images, test_labels) = mnist_dataset.load_data() 
# Reshape to add channel dimension (MNIST is grayscale) 
train_images = train_images.reshape((-1, 28, 28, 1)) 
test_images = test_images.reshape((-1, 28, 28, 1)) 
# Normalize data 
mean = np.mean(train_images) 
stddev = np.std(train_images) 
train_images = (train_images - mean) / stddev 
test_images = (test_images - mean) / stddev 
print('mean: ', mean) 
print('stddev: ', stddev) 
# One-hot encode labels 
train_labels = to_categorical(train_labels, num_classes=10) 
test_labels = to_categorical(test_labels, num_classes=10) 
# Build CNN model 
model = Sequential() 
model.add(Conv2D(64, (5, 5), strides=(2, 2), activation='relu', padding='same', 
input_shape=(28, 28, 1), kernel_initializer='he_normal', bias_initializer='zeros')) 
model.add(Conv2D(64, (3, 3), strides=(2, 2), activation='relu', padding='same', 
kernel_initializer='he_normal', bias_initializer='zeros')) 
model.add(Flatten()) 
model.add(Dense(10, activation='softmax', 
kernel_initializer='glorot_uniform', bias_initializer='zeros')) 
# Compile model 
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) 
model.summary() 
# Train model 
history = model.fit(train_images, train_labels, 
validation_data=(test_images, test_labels), 
epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=2, shuffle=True) 
# Predict 
predictions = model.predict(test_images) 
predicted_classes = np.argmax(predictions, axis=1) 
actual_classes = np.argmax(test_labels, axis=1) 
# Show first 10 predictions 
for i in range(10): 
print(f"Image {i+1}: Predicted = {predicted_classes[i]}, Actual = {actual_classes[i]}") 
# Accuracy 
accuracy = accuracy_score(actual_classes, predicted_classes) 
print("Prediction Accuracy: {:.2f}%".format(accuracy * 100)) """)

    elif(num == 6):
        print("""import tensorflow as tf 
from tensorflow import keras 
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense 
from tensorflow.keras.layers import Flatten 
from tensorflow.keras.layers import Conv2D 
import numpy as np 
import logging 
tf.get_logger().setLevel(logging.ERROR) 
EPOCHS = 128 
BATCH_SIZE = 32 
cifar_dataset = keras.datasets.cifar10 
(train_images, train_labels), (test_images, 
test_labels) = cifar_dataset.load_data() 
mean = np.mean(train_images) 
stddev = np.std(train_images) 
train_images = (train_images - mean) / stddev 
test_images = (test_images - mean) / stddev 
print('mean: ', mean) 
print('stddev: ', stddev) 
train_labels = to_categorical(train_labels, 
num_classes=10) 
test_labels = to_categorical(test_labels, 
num_classes=10) 
model = Sequential() 
model.add(Conv2D(64, (5, 5), strides=(2,2),activation='relu', 
padding='same',input_shape=(32, 32, 
3),kernel_initializer='he_normal',bias_initializer='zeros')) 
model.add(Conv2D(64, (3, 3), strides=(2,2),activation='relu', 
padding='same',kernel_initializer='he_normal',bias_initializer='zeros')) 
model.add(Flatten()) 
model.add(Dense(10, 
activation='softmax',kernel_initializer='glorot_uniform',bias_initializer='zeros')) 
model.compile(loss='categorical_crossentropy',optimizer='adam', metrics =['accuracy']) 
model.summary() 
history = model.fit(train_images, train_labels, validation_data =(test_images, test_labels), 
epochs=7,batch_size=BATCH_SIZE, verbose=2, shuffle=True) 
import numpy as np 
# Predict class probabilities 
predictions = model.predict(test_images) 
# Convert probabilities to class labels 
predicted_classes = np.argmax(predictions, axis=1) 
# Convert one-hot encoded test labels back to integer labels 
actual_classes = np.argmax(test_labels, axis=1) 
# Show first 10 predictions vs actuals 
for i in range(10): 
print(f"Image {i+1}: Predicted = {predicted_classes[i]}, Actual = {actual_classes[i]}") 
from sklearn.metrics import accuracy_score 
accuracy = accuracy_score(actual_classes, predicted_classes) 
print("Prediction Accuracy: {:.2f}%".format(accuracy * 100)) """)

    elif(num == 7):
        print("""import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN
import logging

tf.get_logger().setLevel(logging.ERROR)

EPOCHS = 100
BATCH_SIZE = 16
TRAIN_TEST_SPLIT = 0.8
MIN = 12
FILE_NAME = '../data/book_store_sales.csv'

def readfile(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        next(file)
        data = [float(line.split(',')[1]) for line in file]
    return np.array(data, dtype=np.float32)

sales = readfile(FILE_NAME)
months = len(sales)
split = int(months * TRAIN_TEST_SPLIT)
train_sales = sales[:split]
test_sales = sales[split:]

mean = np.mean(train_sales)
stddev = np.std(train_sales)

train_sales_std = (train_sales - mean) / stddev
test_sales_std = (test_sales - mean) / stddev

train_months = len(train_sales_std)
train_X = np.zeros((train_months - MIN, MIN, 1))
train_y = np.zeros((train_months - MIN, 1))

for i in range(train_months - MIN):
    train_X[i, :, 0] = train_sales_std[i:i + MIN]
    train_y[i, 0] = train_sales_std[i + MIN]

test_months = len(test_sales_std)
test_X = np.zeros((test_months - MIN, MIN, 1))
test_y = np.zeros((test_months - MIN, 1))

for i in range(test_months - MIN):
    test_X[i, :, 0] = test_sales_std[i:i + MIN]
    test_y[i, 0] = test_sales_std[i + MIN]

model = Sequential()
model.add(SimpleRNN(128, activation='relu', input_shape=(MIN, 1)))
model.add(Dense(1, activation='linear'))

model.compile(
    loss='mean_squared_error',
    optimizer='adam',
    metrics=['mean_absolute_error']
)

model.summary()

history = model.fit(
    train_X, train_y,
    validation_data=(test_X, test_y),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    verbose=2,
    shuffle=True
)

test_output = test_sales_std[MIN:]
naive_prediction = test_sales_std[MIN - 1:-1]
naive_mse = np.mean(np.square(naive_prediction - test_output))
naive_mae = np.mean(np.abs(naive_prediction - test_output))

print('Naive baseline MSE:', naive_mse)
print('Naive baseline MAE:', naive_mae)

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.title('Training & Validation Loss')
plt.grid()
plt.show()
""")

    elif(num == 8):
        print("""import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import tensorflow as tf
import logging

EPOCHS = 32
BATCH_SIZE = 256
INPUT_FILE_NAME = '/content/sample.txt'
WINDOW_LENGTH = 40
WINDOW_STEP = 3

tf.get_logger().setLevel(logging.ERROR)

file = open(INPUT_FILE_NAME, 'r', encoding='utf-8')
text = file.read()
file.close()

text = text.lower()
text = text.replace('\n', ' ')
text = text.replace('  ', ' ')

unique_chars = list(set(text))
char_to_index = dict((ch, index) for index, ch in enumerate(unique_chars))
index_to_char = dict((index, ch) for index, ch in enumerate(unique_chars))
encoding_width = len(char_to_index)

fragments = []
targets = []
for i in range(0, len(text) - WINDOW_LENGTH, WINDOW_STEP):
    fragments.append(text[i: i + WINDOW_LENGTH])
    targets.append(text[i + WINDOW_LENGTH])

X = np.zeros((len(fragments), WINDOW_LENGTH, encoding_width))
y = np.zeros((len(fragments), encoding_width))
for i, fragment in enumerate(fragments):
    for j, char in enumerate(fragment):
        X[i, j, char_to_index[char]] = 1
    target_char = targets[i]
    y[i, char_to_index[target_char]] = 1

model = Sequential()
model.add(LSTM(128, return_sequences=True,
               dropout=0.2, recurrent_dropout=0.2,
               input_shape=(None, encoding_width)))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(encoding_width, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

history = model.fit(X, y,
                    validation_split=0.05,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    verbose=2,
                    shuffle=True)

input_seq = 'the body was found near the lake. it was co'
input_seq = input_seq[-40:]

assert len(input_seq) == WINDOW_LENGTH

input_tensor = np.zeros((1, WINDOW_LENGTH, encoding_width))
for t, char in enumerate(input_seq):
    if char in char_to_index:
        input_tensor[0, t, char_to_index[char]] = 1
    else:
        print(f"Warning: Character '{char}' not in vocabulary.")

pred = model.predict(input_tensor, verbose=0)
next_char_index = np.argmax(pred[0])
next_char = index_to_char[next_char_index]

print("Predicted next character:", next_char)
""")

    elif(num == 9):
        print("""import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import tensorflow as tf
import logging

EPOCHS = 32
BATCH_SIZE = 256
INPUT_FILE_NAME = '/content/sample.txt'
WINDOW_LENGTH = 40
WINDOW_STEP = 3

tf.get_logger().setLevel(logging.ERROR)

file = open(INPUT_FILE_NAME, 'r', encoding='utf-8')
text = file.read()
file.close()

text = text.lower()
text = text.replace('\n', ' ')
text = text.replace('  ', ' ')

unique_chars = list(set(text))
char_to_index = dict((ch, index) for index, ch in enumerate(unique_chars))
index_to_char = dict((index, ch) for index, ch in enumerate(unique_chars))
encoding_width = len(char_to_index)

fragments = []
targets = []
for i in range(0, len(text) - WINDOW_LENGTH, WINDOW_STEP):
    fragments.append(text[i: i + WINDOW_LENGTH])
    targets.append(text[i + WINDOW_LENGTH])

X = np.zeros((len(fragments), WINDOW_LENGTH, encoding_width))
y = np.zeros((len(fragments), encoding_width))
for i, fragment in enumerate(fragments):
    for j, char in enumerate(fragment):
        X[i, j, char_to_index[char]] = 1
    target_char = targets[i]
    y[i, char_to_index[target_char]] = 1

model = Sequential()
model.add(LSTM(128, return_sequences=True,
               dropout=0.2, recurrent_dropout=0.2,
               input_shape=(None, encoding_width)))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(encoding_width, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

history = model.fit(X, y,
                    validation_split=0.05,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    verbose=2,
                    shuffle=True)

input_seq = 'the body was found near the lake. it was co'
input_seq = input_seq[-40:]

assert len(input_seq) == WINDOW_LENGTH

input_tensor = np.zeros((1, WINDOW_LENGTH, encoding_width))
for t, char in enumerate(input_seq):
    if char in char_to_index:
        input_tensor[0, t, char_to_index[char]] = 1
    else:
        print(f"Warning: Character '{char}' not in vocabulary.")

pred = model.predict(input_tensor, verbose=0)
next_char_index = np.argmax(pred[0])
next_char = index_to_char[next_char_index]

print("Predicted next character:", next_char)
""")

    elif(num == 10):
        print("""import tensorflow as tf 
from tensorflow.keras.datasets import mnist 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Flatten, Dense 
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.optimizers import Adagrad, Adam, Adadelta 
import matplotlib.pyplot as plt 
# Load and preprocess MNIST dataset 
(x_train, y_train), (x_test, y_test) = mnist.load_data() 
x_train = x_train.astype('float32') / 255.0 
x_test  = x_test.astype('float32') / 255.0 
y_train = to_categorical(y_train, 10) 
y_test  = to_categorical(y_test, 10) 
# Define scenarios 
scenarios = [ 
{"activation": "sigmoid", "epochs": 24, "val_split": 0.3, "optimizer": 
Adagrad(learning_rate=0.001)}, 
{"activation": "relu",    "epochs": 25, "val_split": 0.2, "optimizer": 
Adam(learning_rate=0.001)}, 
{"activation": "tanh",    "epochs": 21, "val_split": 0.1, "optimizer": 
Adadelta(learning_rate=0.001)}, 
{"activation": "sigmoid", "epochs": 23, "val_split": 0.2, "optimizer": 
Adam(learning_rate=0.001)} 
] 
# To store history of all models 
histories = [] 
# Train model for each scenario 
for i, config in enumerate(scenarios, start=1): 
print(f"\nTraining Scenario {i} with activation={config['activation']}, 
epochs={config['epochs']}, val_split={config['val_split']}") 
model = Sequential([ 
Flatten(input_shape=(28, 28)), 
Dense(128, activation=config['activation']), 
Dense(64, activation=config['activation']), 
Dense(10, activation='softmax') 
]) 
model.compile(optimizer=config['optimizer'], 
loss='categorical_crossentropy', 
metrics=['accuracy']) 
history = model.fit(x_train, y_train, 
epochs=config['epochs'], 
validation_split=config['val_split'], 
verbose=0) 
histories.append((f"Scenario {i}", history)) 
# Plot training vs validation accuracy 
plt.figure(figsize=(12, 6)) 
for name, history in histories: 
plt.plot(history.history['val_accuracy'], label=f'{name} - Val Acc') 
plt.plot(history.history['accuracy'], linestyle='dashed', label=f'{name} - Train Acc') 
plt.title('Training vs Validation Accuracy for all Scenarios') 
plt.xlabel('Epochs') 
plt.ylabel('Accuracy') 
plt.legend() 
plt.grid(True) 
plt.tight_layout() 
plt.show()""")
