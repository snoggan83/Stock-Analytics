import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from matplotlib import pyplot as plt
import Getdata
import Loaddata

# Stock tag
tag = 'LargeCap'
# tag = 'MidCap'
# tag = 'SmallCap'
# tag = 'Commodities'
# tag = 'Index'

#  Running mode
mode = 'predict'

# Assigning stocks
stocktags = Getdata.load_stock_list(tag)

# Assigning data
datamat = Loaddata.load(stocktags, tag)

if mode == 'predict':
    for stockname in stocktags.keys():

        # Defining dataframe stock
        stock = datamat[stockname]

        # Set X and y
        X = stock
        for col in ["Close", "Dates", "Open"]:
            X = X.drop(col, axis=1)
        X.dropna()
        y = stock["Close"]
        # if not y.isnull().any() and

        # --- Data Pre-Processing ---

        # Split dataset into training and testing datasets
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # Scale data with StandardScaler
        scaler = StandardScaler()

        # Fit scaler
        scaler.fit(X_train)

        # Transform with scaler
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        # --- Train the model ---

        # Define hyper parameters of the neural network
        nn = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=10000, learning_rate_init=.1, verbose=100,
                            solver="sgd")

        # Fit the neural network
        nn.fit(X_train, y_train)

        # --- Predictions and evaluations ---

        # Prediction outcome using test set
        predictions = mlp.predict(X_test)
        plt.plot(range(len(predictions)), predictions)
        # plt.plot(range(len(y_test)), y_test)
        plt.show()