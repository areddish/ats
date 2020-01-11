from __future__ import print_function
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import time
import os
import datetime

LSTM1_SIZE = 26
LSTM2_SIZE = 121

INPUT_SIZE = 5
OUTPUT_SIZE = 1

window_size = 1 # 1 minutes

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=INPUT_SIZE, hidden_size=LSTM1_SIZE, num_layers=1)
        self.lstm2 = nn.LSTM(input_size=LSTM1_SIZE, hidden_size=LSTM2_SIZE, num_layers=1)
        self.linear = nn.Linear(in_features=LSTM2_SIZE, out_features=OUTPUT_SIZE)

    def forward(self, input):
        outputs = []
        hidden1 = (torch.rand(self.lstm1.num_layers, 1, LSTM1_SIZE, dtype=torch.double), torch.rand(self.lstm1.num_layers, 1, LSTM1_SIZE, dtype=torch.double))
        hidden2 = (torch.rand(self.lstm2.num_layers, 1, LSTM2_SIZE, dtype=torch.double), torch.rand(self.lstm2.num_layers, 1, LSTM2_SIZE, dtype=torch.double))

        for i, input_t in enumerate(input.chunk(input.size(1), dim=1)):
            out1, hidden1 = self.lstm1(input_t, hidden1)
            out2, hidden2 = self.lstm2(out1, hidden2)
            output = self.linear(out2)
            outputs += [output]

        outputs = torch.stack(outputs, OUTPUT_SIZE).squeeze(2)
        return outputs

def load_data():
    data = []
    early = 0
    for f in os.listdir("c:\\stock-data\\AAPL"):
        with open("c:\\stock-data\\AAPL\\"+f,"rt") as file:
            print ("Processing:", f)
            for l in file.readlines():
                parts = l.split(" ")
                date = int(parts[0])
                o = float(parts[1])
                h = float(parts[2])
                l = float(parts[3])
                c = float(parts[4])
                v = int(parts[5])
                bc = int(parts[6])
                dt = datetime.datetime.fromtimestamp(date)
                data.append([o,l,h,c,v])

        early += 1
        if (early > 0):
            return data
    return data

def build_target(data):
    rows = len(data)
    target = []
    for i in range(1,rows-window_size):
        # todo: update with window_size
        result = []
        for j in range(window_size):
            result.append(np.array([data[i-3+j][3]]))
        target.append(np.array(result))
    return target

def reshape_data(data):
    batches = []
    for si in range(1, len(data)-window_size):
        batches.append(np.array(data[si:si+window_size]))
    return batches

if __name__ == '__main__':
    # set random seed to 0
    np.random.seed(0)
    torch.manual_seed(0)

    # load data and make training set
    input_data = load_data()
    target_data = np.array(build_target(input_data))

    input_data = np.array(reshape_data(input_data))

    data_count = len(input_data)
    split = int(data_count * .95)

    # input_data = np.array(input_data, dtype=float)
    # target = np.array(target, dtype=float)
    
    input = torch.from_numpy(input_data[:split])
    target = torch.from_numpy(target_data[:split])
    test_input = torch.from_numpy(input_data[split:])
    test_target = torch.from_numpy(target_data[split:])

    # build the model
    seq = MyModel()
    seq.double()
    criterion = nn.MSELoss()
    # use LBFGS as optimizer since we can load the whole data to train
    optimizer = optim.LBFGS(seq.parameters(), lr=0.8)
    #begin to train
    for i in range(15):
        print('STEP: ', i)
        print(f"Input has {input.size(0)} rows with a window of {window_size} and {input.size(2)} features.")
        def closure():
            optimizer.zero_grad()
            out = seq(input)
            loss = criterion(out, target)
            print('loss:', loss.item())
            loss.backward()
            return loss
        optimizer.step(closure)
        # begin to predict, no need to track gradient here
        with torch.no_grad():
            pred = seq(test_input)
            loss = criterion(pred, test_target)
            print('test loss:', loss.item())
            y = pred.detach().numpy()

        # draw the result
        plt.figure(figsize=(30,10))
        plt.title('Predict future values for time sequences\n(Dashlines are predicted values)', fontsize=30)
        plt.xlabel('x', fontsize=20)
        plt.ylabel('y', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        def draw(yi, color):
            plt.plot(np.arange(input.size(0)), input[:,0,3].numpy(), color, linewidth = 2.0)
            plt.plot(np.arange(input.size(0))[-len(y):], yi[:,0,0], color + ':', linewidth = 2.0)
        draw(y, 'r')
        #time.sleep(30)
#        draw(y[1], 'g')
#        draw(y[2], 'b')
        plt.savefig('predict%d.pdf'%i)
        plt.show()
#        plt.close()
