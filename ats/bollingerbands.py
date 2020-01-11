import numpy as np

def bbands_array(data, window_size=20, num_std_dev=2):

    if len(data) < window_size:
        # what to do?
        raise NotImplementedError
        
    middle = []
    upper = []
    lower = []
    for i in range(0,len(data)-window_size):
        window = np.array(data[i:i+window_size])
        middle.append(window.mean())
        std_dev = window.std()
        upper.append(middle + std_dev * num_std_dev)
        lower.append(middle - std_dev * num_std_dev)

    return upper, middle, lower

def bbands_last(data, window_size=20, num_std_dev=2):

    if len(data) < window_size:
        # what to do?
        raise NotImplementedError
        
    window = np.array(data[-window_size:])
    middle = window.mean()
    std_dev = window.std()
    upper = middle + std_dev * num_std_dev
    lower = middle - std_dev * num_std_dev

    return upper, middle, lower

# Compute the percent range.
# Upper or greater = 1.0
# Lower or lesser = 0.0
def bbands_percent(upper, lower, current):
    if current >= upper:
        return 1.0
    elif current <= lower:
        return 0.0
    
    return (current - lower) / (upper - lower)