from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated
from datetime import datetime
##
from data_code.trends import full_result
from data_code.sofascore import avg_user_count_dict, avg_home_score_dict
##
import re
import nltk
from nltk.stem import WordNetLemmatizer


nltk.download('stopwords')
from nltk.corpus import stopwords
eng_stopwords = set(stopwords.words('english'))
nltk.download('wordnet')
lem = WordNetLemmatizer()

class InputData(BaseModel):
    Title: Annotated[str, Field(..., description="Title of your product listed on the Ebay Marketplace.", examples=['YONEX 2022 Model REGNA 98 02RGN98/02RGN98C Tennis Racket Black Frame only  G2/G3'])]
    Category: Annotated[str, Field(...,  description="Category of your product.", examples=["Racquets"])]
    SellerFeedbackPercentage: Annotated[float, Field(..., ge=0, le=100, description="Your online shop feedback percentage.", examples=[100.0])]
    SellerFeedbackScore: Annotated[float, Field(..., ge=0, description="Your online shop feedback score.", examples=[665])]
    Condition: Annotated[str, Field(..., description="Condition of your product.", examples=["New"])]
    ShippingCostType: Annotated[str, Field(..., description="How you compute your shipping cost.", examples=["FIXED"])]
    ShippingPrice: Annotated[float, Field(..., gt=0, description="Shipping price in dollars.", examples=[30])]
    MinEstimatedDeliveryDate: Annotated[str, Field(..., description="Minimumly when will your product be delivered.", examples=["2025-08-15T07:00:00.000Z"])]
    MaxEstimatedDeliveryDate: Annotated[str, Field(..., description="Maximumly when will your product be delivered.", examples=["2025-08-19T07:00:00.000Z"])]
    ItemLocation: Annotated[str, Field(..., description="Where your product will be delivered.", examples=["US"])]
    AvailableCoupons: Annotated[bool, Field(..., description="Do you have available coupons for your product.", examples=[True, False])]
    ItemOriginDate: Annotated[str, Field(..., description="When did you received the stock of your product.", examples=["2025-08-14T01:39:00.000Z"])]
    ItemCreationDate: Annotated[str, Field(..., description="When did your product listed on the market place.", examples=["2025-08-14T01:39:00.000Z"])]
    TopRatedBuyingExperience: Annotated[bool, Field(..., description="Do you provide top rated buying experience.", examples=[True, False])]
    PriorityListing: Annotated[bool, Field(..., description="Is your product listed on priority.", examples=[True, False])]
    ProductVariation:Annotated[bool, Field(..., description="Do you have a variation / different version of your product.", examples=[True, False])]


    @field_validator("ShippingCostType")
    @classmethod
    def normalize_cost_type(cls, v: str) -> str:
      v = v.strip().capitalize()
      return v
    
    @field_validator("MinEstimatedDeliveryDate", "MaxEstimatedDeliveryDate", "ItemOriginDate", "ItemCreationDate")
    @classmethod
    def validate_iso8601_utc(cls, v:str)->str:
        try:
            if not v.endswith('Z'):
                raise ValueError("Datetime must end with Z for UTC")
            datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            raise ValueError("Datetime must be in ISO 8601 UTC format: YYYY-MM-DDTHH:MM:SS.sssZ")
        
        return v
    
    
    @computed_field
    @property
    def KeywordTrend(self)->float:
        def find_frequent_score(text):
          score = 0
          words = text.split()
          for w in words:
            if w in full_result['word'].tolist():
              word_score = full_result[full_result['word'] == w]['score'].iloc[0]
              score = score + word_score * words.count(w)
          return score
        
        combined = self.Title + ' ' + self.Category
        score = find_frequent_score(combined)
        return score


    @computed_field
    @property
    def AvgUserCountScore(self)->float:
       def find_user_count_score(text):
          score = 0
          for word in text:
            if word in avg_user_count_dict.keys():
              score = score + avg_user_count_dict[word]
          return score
       
       def clean_text(text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        words = [lem.lemmatize(word) for word in text.split() if word not in eng_stopwords and len(word) > 2]
        return words

       combined = self.Title + ' ' + self.Category
       result = clean_text(combined)
       avg_user_count_out = find_user_count_score(result)

       return avg_user_count_out
    

    @computed_field
    @property
    def AvgHomeScore(self)->float:
       def find_home_score(text):
          score = 0
          for word in text:
            if word in avg_home_score_dict.keys():
              score = score + avg_home_score_dict[word]
          return score
       
       def clean_text(text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        words = [lem.lemmatize(word) for word in text.split() if word not in eng_stopwords and len(word) > 2]
        return words
       
       combined = self.Title + ' ' + self.Category
       result = clean_text(combined)
       avg_home_score_out = find_home_score(result)

       return avg_home_score_out