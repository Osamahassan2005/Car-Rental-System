import pandas as pd
import os
import streamlit as st
from models.account import Account

class RentalManager:
    '''RentalManager class for managing rental history in the car rental system.'''
    rental_history_file = Account.get_data_path('data/rental_history.json')

    def __init__(self, user_name):
        '''Initializes the RentalManager object with user_name.'''
        self.user_name = user_name

    @staticmethod
    def load_history():
        '''Loads the rental history from the JSON file.'''
        try:
            if not os.path.exists(RentalManager.rental_history_file):
                return pd.DataFrame(columns=['user_name', 'car_id', 'start_date', 'end_date', 'status', 'rent_amount', 'late_fee'])

            rental_history = pd.read_json(RentalManager.rental_history_file)
            if 'car_id' in rental_history.columns:
                rental_history['car_id'] = rental_history['car_id'].astype(str)
            return rental_history
        except ValueError as e:
            st.error(f"Error reading json file: {e}")
            return pd.DataFrame(columns=['user_name', 'car_id', 'start_date', 'end_date', 'status', 'rent_amount', 'late_fee'])

    def save_rental_history(self, rental_history):
        '''Saves the rental history to the JSON file.'''
        try:
            rental_history.to_json(RentalManager.rental_history_file, orient='records', indent=4)
        except Exception as e:
            st.error(f"Error while saving rental history: {e}")

    def add_rental_history(self, car_id, start_date, end_date, rent_amount,payment_method):
        '''Adds a new rental history entry for the user. If the user already has an active rental, it shows a warning.'''
        rental_history = self.load_history()

        matched = (
            (rental_history['user_name'] == self.user_name)
            & (rental_history['status'] == 'active')
            & (rental_history['car_id'].astype(str) == car_id)
        )

        if not rental_history.empty and matched.any():
            st.warning(f"User {self.user_name} already has an active rental for car ID {car_id}.")
            return

        new_rental_history = {
            'user_name': self.user_name,
            'car_id': car_id,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'active',
            'rent_amount': rent_amount,
            'late_fee': 0.0,
            'Payment Method': payment_method
        }

        new_rental_df = pd.DataFrame([new_rental_history])

        if rental_history.empty:
            rental_history = new_rental_df
        else:
            rental_history = pd.concat([rental_history, new_rental_df], ignore_index=True)

        rental_history['car_id'] = rental_history['car_id'].astype(str)
        self.save_rental_history(rental_history)
        #st.success(f"User {self.user_name}'s rental history updated successfully!")

    def view_rental_history(self):
        '''Displays the rental history for the user. If no history is found, it shows an info message.'''
        rental_history = self.load_history()

        if rental_history.empty:
            st.info("No rental history found!")
            return

        user_rental = rental_history[rental_history['user_name'] == self.user_name]

        if not user_rental.empty:
            st.dataframe(user_rental)
        else:
            st.info(f"Rental history not available for user {self.user_name}.")
