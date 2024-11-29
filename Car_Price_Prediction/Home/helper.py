from urllib import request
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from django.contrib import messages



class GETDATA:

    def __init__(self):
        self.cars_data = pd.read_csv(r"D:\myProject\ML Project\Car_Price_Prediction\Data\Cardetails.csv")
        self.cars_data.drop(columns=["torque"], inplace=True)
        self.cars_data.dropna(inplace=True)
        self.cars_data.drop_duplicates(inplace=True)

        self.cars_data['name']=self.cars_data['name'].apply(self.get_first_string)
        self.cars_data['mileage']=self.cars_data['mileage'].apply(self.get_first_value)
        self.cars_data['max_power']=self.cars_data['max_power'].apply(self.get_first_value)
        self.cars_data['engine']=self.cars_data['engine'].apply(self.get_first_value)
        self.cars_data['seats']=self.cars_data['seats'].convert_dtypes(int)

    def get_first_string(self, first_string):
        return first_string.split(' ')[0].strip()

    def get_first_value(self,value):
        value = value.split(' ')[0]  
        value = value.strip()  
        if value == '':
            return 0
        return int(float(value))



    def get_cars_data(self):
        cars_data = self.cars_data

        context = {
            'car_brands': {idx + 1: brand for idx, brand in enumerate(cars_data['name'].unique())},
            'fuel_types': {1: 'Diesel', 2: 'Petrol', 3: 'LPG', 4: 'CNG'},
            'transmissions': {1: 'Manual', 2: 'Automatic'},
            'owners': {idx + 1: owner for idx, owner in enumerate(cars_data['owner'].unique())},
            'seller_types': {idx + 1: seller for idx, seller in enumerate(cars_data['seller_type'].unique())},
            'engines': {idx + 1: engine for idx, engine in enumerate(cars_data['engine'].unique())},
            'max_power': {idx + 1: power for idx, power in enumerate(cars_data['max_power'].unique())},
            'seats': {idx + 1: seat for idx, seat in enumerate(cars_data['seats'].unique())},
        }

        return context


    def get_prediction(self, input_data):
        
        cars_data = self.cars_data.copy()
        name_mapping = {name: idx + 1 for idx, name in enumerate(cars_data['name'].unique())}
        cars_data['name'] = cars_data['name'].map(name_mapping)
        cars_data['transmission'].replace({'Manual': 1, 'Automatic': 2}, inplace=True)
        cars_data['seller_type'].replace({'Individual': 1, 'Dealer': 2, 'Trustmark Dealer': 3}, inplace=True)
        cars_data['fuel'].replace({'Diesel': 1, 'Petrol': 2, 'LPG': 3, 'CNG': 4}, inplace=True)
        owner_mapping = {owner: idx + 1 for idx, owner in enumerate(cars_data['owner'].unique())}
        cars_data['owner'] = cars_data['owner'].map(owner_mapping)

        # Prepare features and target for training
        feature_columns = ['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats']
        X = cars_data[feature_columns]
        y = cars_data['selling_price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

        model = RandomForestRegressor()
        model.fit(X_train, y_train)

        input_row = pd.DataFrame([{
            'name': int(input_data['name']),
            'year': int(input_data['year']),
            'km_driven': float(input_data['km']),
            'fuel': int(input_data['fuel']),
            'seller_type': int(input_data['seller_type']),
            'transmission': int(input_data['transmission']),
            'owner': int(input_data['owner']),
            'mileage': float(input_data['mileage']),
            'engine': float(input_data['engine']),
            'max_power': float(input_data['max_power']),
            'seats': int(input_data['seats']),
        }], columns=feature_columns)

        prediction = model.predict(input_row)
        return {"prediction": prediction[0]}  
