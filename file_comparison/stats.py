# Statistics routines
import os
from nltk.metrics import edit_distance
import sklearn.metrics
import numpy as np
# import nltk.metrics.distance

error_diff_types = ["type", "len"]

def core (origin, new):
    res = 0.
    try:
        res = (origin - new)/origin
    except ZeroDivisionError as e:
        if origin == 0. and origin == new:
            res = 0.
    return res

def vcore (origin, new):
    res = []
    n = min(len(origin), len(new))
    for iel in range(n):
        res.append(core(origin=origin[iel], new=new[iel]))
    return res

def mean_levenshtein_distance_percentage (origin, new):
    n = min(len(origin), len(new))
    lev_max_scores = []
    # Compute Levenshtein maximum scores
    for iel in range(n):
        lev_max_scores.append(max(len(str(origin[iel])), len(str(new[iel]))))

    distance_percentage = 0.
    for iel in range(n):
        distance_percentage += edit_distance(str(origin[iel]), str(new[iel]))*100./lev_max_scores[iel]
    mean_distance_percentage = distance_percentage / n

    return 100. - mean_distance_percentage

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
        
        