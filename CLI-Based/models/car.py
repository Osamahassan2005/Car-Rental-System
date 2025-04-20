import pandas as pd
import os
class Car:
    #class attribute
    cars_file='data/cars.json'
    #instant attribute
    def __init__(self,car_id,brand,model,seating_capacity,price_per_day,available=True):
        self.car_id=car_id
        self.brand=brand
        self.model=model
        self.seating_capacity=seating_capacity
        self.price_per_day=price_per_day
        self.available=available
    # staticmethod is a
    @staticmethod
    def load_cars():
        try:
        #check car file path exists
            if not os.path.exists(Car.cars_file) or os.stat(Car.cars_file).st_size==0:
                return pd.DataFrame(columns=['car_id','brand','model','seating_capacity','price_per_day','available'])
            #read car file
            cars=pd.read_json(Car.cars_file)
            if 'car_id' in cars.columns:
                cars['car_id']=cars['car_id'].astype(str)
                cars['available']=cars['available'].astype(bool)
            return cars
        except ValueError as e:
            print('Error loading cars:',e)
            return pd.DataFrame(columns=['car_id','brand','model','seating_capacity','price_per_day','available'])
    @staticmethod           
    def save_cars(cars_df):
        #dataframe convert into json
        cars_df.to_json(Car.cars_file,orient='records',indent=4)
    def add_car(self):
        cars=Car.load_cars()
        #check car id already exists or not
        if not cars.empty and self.car_id in cars['car_id'].values:
           print(f"Car with ID {self.car_id} already exists.")
           return
        #create new car
        new_car={'car_id':self.car_id,
                 'brand':self.brand,
                 'model':self.model,
                 'seating_capacity':self.seating_capacity,
                 'price_per_day':self.price_per_day,
                 'available':self.available
        }
        new_cars_df=pd.DataFrame([new_car])
        if cars.empty:
            cars=new_cars_df
        else:
            cars=pd.concat([cars,new_cars_df],ignore_index=True)
        cars['car_id']=cars['car_id'].astype(str)
        Car.save_cars(cars)
        print(f"Car {self.brand.upper()}-{self.model.upper()} added successfully!")
    @staticmethod
    def display_available_cars():
        #load cars from car file
        cars=Car.load_cars()
        #check which car is available for display
        print(cars[['car_id','available']])
        available_cars=cars[cars['available']==True]
        if not available_cars.empty:
            print('*'*70)
            print(available_cars.to_string(index=False))
            print('*'*70)
        else:
            print('No cars available in the system!')

# client test code 
#car1=Car(1,'toyota','corolla',5,100)
#car2=Car(4,'honda','alto',5,200)
# car2.add_car()
# Car.display_cars()
