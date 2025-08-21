import numpy as np

def log1p_func(y):
  return np.log1p(np.log1p(y))

def expm1_func(y):
  return np.expm1(np.expm1(y))