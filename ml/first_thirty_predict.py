import pandas as pd
import numpy as np
import os
from datetime import datetime
from dateutil import parser
import math

from keras import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras import optimizers

# TODO
data_dir = "/ml/data"
days = []
close = []
def read_all_data():
    global days
    global close
    for data_file in os.listdir(os.fsencode(data_dir)):
        #print ("Opening: ", data_file)
        bars = []
        four_pm_output = 0
        one_pm_output = 0
        with open(data_dir + "/" + os.fsdecode(data_file), mode="rt") as historical_data:
            # remove headers
            for line in historical_data:
                # { Date = 20141231  09:30:00, Open = 2080.96, Close = 2083.89, High = 2084.21, Low = 2080.96, Volume = 0, Count = 26, WAP = 0, Gaps = False }
                parts = line.split()
                #date = parser.parse(parts[3])
                #print (parts)
                #bars.append(date.weekday())

                if "09:30:00" in parts[4]:
                    bars.append(float(parts[7][:-1]))
                if len(bars) < 30:
                    #bars.append(float(parts[10][:-1]))
                    bars.append(float(parts[13][:-1]))
                    bars.append(float(parts[16][:-1]))

                elif "12:59:00" in parts[4]:
                    one_pm_output = float(parts[10][:-1])
                elif "15:59:00" in parts[4]:
                    four_pm_output = float(parts[10][:-1])

        if four_pm_output != 0:
            days.append(bars)   
            close_val = one_pm_output if four_pm_output == 0 else four_pm_output
            close.append(close_val)

def train():
    d_input = np.asarray(days[:-20])
    d_output = np.asarray(close[:-20])

    print("input",d_input.shape)
    print("output",d_output.shape)

    # normalize
    mu = d_input.mean()
    rng = (d_input.max() - d_input.min())
    d_input = (d_input - mu) / rng
    d_output = (d_output - mu) / rng
    # We build a sequential NN 
    model = Sequential()
    model.add(Dense(units=90, input_shape=(d_input.shape[1],), kernel_initializer="uniform", activation="relu"))
    # If we over fit, can regularize by dropping some samples
    #model.add(Dropout(0.1))
    #model.add(Dense(units=90, kernel_initializer="normal", activation="relu"))
    model.add(Dense(units=1, kernel_initializer="uniform"))
    

    # Stochastic gradient descent optimizer with some sensible defaults.
    #sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    #model.compile(loss='mean_squared_error',
    #            optimizer=sgd)

    model.compile(loss='mean_squared_error', optimizer='adam')
    # Uncomment this to view the model summary
    #model.summary()

    # Train the model.
    model.fit(d_input, d_output, epochs=5)
    model.summary()
    #results = model.evaluate(test_input_data, test_output_data)
    print ()
    #print ("Model evaluation results (loss, acc): " + str(results))

    #kfold = KFold(n_splits=10, random_state=seed)
    #results = cross_val_score(estimator, d_input, d_output, cv=kfold)
    #print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


    # prepare data
    test_x = days[-20:]
    test_x = (test_x - mu) / rng

    predicted_close = model.predict(np.asarray(test_x))
    corrected_close = predicted_close * rng + mu
    error = math.sqrt(sum((corrected_close - close[-20])**2))
    print("Prediction", predicted_close ,"translates to", corrected_close ,close[-20:])
    print("Error", error)

    print ()
    print ()
    c = close[-20:]
    err = 0
    print ("%10s %10s %10s" % ("Predicted", "Actual", "Diff"))
    for x in range(20):
        err += (c[x]-corrected_close[x][0])**2
        print("%10.2f %10.2f %10.2f" % (corrected_close[x][0], c[x], c[x]-corrected_close[x][0]))
    print ("err", math.sqrt(err))

if __name__ == "__main__":
    read_all_data()
    print(len(days),"days")

    train()