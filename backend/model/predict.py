import pickle
import pandas as pd



with open('model/vr_pipeline.pkl', 'rb') as file:
    vr_pipeline = pickle.load(file)



MODEL_VERSION = '1.0.0'

def predict_output(final_data: dict):

    input_df = pd.DataFrame([final_data])

    prediction = vr_pipeline.predict(input_df)[0]

    return prediction