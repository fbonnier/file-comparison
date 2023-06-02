# Statistics routines
import os
import nltk
import sklearn.metrics
import numpy as np
import nltk.metrics.distance

error_diff_types = ["type", "len"]

def mean_levenshtein_distance (origin, new):
    n = min(len(origin), len(new))
    value = 0.
    for iel in range(n):
        value += nltk.metrics.distance.edit_distance(origin[iel], new[iel])
    value = value / n

    return value*100

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
def root_mean_squared_percentage_error(origin, new):
    return np.sqrt(np.mean(np.square(((origin - new) / origin)), axis=0))*100.

# MSE  
# Compute Mean Squared Error between two lists
def mean_squared_error(origin, new):
    return np.mean(np.square(origin - new), axis=0)

# RMSE
# Compute Root Mean Squared Error between two lists
def root_mean_squared_error(origin, new):
    return np.sqrt(np.mean(np.square(origin - new), axis=0))

# MPE
# Compute Mean Percentage Error between two lists
def mean_percentage_error(origin, new):
    n = min(len(origin), len(new))
    core_value = 0.
    for icore in range (n):
        core_value += (origin[icore] - new[icore])/origin[icore]
    core_value = core_value/n

    return core_value * 100.

# MRPD
# Compute Mean Relative Percentage Difference between two lists
def mean_relative_percentage_difference(origin, new):
    n = min(len(origin), len(new))
    core_value = 0.
    for icore in range (n):
        core_value += abs((origin[icore] - new[icore])) / ((origin[icore] + new[icore])/2)
    core_value = abs(core_value)/n

    return core_value * 100.


# Compute difference between two values
# TODO
def delta (origin, new):
    return new - origin
        
        