import pandas as pd

ebay_list_data = pd.read_csv('ebay_data/ebay_list_data.csv')

category_list = ebay_list_data['Category'].unique()
category_list = category_list[~pd.isna(category_list)]

condition_list = ebay_list_data['Condition'].unique()
condition_list = condition_list[~pd.isna(condition_list)]

shipping_cost_type_list = ebay_list_data['ShippingCostType'].unique()
shipping_cost_type_list = shipping_cost_type_list[~pd.isna(shipping_cost_type_list)]

item_location_list = ebay_list_data['ItemLocation'].unique()
item_location_list = item_location_list[~pd.isna(item_location_list)]
