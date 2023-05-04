# Statistics routines
import os
from nltk.metrics.distance import *
import sklearn.metrics
import numpy as np

error_diff_types = ["type", "len"]

def levenshtein_distance (origin, new):
    pass

# MAPE
# Compute Mean Absolute Percentage Error between two values
def mean_absolute_percentage_error(origin, new):
    return sklearn.metrics.mean_absolute_percentage_error(origin, new)*100.

# MSPE
# Compute Mean Squared Percentage Error between two values
def mean_squared_percentage_error(origin, new):
    return np.mean(np.square(((origin - new) / origin)), axis=0)*100.

# RMSPE
# Compute Root Mean Squared Percentage Error between two lists
# TODO
def root_mean_squared_percentage_error(origin, new):
    return np.sqrt(np.mean(np.square(((origin - new) / origin)), axis=0))*100.

# MSE  
# Compute Mean Squared Error between two values
def mean_squared_error(origin, new):
    return np.mean(np.square(origin - new), axis=0)

# RMSE
# Compute Root Mean Squared Error between two lists
# TODO
def root_mean_squared_error(origin, new):
    return np.sqrt(np.mean(np.square(origin - new), axis=0))



# Compute difference between two values
def delta (origin, new):
    return new - origin
        
        