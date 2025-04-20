import os
import json
import  pandas as pd
from models.car import Car
from models.customer import Customer
from models.account import Account
from models.rental import RentalManager
# ADMIN IS ACCOCIATED WITH CAR,CUSTOMER,RENTAL CLASSes BY USING THIER METHOD's
class Admin(Account):
    admin_file='data/admins.json'
    def __init__(self,user_name,password,first_name,last_name,role='admin'):
        super().__init__(role,user_name,password,first_name,last_name)
        self.rental=RentalManager(None)
    def __str__(self):
        return f"{super().__str__()} \n{'-'*20}"
    @staticmethod
    def verify_admin_key(input_key):
        try:
            with open("data/config.json","r") as f:
                config=json.load(f)
                return input_key == config.get("admin_key")
        except Exception as e:
            print("Error While loading Config file:",e)
    @staticmethod
    def load_admin():
        try: 
        #check admin file path
            if not os.path.exists(Admin.admin_file):
               return pd.DataFrame(columns=['role','user_name','password','first_name','last_name'])
            #read admin file 
            admin=pd.read_json(Admin.admin_file)
            return admin
        except ValueError as e:
            print('Error reading json file',e)
            return pd.DataFrame(columns=['role','user_name','password','first_name','last_name'])
    def save_admin(self):
           #load user from user file
           admin=Admin.load_admin()
           #check username is in file
           if not admin.empty and self.user_name in admin['user_name'].values:
               print(f"Username {self.user_name} already exists.")
               return
           #create new user
           new_admin={'role':self.role,
                     'user_name':self.user_name,
                     'password': self.password,
                     'first_name':self.first_name,
                     'last_name':self.last_name,
           }
           new_admin_df=pd.DataFrame([new_admin])
           admin=pd.concat([admin,new_admin_df],ignore_index=True)
           admin.to_json(Admin.admin_file,orient='records',indent=4)
           print(f"Admin {self.first_name.upper()}-{self.last_name.upper()} added successfully!")
    @staticmethod
    def admin_login(user_name,password):
        data=Admin.load_admin()
        return Admin.login(data,user_name,password)
    def __sub__(self,car_id):
        cars=Car.load_cars()
        if cars.empty:
            print('No cars Available in the system.')
            return 
        #check car id already exists or not
        if car_id in cars['car_id'].values:
           cars=cars[cars['car_id'] != car_id]
           Car.save_cars(cars)
           print(f"Car with ID {car_id} Removed succesfully.")
        else:
            print(f'No car found with ID {car_id}.')
    @staticmethod
    def display_cars():
        #load cars from car file
        cars=Car.load_cars()
        #check which car is available for display
        if not cars.empty:
            print('*'*70)
            print(cars.to_string(index=False))
            print('*'*70)
        else:
            print('No cars available!')    
    @staticmethod
    def view_customers():
        #load customer from the file
        customers=Customer.load_customer()
        if not customers.empty:
            print('*'*70)
            print(customers.to_string(index=False))
            print('*'*70)
        else:
            print('No customers available!')
    @staticmethod
    def view_rentals_history():
        #load rental history from the file
        rental_history=RentalManager.load_history()
        if not rental_history.empty:
            print('*'*70)
            print(rental_history.to_string(index=False))
            print('*'*70)
        else:
            print('No Rental history available!')

#client code        
#a=Admin('admin123','cs120','ali','hassan')
# a.save_admin()
# Admin.remove_car(1)
# Admin.display_cars()
# Admin.view_customer()
# Admin.view_rental_history()
#Admin.admin_login('admin123','cs120')
