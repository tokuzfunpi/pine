import pickle

def read_pickle(file_name):
    data = None
    with open(file_name, 'r') as fd :
        data = pickle.load(fd)
    return data

def write_pickle(file_name, data):
    with open(file_name, 'w') as fd :
        pickle.dump(data, fd)
