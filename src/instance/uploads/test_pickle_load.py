import pickle

def load_data(file_path):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data

#Line	Issue
#1	Suspicious import detected: pickle
#5	Pattern detected: pickle load