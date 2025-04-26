import pandas as pd
import os
import streamlit as st
from models.account import Account
class Car:
    '''Car class for managing car rental system. It includes methods to load, save, and add cars.'''
    cars_file = Account.get_data_path('data/cars.json')

    def __init__(self, car_id, brand, model, seating_capacity, price_per_day, available=True):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.seating_capacity = seating_capacity
        self.price_per_day = price_per_day
        self.available = available

    @staticmethod
    def load_cars():
        '''Loads the car data from the JSON file.'''
        try:
            if not os.path.exists(Car.cars_file) or os.stat(Car.cars_file).st_size == 0:
                return pd.DataFrame(columns=['car_id', 'brand', 'model', 'seating_capacity', 'price_per_day', 'available'])

            cars = pd.read_json(Car.cars_file)
            if 'car_id' in cars.columns:
                cars['car_id'] = cars['car_id'].astype(str)
                cars['available'] = cars['available'].astype(bool)
            return cars
        except ValueError as e:
            st.error(f'Error loading cars: {e}')
            return pd.DataFrame(columns=['car_id', 'brand', 'model', 'seating_capacity', 'price_per_day', 'available'])

    @staticmethod
    def save_cars(cars_df):
        '''Saves the car data to the JSON file.'''
        cars_df.to_json(Car.cars_file, orient='records', indent=4)

    def add_car(self):
        '''Adds a new car to the system. If the car already exists, it shows a warning.'''
        cars = Car.load_cars()
        if not cars.empty and self.car_id in cars['car_id'].values:
            st.warning(f"Car with ID {self.car_id} already exists.")
            return
        new_car = {
            'car_id': self.car_id,
            'brand': self.brand,
            'model': self.model,
            'seating_capacity': self.seating_capacity,
            'price_per_day': self.price_per_day,
            'available': self.available
        }

        new_cars_df = pd.DataFrame([new_car])

        if cars.empty:
            cars = new_cars_df
        else:
            cars = pd.concat([cars, new_cars_df], ignore_index=True)

        cars['car_id'] = cars['car_id'].astype(str)
        Car.save_cars(cars)

        st.success(f"Car {self.brand.upper()}-{self.model.upper()} added successfully!")

    @staticmethod
    def display_available_cars():
        '''Displays the available cars in the system. If no cars are available, it shows an info message.'''
        cars = Car.load_cars()
        available_cars = cars[cars['available'] == True]
        if not available_cars.empty:
                st.dataframe(available_cars.reset_index(drop=True))
        else:
            st.info("No cars available in the system!")
