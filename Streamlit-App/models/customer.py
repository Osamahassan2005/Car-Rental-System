import os
import pandas as pd
import streamlit as st
from models.car import Car
from models.rental import RentalManager
from models.account import Account
from models.payment import PaymentMethod

class Customer(Account):
    '''Customer class for managing customer accounts in the car rental system. Inherits from Account class.'''
    customer_file = 'data/customers.json'

    def __init__(self, user_name, password, first_name, last_name, address, balance, role='customer'):
        super().__init__(role, user_name, password, first_name, last_name)
        self.balance = balance
        self.address = address
        self.rental_manager = RentalManager(user_name)

    def __str__(self):
        '''Returns a string representation of the Customer object.'''
        return f"{super().__str__()} Balance: {self.balance}\n Address: {self.address}"

    @staticmethod
    def load_customer():
        '''Loads the customer data from the JSON file.'''
        try:
            if not os.path.exists(Customer.customer_file):
                return pd.DataFrame(columns=['role', 'user_name', 'password', 'first_name', 'last_name', 'address', 'balance'])
            customer = pd.read_json(Customer.customer_file)
            return customer
        except ValueError as e:
            st.error('Error reading json file: ' + str(e))
            return pd.DataFrame(columns=['role', 'user_name', 'password', 'first_name', 'last_name', 'address', 'balance'])

    def save_customer(self):
        '''Saves the customer data to the JSON file.'''
        customer = Customer.load_customer()
        if not customer.empty and self.user_name in customer['user_name'].values:
            st.error(f"Username {self.user_name} already exists.")
            return
        new_customer = {
            'role': self.role,
            'user_name': self.user_name,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'balance': self.balance
        }
        new_customer_df = pd.DataFrame([new_customer])
        customer = pd.concat([customer, new_customer_df], ignore_index=True)
        customer.to_json(Customer.customer_file, orient='records', indent=4)
        st.success(f"Customer {self.first_name.upper()}-{self.last_name.upper()} account created succesfully!.")

    @staticmethod
    def customer_login(user_name, password):
        data = Customer.load_customer()
        return Customer.login(data, user_name, password)

    def view_rental_history(self):
        self.rental_manager.view_rental_history()

    def __add__(self, amount):
        '''Adds the given amount to the customer's balance.'''
        if isinstance(amount, (int, float)):
            self.balance += amount
            customer = Customer.load_customer()
            if self.user_name in customer['user_name'].values:
                customer.loc[customer['user_name'] == self.user_name, 'balance'] = self.balance
                customer.to_json(Customer.customer_file, orient='records', indent=4)
                st.success(f'Balance Updated. New balance is {self.balance}.')
            else:
                st.error(f'ERROR: User {self.user_name} not found in file for updating balance.')
        else:
            raise TypeError('Amount must be a number.')
    def rent_car(self, car_id, start_date, end_date):
        '''Rents a car for the specified duration. If the car is not available, it shows a warning.'''
        try:
            #initialize the processing payment state
            st.session_state.processing_payment = True
            cars = Car.load_cars()
            # Check if the car ID is valid
            if car_id not in cars['car_id'].values:
                st.error(f"Car '{car_id}' is not valid.")
                return
            car_row = cars[cars['car_id'] == car_id].iloc[0]
            # Check if the car is available
            if car_row['available'] == False:
                st.info(f"Car '{car_id}' is currently not available.")
                return
            #rent amount calculation
            rental_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
            if rental_days <= 0:
                st.error('Invalid rental duration.')
                return
            #check if balance is sufficient
            rent_amount = rental_days * car_row['price_per_day']
            if self.balance < rent_amount:
                st.error(f"Insufficient balance. You need ${rent_amount} but have ${self.balance}.")
                return
            # Process payment
            payment=PaymentMethod(rent_amount,self.user_name)
            payment_success=payment.process_payment()
            # Check if payment was successful
            if payment_success:
                new_balance = self.balance - rent_amount
                self.update_balance(new_balance)
                cars.loc[cars['car_id'] == car_id, 'available'] = False
                Car.save_cars(cars)
                st.success('Payment Succesfull!, Your ride is booked.')
                st.subheader("Rental Details")
                st.markdown(f"""\n
                            **Days:** {rental_days}\n  
                            **Date:** from {start_date} to {end_date}\n  
                            **Total rent:** Rs-{rent_amount}\n  
                            **Payment Method:** {payment.payment_method}\n 
                            **Payment Details:** {'.'.join(payment.details)}\n 
                            """)
                self.rental_manager.add_rental_history(car_id, start_date, end_date, rent_amount,payment.payment_method)
                #mark processing payment as false
                st.session_state.processing_payment = False
            else:
                st.warning('Please complete the payment to rent the car.')
        except Exception as e:
            st.error(f'Error occured during rent car: {e}')

    def return_car(self, user_name, car_id, return_date):
        '''Returns a rented car. If the car is not found or the return date is invalid, it shows an error.'''
        car_id = str(car_id)
        rental_history = RentalManager.load_history()
        matched_data = rental_history[(rental_history['user_name'].astype(str) == str(user_name)) & 
                                      (rental_history['car_id'].astype(str) == car_id) & 
                                      (rental_history['status'] == 'active')]
        if matched_data.empty:
            st.error(f'No active rental found for carID {car_id} and user {user_name}.')
            return
        active_rental = matched_data.iloc[0]
        # Check if the return date is valid
        expected_days = (pd.to_datetime(active_rental['end_date']) - pd.to_datetime(active_rental['start_date'])).days
        actual_days = (pd.to_datetime(return_date) - pd.to_datetime(active_rental['start_date'])).days
        extra_charges = 0
        if actual_days > expected_days:
            extra_charges = self.deduct_balance(user_name, car_id, actual_days, expected_days)
            self.update_status(rental_history, active_rental, extra_charges)
            self.mark_car_available(car_id)
            st.success(f'Late Returned Notice: You were {actual_days - expected_days} days late, RS{extra_charges} Fee Applied.')
        else:
            self.update_status(rental_history, active_rental, extra_charges)
            self.mark_car_available(car_id)
            st.success('Return Completed. Thank you for using our service!')

    def update_balance(self, balance):
        '''Updates the customer's balance in the JSON file.'''
        customer = Customer.load_customer()
        if self.user_name in customer['user_name'].values:
            customer.loc[customer['user_name'] == self.user_name, 'balance'] = balance
            customer.to_json(Customer.customer_file, orient='records', indent=4)
            self.balance = balance
        else:
            st.error(f'ERROR: User {self.user_name} not found in file for updating balance.')

    def deduct_balance(self, user_name, car_id, actual_days, expected_days):
        '''Deducts the extra charges from the customer's balance if the car is returned late.'''
        cars = Car.load_cars()
        car_match = cars[cars['car_id'] == car_id]
        if car_match.empty:
            st.error(f'Car id {car_id} not found.')
            return
        car_row = car_match.iloc[0]
        extra_charges = int(car_row['price_per_day'] * (actual_days - expected_days))
        self.balance -= extra_charges
        self.update_balance(self.balance)
        return extra_charges

    def update_status(self, rental_history, active_rental, extra_charges):
        '''Updates the rental status to 'returned' and applies any extra charges.'''
        conditions = (
            (rental_history['user_name'] == active_rental['user_name']) & 
            (rental_history['car_id'].astype(str) == active_rental['car_id']) &
            (rental_history['status'] =='active')
        )
        if not conditions.any():
            st.error('Mathing rental record not found for updating status.')
        rental_history.loc[conditions, 'status'] = 'returned'
        rental_history.loc[conditions, 'late_fee'] = extra_charges
        self.rental_manager.save_rental_history(rental_history)

    def mark_car_available(self, car_id):
        '''Marks the car as available in the JSON file.'''
        cars = Car.load_cars()
        cars.loc[cars['car_id'].astype(str) == car_id, 'available'] = True
        Car.save_cars(cars)
