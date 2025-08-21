import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pipeline_code.feature_combination import FeatureCombination
from pipeline_code.select_dtypes import numeric_selector, categorical_selector
from pipeline_code.transformed_target_regressor import log1p_func, expm1_func
from schema.input_data import InputData
from model.predict import predict_output, MODEL_VERSION, vr_pipeline
import pandas as pd


# new = pd.DataFrame({'Title':'Yandex 12pcs racket', 'Category':'Racket','SellerFeedbackPercentage':14,
#                     'SellerFeedbackScore':100, 'Condition':'Old', 'ShippingCostType':'Calculated', 'ShippingPrice':400,
#                     'MinEstimatedDeliveryDate': '2025-08-16T07:00:00.000Z',	'MaxEstimatedDeliveryDate': '2025-08-20T07:00:00.000Z',
#                      'ItemLocation':'US',  'AvailableCoupons':True, 'ItemOriginDate':'2024-08-20T03:13:29.000Z',	'ItemCreationDate':'2024-08-20T03:13:29.000Z',
#                     'TopRatedBuyingExperience':True,'PriorityListing':False, 'KeywordTrend':182.483871, 'AvgUserCountScore':97.64,	'AvgHomeScore':0.14, 'ProductVariation': False}, index=[0])

# print(vr_pipeline.predict(new))


app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to US based Ebay Tennis products price recommender system."}

@app.get("/about")
def about():
    return {"message":"This web application is designed to help sellers identify the market competitive price of the tennis products on Ebay marketplace. It is based on Ebay tennis products, Keywords trends of tennis related products and Average score of matches (events) on keywords from previous month."}

@app.get("/health")
def health_check():
    return {
        'status':'ok',
        'model_version':MODEL_VERSION,
        'model_loaded':vr_pipeline is not None
    }


@app.post("/predict")
def predict(data: InputData):
    final_data = data.model_dump(include=['Title', 'Category', 'SellerFeedbackPercentage', 'SellerFeedbackScore', 'Condition',
                                          'ShippingCostType', 'ShippingPrice', 'MinEstimatedDeliveryDate', 'MaxEstimatedDeliveryDate', 'ItemLocation',
                                           'AvailableCoupons', 'ItemOriginDate', 'ItemCreationDate', 'TopRatedBuyingExperience', 'PriorityListing',
                                             'KeywordTrend', 'AvgUserCountScore', 'AvgHomeScore', 'ProductVariation'])
    
    def get_competitive_price(prediction, category):
        deltas = {
            "racquet":0.95,
            "balls":0.95,
            "strings":0.97,
            "grips":0.97,
            "athletic shoes":0.98,
            "activewear pants":0.98,
            "activewear tops":0.98,
            "activewear jackets": 0.98,
            "acitvewear shorts": 0.98}
        
        delta = deltas.get(category.lower())
        if delta is not None:
            return (prediction * delta)
        else:
            return (prediction * 0.99)
    
    try:
        prediction = predict_output(final_data)
        return JSONResponse(status_code=200, content={'The predicted price is':f'$ {round(prediction, 2)}',
                            'Competitive Price of this product is':f'$ {round(get_competitive_price(prediction, final_data.get("Category")), 2)}'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error':str(e)})










