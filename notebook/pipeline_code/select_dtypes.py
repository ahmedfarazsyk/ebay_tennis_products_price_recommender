def numeric_selector(X):
  return X.select_dtypes(include=[int, float]).columns.tolist()

def categorical_selector(X):
  return X.select_dtypes(include=object).columns.tolist()