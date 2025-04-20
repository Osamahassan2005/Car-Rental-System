import pandas as pd
import os
#RentalManager composed to customer
class RentalManager:
    rental_history_file='data/rental_history.json'
    def __init__(self,user_name):
        self.user_name=user_name
    @staticmethod
    def load_history():
        try: 
        #check rebtal history file path
            if not os.path.exists(RentalManager.rental_history_file):
               return pd.DataFrame(columns=['user_name','car_id','start_date','end_date','status','rent_amount','late_fee'])
            #read user file 
            rental_history=pd.read_json(RentalManager.rental_history_file)
            if 'car_id' in rental_history.columns:
                rental_history['car_id']=rental_history['car_id'].astype(str)
            return rental_history
        except ValueError as e:
             print('Error reading json file',e)
             return pd.DataFrame(columns=['user_name','car_id','start_date','end_date','status','rent_amount','late_fee'])
    def save_rental_history(self,rental_history):
        try:
            rental_history.to_json(RentalManager.rental_history_file,orient='records',indent=4)
        except Exception as e:
            print('ERROR while saving rental history',e)
    def add_rental_history(self,car_id,start_date,end_date,rent_amount):
           #load user from user file
           rental_history=self.load_history()
           #check username is in file
           matched=((rental_history['user_name'] == self.user_name)
                                            & (rental_history['status']=='active') 
                                            & (rental_history['car_id'].astype(str)==car_id))
           if not rental_history.empty and matched.any():
               print(f"User {self.user_name} had an active rental.")
               return
           #new rental history
           new_rental_history={'user_name':self.user_name,
                               'car_id':car_id,
                               'start_date':start_date,
                               'end_date':end_date,
                               'status':'active',
                               'rent_amount':rent_amount,
                               'late_fee':0.0
                               }
           new_rental_df=pd.DataFrame([new_rental_history])
           if rental_history.empty:
              rental_history=new_rental_df
           else:
               rental_history=pd.concat([rental_history,new_rental_df],ignore_index=True)
           rental_history['car_id']=rental_history['car_id'].astype(str)
           self.save_rental_history(rental_history)
           print(f"User {self.user_name} history updated successfully!")
    def view_rental_history(self):
        #load rental history from the file
        rental_history=self.load_history()
        if rental_history.empty:
            print('No Rental history Found!')
            return
        user_rental=rental_history[rental_history['user_name']==self.user_name]
        if not user_rental.empty:
           print('*'*70)
           print(user_rental.to_string(index=False))
           print('*'*70)
        else:
            print(f'User {self.user_name} history not Available.')
#clent code for test
# r=Rental(['usama','1','2025-04-07','2025-04-10','10'],'no','yes',0)
# r.save_reantal_history()
