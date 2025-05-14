def dlans(num):
    if(num == 1):
        print("""
        import numpy as np 
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
          print(f'{input_val}->{prediction[0]:.4f}')
""")

    elif(num == 2):
        print("""import tensorflow 
        from tensorflow import keras 
        from tensorflow.keras import Sequential 
        from tensorflow.keras.layers import Dense,Flatten 
        
        (X_train,y_train),(X_test,y_test)=keras.datasets.mnist.load_data() 
        X_train.shape 
        X_test.shape 
        y_train.shape 
        y_test.shape 
        y_train 
        
        X_test=X_test/255 
        X_train=X_train/255 
        X_train[2] 
        
        model=Sequential() 
        model.add(Flatten(input_shape=(28,28))) 
        model.add(Dense(128,activation='relu')) 
        model.add(Dense(32,activation='relu')) 
        model.add(Dense(10,activation='softmax')) 
        
        model.compile(loss='sparse_categorical_crossentropy',optimizer='Adam',metrics=['accuracy']) 
        history=model.fit(X_train,y_train,validation_split=0.2,epochs=25) 
        
        y_prob=model.predict(X_test) 
        y_pred=y_prob.argmax(axis=1) 
        
        from sklearn.metrics import accuracy_score 
        accuracy_score(y_pred,y_test) 
        
        import matplotlib.pyplot as plt 
        plt.plot(history.history['loss']) 
        plt.plot(history.history['val_loss']) 
        plt.plot(history.history['accuracy']) 
        plt.plot(history.history['val_accuracy']) 
        plt.imshow(X_test[1]) 
        
        model.predict(X_test[1].reshape(1,28,28)).argmax(axis=1) 
""")

    elif(num==3):
        print("""import numpy as np 
        import tensorflow as tf 
        from tensorflow import keras 
        from tensorflow.keras.layers import Dense 
        from tensorflow.keras import Sequential 
        import logging 
        tf.get_logger().setLevel(logging.ERROR) 
        
        EPOCHS=500
        BATCH_SIZE=16 
        
        (x_raw_train,y_train),(x_raw_test,y_test)=keras.datasets.boston_housing.load_data() 
        
        from tensorflow.keras.layers import Input 
        
        model=Sequential() 
        model.add(Dense(64,activation='relu',input_shape=[13])) 
        model.add(Dense(64,activation='relu')) 
        model.add(Dense(1,activation='linear')) 
        model.compile(loss='mean_squared_error',optimizer='adam',metrics=['mean_absolute_error']) 
        
        model.summary() 
        
        history = model.fit(x_raw_train, y_train, validation_data=(x_raw_test, y_test), epochs=EPOCHS, 
        batch_size=BATCH_SIZE, verbose=2, shuffle=True) 
        predictions=model.predict(x_raw_test) 
        
        for i in range(0,4): 
          print('prediction:', predictions[i],', true value',y_test[i]) 
""")

    elif(num==4):
        print("""import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras.utils import to_categorical
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
        from tensorflow.keras.optimizers import Adam
        import numpy as np
        
        import logging
        tf.get_logger().setLevel(logging.ERROR)
        
        cifar_dataset = keras.datasets.cifar10
        (train_images, train_labels), (test_images, test_labels) = cifar_dataset.load_data()
        mean = np.mean(train_images)
        stddev = np.std(train_images)
        train_images = (train_images - mean) / stddev
        test_images = (test_images - mean) / stddev
        train_labels = to_categorical(train_labels, num_classes=10)
        test_labels = to_categorical(test_labels, num_classes=10)
        
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dropout(0.4))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(10, activation='softmax'))
        model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        
        history = model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=10, batch_size=32, verbose=2, shuffle=True)
        
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
        print(f"Final Test Accuracy: {test_accuracy * 100:.2f}%")
""")

    elif(num==5):
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

    elif(num==6):
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
        model.add(LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2, input_shape=(None, encoding_width)))
        model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
        model.add(Dense(encoding_width, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        model.summary()
        
        history = model.fit(X, y, validation_split=0.05, batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=2, shuffle=True)
        
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