import pandas as pd
from sklearn.preprocessing import StandardScaler

def process_data(data):
    # Preprocess data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data