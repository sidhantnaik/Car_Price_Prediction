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

        self.cars_data['name'] = self.cars_data['name'].apply(self.get_first_string)
        self.cars_data['mileage'] = self.cars_data['mileage'].apply(self.get_first_value)
        self.cars_data['max_power'] = self.cars_data['max_power'].apply(self.get_first_value)
        self.cars_data['engine'] = self.cars_data['engine'].apply(self.get_first_value)


    def get_first_string(self, first_string):
        first_string = first_string.split(' ')[0]
        return first_string.strip(' ')

    def get_first_value(self, value):
        value = value.split(' ')[0]
        value = value.strip()
        if value == '':
            value = 0
        return float(value)
    
    


    def get_cars_data(self):
        cars_data = self.cars_data
        
        # Extract unique values for dropdowns
        car_brands = cars_data['name'].unique()
        fuel_types = cars_data['fuel'].unique()
        transmissions = cars_data['transmission'].unique()
        owners = cars_data['owner'].unique()
        engines = cars_data['engine'].unique()
        seller_type = cars_data['seller_type'].unique()
        max_power = cars_data['max_power'].unique()
        seats = cars_data['seats'].unique()


        context = {
            'car_brands': car_brands,
            'fuel_types': fuel_types,
            'transmissions': transmissions,
            'owners': owners,
            'engines': engines,
            'seller_type': seller_type,
            'max_power': max_power,
            'seats': seats,
        }

        return context

    def get_prediction(self, input_data):
        cars_data = self.cars_data

        arr = np.arange(1, 32)

        cars_data['name'].replace(cars_data['name'].unique(), arr, inplace=True)
        cars_data['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
        cars_data['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
        cars_data['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
        cars_data['owner'].replace(cars_data['owner'].unique(), [1, 2, 3, 4, 5], inplace=True)

        input_data = cars_data.drop(columns=['selling_price'])
        output_data = cars_data['selling_price']
        x_train, x_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2, random_state=2)

        model = RandomForestRegressor()
        model.fit(x_train, y_train)

        context = self.get_cars_data()
        result = model.predict(input_data)
        messages.success(request,"The predicted car price is : ",result)
        # context['prediction'] = result

        return context






# if request.method == "POST":
#             prediction=model.predict(xyz)
#             context['prediction']=prediction

# self.cars_data['name'].unique()      
#         self.cars_data['fuel'].unique()      
#         self.cars_data['transmission'].unique()
#         self.cars_data['owner'].unique()    
#         self.cars_data['engine'].unique()    
#         self.cars_data['seller_type'].unique()
#         self.cars_data['max_power'].unique()
#         self.cars_data['seats'].unique()