from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
import re
import pandas as pd



class FeatureCombination(BaseEstimator, TransformerMixin):
  def __init__(self):
    pass

  def fit(self, X, y=None):
    self.n_features_in_ = X.shape[1]
    self.feature_names_in_ = X.columns.tolist()
    return self

  def transform(self, X):
    check_is_fitted(self)
    assert(X.shape[1] == self.n_features_in_)
    X = X.copy()

    known_brands = {
    "adidas", "ASICS", "Ace The Moon", "ACEing Autism", "Alpha & RAB String", "Ame & Lulu",
    "Ashaway", "ASO", "Australian", "Australian Open", "Babolat", "Band-IT",
    "BB by Belen Berbel", "Bird & Vine", "Bjorn Borg", "BloqUV", "BlueFish Sport", "Blumaka",
    "BOAST", "Bolle", "Born To Rally", "BOSS", "Brooks", "Bubble", "Butterfly", "Cadence",
    "Cancha", "CoolNES", "Cortiglia", "Court Couture", "CourtLife", "Cross Court",
    "Denise Cronwall", "Diadem", "Diadora", "Doc & Glo", "DUC", "Dunlop", "Ektelon", "EleVen",
    "ellesse", "Fabletics", "Fairway", "Feetures", "Fila", "Fitsok", "Flow Society", "Forten",
    "FP Movement", "Gamma", "Geau Sport", "Genesis", "Glove It", "Goodr", "Gosen", "Grand Slam",
    "Grapplesnake", "Head", "HALO Hydration", "Hely Weber", "Hydro Flask", "Hydrogen", "IBKUL",
    "Incrediwear", "InPhorm", "Isospeed", "Jerdog", "Jofit", "Joma", "Joola", "Kirschbaum",
    "Klip", "Knockaround", "KSwiss", "Lacoste", "Lasso", "Le Coq Sportif", "Li Mi", "LIJA",
    "Lobster", "Lotto", "Lucky In Love", "Luxilon", "Maggie Mather", "Mizuno", "Mouratoglou Apparel",
    "MSV", "Nike", "New Balance", "Nick Kyrgios Foundation", "Nothing Major", "ON", "ON'RE",
    "Original Penguin", "OS1st", "Prince", "Penn", "PowerAngle", "Pro-Tec", "ProKennex",
    "ProSeries", "Puma", "Racquet Inc Gifts", "Rafa Nadal Academy", "REDVANLY", "Reebok", "Revo",
    "Roland Garros", "SaltStick", "SanSoleil", "Sergio Tacchini", "Signum-Pro", "Skechers",
    "Slazenger", "Slinger", "SmellWell", "Sofibella", "Solinco", "Spin It", "SSI - Sport Source International",
    "Sta Active", "Superfeet", "Surface", "Tail", "tasc", "Tecnifibre", "Tennis-Point",
    "Tennis Tutor", "Tennis Warehouse", "The Alabama Girl", "Thorlo", "Tifosi", "Topspin",
    "Toroline", "Tourna", "Travis Mathew", "Under Armour", "UomoSport", "VimHue", "Vitalyte",
    "Volkl", "Waterdrop", "Wilson", "Weiss CANNON", "Yonex", "Ytex", "Zamst", "2UNDR"
    }

    def extract_brand_model(title):
      title_lower = title.lower()
      found_brand = None
      for brand in known_brands:
        pattern = rf"(?i)(?<!\S){re.escape(brand)}(?!\S)"
        if re.search(pattern, title_lower):
          found_brand = brand
          break
      model = None
      if found_brand:
        remaining = title_lower.split(found_brand.lower(), 1)[1].strip()
        model_tokens = remaining.split()
        model = " ".join(model_tokens[:3]) if model_tokens else None
      return found_brand, model
    X['Brand'], X['Model'] = zip(*X['Title'].map(extract_brand_model))

    X['BrandModel'] = X['Brand'] + ' ' + X['Model']

    X['ProdFreq'] = X['BrandModel'].map(X['BrandModel'].value_counts())

    def categorize(prod_freq):
      if prod_freq > 10:
        return 'Best Seller'
      if prod_freq > 2:
        return 'Trending'
      else:
        return 'Normal'
    X['SellerCategory'] = X['ProdFreq'].apply(categorize)

    X['SellerFeedbackPercentageInv'] = max(X['SellerFeedbackPercentage'])+1 - X['SellerFeedbackPercentage']

    X['DeliveryLatency'] = (pd.to_datetime(X['MaxEstimatedDeliveryDate']) - pd.to_datetime(X['MinEstimatedDeliveryDate'])).dt.days

    X['ListingLatency'] = (pd.to_datetime(X['ItemCreationDate']) - pd.to_datetime(X['ItemOriginDate'])).dt.days

    X['OldProducts'] = X['ListingLatency'] > 0

    X['OriginToDelivery'] = (pd.to_datetime(X['MaxEstimatedDeliveryDate']) - pd.to_datetime(X['ItemOriginDate'])).dt.days

    X['WeightedSellerFeedback'] = X['SellerFeedbackPercentage'] * X['SellerFeedbackScore']

    X['Brand'].fillna('missing')
    X['ProdFreq'].fillna(0)

    #Remove unwanted Columns
    X.drop(columns = ['Title', 'MinEstimatedDeliveryDate', 'MaxEstimatedDeliveryDate',
                    'ItemOriginDate', 'ItemCreationDate', 'Model', 'BrandModel',
                      'SellerFeedbackPercentage'], inplace=True)

    self.n_features_out_ = X.shape[1]
    self.feature_names_out_ = X.columns.tolist()

    return X

  def get_feature_names_out(self, input_features=None):
    if input_features is None:
      if hasattr(self, "feature_names_out_"):
        return self.feature_names_out_

      else:
        return self.feature_names_in_

    if hasattr(self, "n_features_out_"):
      if (self.n_features_out_ == len(input_features)):
        return input_features
      else:
        return "Input feature size does not match the number of columns."

    else:
      if (self.n_features_in_ == len(input_features)):
        return input_features
      else:
        return "Input feature size does not match the number of columns."