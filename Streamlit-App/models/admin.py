import os
import json
import pandas as pd
import streamlit as st
from models.car import Car
from models.customer import Customer
from models.account import Account
from models.rental import RentalManager

class Admin(Account):
    admin_file = 'data/admins.json'

    def __init__(self, user_name, password, first_name, last_name, role='admin'):
        super().__init__(role, user_name, password, first_name, last_name)
        self.rental = RentalManager(None)

    def __str__(self):
        return f"{super().__str__()}"

    @staticmethod
    def verify_admin_key(input_key):
        try:
            with open("data/config.json", "r") as f:
                config = json.load(f)
                return input_key == config.get("admin_key")
        except Exception as e:
            st.error(f"Error while loading config file: {e}")

    @staticmethod
    def load_admin():
        try:
            if not os.path.exists(Admin.admin_file):
                return pd.DataFrame(columns=['role', 'user_name', 'password', 'first_name', 'last_name'])
            return pd.read_json(Admin.admin_file)
        except ValueError as e:
            st.error(f"Error reading JSON file: {e}")
            return pd.DataFrame(columns=['role', 'user_name', 'password', 'first_name', 'last_name'])

    def save_admin(self):
        admin = Admin.load_admin()
        if not admin.empty and self.user_name in admin['user_name'].values:
            st.warning(f"Username {self.user_name} already exists.")
            return
        new_admin = {
            'role': self.role,
            'user_name': self.user_name,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        new_admin_df = pd.DataFrame([new_admin])
        admin = pd.concat([admin, new_admin_df], ignore_index=True)
        admin.to_json(Admin.admin_file, orient='records', indent=4)
        st.success(f"Admin {self.first_name.upper()}-{self.last_name.upper()} added successfully!")

    @staticmethod
    def admin_login(user_name, password):
        data = Admin.load_admin()
        return Admin.login(data, user_name, password)

    def __sub__(self, car_id):
        cars = Car.load_cars()
        if cars.empty:
            st.warning('No cars available in the system.')
            return
        if car_id in cars['car_id'].values:
            cars = cars[cars['car_id'] != car_id]
            Car.save_cars(cars)
            st.success(f"Car with ID {car_id} removed successfully.")
        else:
            st.warning(f"No car found with ID {car_id}.")

    @staticmethod
    def display_cars():
        cars = Car.load_cars()
        if not cars.empty:
            st.image('Streamlit-App/image/allcars.jpg')
            st.dataframe(cars)
        else:
            st.info('No cars available!')

    @staticmethod
    def view_customers():
        customers = Customer.load_customer()
        if not customers.empty:
            st.dataframe(customers)
        else:
            st.info('No customers available!')

    @staticmethod
    def view_rentals_history():
        rental_history = RentalManager.load_history()
        if not rental_history.empty:
            st.dataframe(rental_history)
        else:
            st.info('No rental history available!')
