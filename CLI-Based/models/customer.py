#imports
import os
import pandas as pd
from models.car import Car
from models.rental import RentalManager
from models.account import Account
from models.payment import PaymentMethod
#child class inherit to base class (Account)
class Customer(Account):
    #class attribute
    customer_file='data/customers.json'
    #instant attributes
    def __init__(self,user_name,password,first_name,last_name,address,balance,role='customer'):
        super().__init__(role,user_name,password,first_name,last_name)
        self.balance=balance
        self.address=address
        self.rental_manager=RentalManager(user_name)
    #method override w
    def __str__(self):
        return F"{super().__str__()} Balance: {self.balance}\n Address: {self.address}\n{'-'*20}"
    @staticmethod
    def load_customer():
        try: 
        #check user file path
            if not os.path.exists(Customer.customer_file):
                return pd.DataFrame(columns=['role','user_name','password','first_name','last_name','address','balance'])
            #read user file 
            customer=pd.read_json(Customer.customer_file)
            return customer
        except ValueError as e:
            print('Error reading json file',e)
            return pd.DataFrame(columns=['role','user_name','password','first_name','last_name','address','balance'])
    def save_customer(self):
           #load user from user file
           customer=Customer.load_customer()
           #check username is in file
           if not customer.empty and self.user_name in customer['user_name'].values:
               print(f"Username {self.user_name} already exists.")
               return
           #create new user
           new_customer={'role':self.role,
                     'user_name':self.user_name,
                     'password': self.password,
                     'first_name':self.first_name,
                     'last_name':self.last_name,
                     'address':self.address,
                     'balance':self.balance
           }
           new_customer_df=pd.DataFrame([new_customer])
           customer=pd.concat([customer,new_customer_df],ignore_index=True)
           customer.to_json(Customer.customer_file,orient='records',indent=4)
           print(f"User {self.first_name.upper()}-{self.last_name.upper()} added successfully!")
    @staticmethod
    def customer_login(user_name,password):
        data=Customer.load_customer()
        return Customer.login(data,user_name,password)
    def view_rental_history(self):
        self.rental_manager.view_rental_history()
    #operator averloading to add new balance amount
    def __add__(self,amount):
        if isinstance(amount,(int,float)):
            self.balance+=amount
            customer=Customer.load_customer()
            if self.user_name in customer['user_name'].values:
                customer.loc[customer['user_name']== self.user_name,'balance']=self.balance
                customer.to_json(Customer.customer_file,orient='records',indent=4)
                print(f'Balance Updated. New balance is {self.balance} .')
            else:
                print(f'ERROR: User {self.user_name} not found in file for update balance.')
        else:
            raise TypeError('Amount must be a number.')
    def rent_car(self,car_id,start_date,end_date):
        try:
            #load cars from car file
            cars=Car.load_cars()
            #check car id in car file
            if car_id not in cars['car_id'].values:
                print(f"car '{car_id}' is not available.")
                return
            car_row = cars[cars['car_id']==car_id].iloc[0]
            #check car is avilable
            if car_row['available']==False:
                print(f"Car '{car_id}' is currently not available.")
                return
            rental_days=(pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
            #check rental duration
            if rental_days<=0:
                print('Invalid rental duration.')
                return
            rent_amount=rental_days*car_row['price_per_day']
            #check balance is sufficient
            if self.balance<rent_amount:
                print(f"Insufficient balance.You need ${rent_amount} but have ${self.balance}.")
                return
            #payment
            payment=PaymentMethod(rent_amount,self.user_name)
            if payment.process_payment():
               #deduct and update
               new_balance=self.balance-rent_amount
               self.update_balance(new_balance)
               cars.loc[cars['car_id']==car_id,'available']=False
               Car.save_cars(cars)
               
               print(f"Car '{car_id}' succesfully rented for {rental_days} days, from {start_date} to {end_date}. Total rent: Rs-{rent_amount}.")
               #save details of rental car
               self.rental_manager.add_rental_history(car_id,start_date,end_date,rent_amount)
            else:
                print('Payment Failed! Car not Rented.')
        except Exception as e: 
            print(f'An error occured while processing the rental:',e)
    def return_car(self,user_name,car_id,return_date):
        car_id=str(car_id)
        #load  data
        rental_history=RentalManager.load_history()
        matched_data=rental_history[(rental_history['user_name'].astype(str) ==str(user_name))
                                     & (rental_history['car_id'].astype(str)==car_id)
                                     & (rental_history['status']=='active')]
        if matched_data.empty:
            print(f'No active rental found for carID {car_id} and  user {user_name}.')
            return
        active_rental=matched_data.iloc[0]
        expected_days=(pd.to_datetime(active_rental['end_date']) - pd.to_datetime(active_rental['start_date'])).days
        actual_days=(pd.to_datetime(return_date) - pd.to_datetime(active_rental['start_date'])).days                      
        extra_charges = 0
        if actual_days>expected_days:
            extra_charges=self.deduct_balance(user_name,car_id,actual_days,expected_days)
            self.update_status(rental_history,active_rental,extra_charges)
            self.mark_car_available(car_id)
            print(f'You Renturn car after {actual_days-expected_days} days so extra chrages has been deducted, RS-{extra_charges}.Thank you for using our service!')   
        else:
            self.update_status(rental_history,active_rental,extra_charges)
            self.mark_car_available(car_id)
            print('Car returned Succesfully.Thank you for using our service!')         
    def update_balance(self,balance):
        customer=Customer.load_customer()
        if self.user_name in customer['user_name'].values:
            customer.loc[customer['user_name']==self.user_name,'balance']=balance
            customer.to_json(Customer.customer_file,orient='records',indent=4)
            self.balance=balance
        else:
            print(f'ERROR: User {self.user_name} not found in file for update balance.')
    def deduct_balance(self,user_name,car_id,actual_days,expected_days):
        cars=Car.load_cars()
        car_match=cars[cars['car_id'] ==car_id]
        if car_match.empty:
            print(f'Car id {car_id} not found.')
            return
        car_row=car_match.iloc[0]
        extra_charges=int(car_row['price_per_day']*(actual_days-expected_days))
        if self.balance < extra_charges:
           st.warning(f"You do not have enough balance to pay late fee of Rs {extra_charges}. Please recharge your account.")
           return   # Or handle it differently
        self.balance -= extra_charges
        #update balance
        self.update_balance(self.balance)
        return extra_charges
    def update_status(self,rental_history,active_rental,extra_charges):
        conditions=(rental_history['user_name']==active_rental['user_name']) \
                     & (rental_history['car_id'].astype(str) ==active_rental['car_id'])
        rental_history.loc[conditions,'status']='returned'
        rental_history.loc[conditions,'late_fee']=extra_charges
        self.rental_manager.save_rental_history(rental_history)
    def mark_car_available(self,car_id):
        cars=Car.load_cars()
        cars.loc[cars['car_id'].astype(str) == car_id,'available']=True
        Car.save_cars(cars)

#client code for test
#user2=Customer('bob123','000','osama','hasan','karachi',50000)
#Customer.customer_login('bob123','000'))
# user1=User('bob123','xyz123','osama','hasan','karachi',50000)
#user2.save_user()
#user2.save_user()
#user2.rent_car(2,'2025-04-09','2025-04-10')
#user2.return_car('bob123',2,'2025-04-11')
# user1.show_info()
#print(user2)
