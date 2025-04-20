from models.car import Car
from models.admin import Admin
from models.customer import Customer

def admin_menu(admin):
    """Handles Admin operations"""
    print(f'\nHello, {admin.first_name.upper()}!')
    while True:
        print('='*45)
        print('''Admin Options:
              1) View Personal Info
              2) Add New Car
              3) Remove Car
              4) View Cars
              5) View Rental History
              6) View Customer's History
              7) Logout
        ''')
        print('='*45)
        choice = input('Enter your choice: ')
        if not choice.isdigit():
            print("Invalid input! Please enter a number.")
            continue
        choice= int(choice) 

        if choice == 1:
            print(admin)
        elif choice == 2:
            car_id=input('Enter unique carID : ')
            brand=input('Enter Brand of the car: ').lower()
            model=input('Enter Model of the car: ').lower()
            seating_capacity=input('Enter seating capacity for car: ')
            try:
                seating_capacity= int(seating_capacity)
            except ValueError:
                print("Invalid input! Please enter an integer or a float.")
                return
            price_per_day=input('Enter rent price of the car per day: ')
            try:
                price_per_day= float(price_per_day)
            except ValueError:
                print("Invalid input! Please enter an integer or a float.")
                return
            is_available = input("Car is Available? (true/false): ").strip().lower()
            # Convert to boolean
            if is_available == "true":      
               available = True
            elif is_available == "false":      
                available = False
            else:
              print("Invalid input! Defaulting to False.")
              available = False
            car=Car(car_id,brand,model,seating_capacity,price_per_day,available)
            car.add_car()
        elif choice == 3:
            # remove by operator overloading (subtract)
            car_id = input('Enter car ID to remove: ')
            try:
               admin - car_id
            except Exception as e:
                print('Error while removing car',e)
        elif choice == 4:
            Admin.display_cars()
        elif choice == 5:
            Admin.view_rentals_history()
        elif choice == 6:
            Admin.view_customers()
        elif choice == 7:
            print('Logout Successfully!')
            break
        else:
            print("Invalid choice! Please select 1 - 5.")

def customer_menu(customer):
    """Handles  operations"""
    print(f'\nHello, {customer.first_name.upper()}!')
    while True:
        print('='*45)
        print('''Customer Options:
              1) View Available Cars
              2) Rent Cars 
              3) Add balance
              4) View Rental History
              5) Return Car 
              6) View Personal Info
              7) Log Out  
        ''')
        print('='*45)
        select = input('Enter your choice: ')
        if not select.isdigit():
            print("Invalid input! Please enter a number.")
            continue
        select= int(select)
        if select == 1:
            Car.display_available_cars()
        elif select == 2:
            rent_car_id=input('Enter Car ID for Rent: ')
            start_date=input('Enter start date For rent in the format (YYYY-MM-DD): ')
            end_date=input('Enter end date For rent in the format (YYYY-MM-DD): ')
            customer.rent_car(rent_car_id,start_date,end_date)
        elif select ==3:
            amount=input('Enter amount to Add balance: ')
            try:
                amount= float(amount)
                customer + amount
            except ValueError:
                print("Invalid input! Please enter an integer or a float.")
            except Exception as e:
                print('Error while adding amount',e)
        elif select == 4:
            customer.view_rental_history()
        elif select == 5:            
            return_car_id = input('Enter Car ID that return: ')
            return_date=input('Enter return date in the format (YYY-MM-DD): ')
            customer.return_car(customer.user_name,return_car_id,return_date)
        elif select == 6:
            print(customer)
        elif select == 7:
            print("Log Out Succesfully!")
            break
        else:
            print("Invalid choice! Please select a number between 1 - 7.")

def main():
    """Main menu of the Online Shopping System"""
    while True:
        print('=' * 50)
        print('::: Welcome to the Online Car Rental System :::')
        print('=' * 50)
        print('''
              1) Create Account
              2) Admin LogIn
              3) Customer LogIn
              4) Exit
        ''')
        option = input("Select an option: ")
        if not option.isdigit():
            print("Invalid input! Please enter a number.")
            continue
        option= int(option)

        if option == 1:
            role=input('Enter your Role (admin/customer):').lower()
            user_name = input('Enter any Unique Username: ')
            password = input('Enter Your Password: ')
            first_name= input('Enter Your First Name: ').lower()
            last_name= input('Enter Your Last Name: ').lower()
            address= input('Enter Your Address: ')
            match role:
                case 'admin':
                    input_key=input('Enter Admin key: ')
                    if not Admin.verify_admin_key(input_key):
                        print("Invalid Admin key! Access denied.")
                        return
                    new_admin=Admin(user_name,password,first_name,last_name,role)
                    new_admin.save_admin()
                case 'customer':
                    balance= input('Enter Your total balance: ')
                    try:
                        balance= float(balance)
                    except ValueError:
                        print("Invalid input! Please enter an integer or a float.")
                        return
                    new_customer = Customer(user_name,password,first_name,last_name,address,balance,role)
                    new_customer.save_customer()
                case _:
                    print("Invalid role! please enter 'admin' or 'customer'.")
        
        elif option == 2:
            admin_name = input('Enter Username: ')
            admin_password = input('Enter user Password: ')
            admin=Admin.admin_login(admin_name,admin_password)
            if admin:
                admin_menu(admin)
            else:
                print('Please enter correct username and password.')
        elif option == 3:
            customer_name = input('Enter username: ')
            customer_password=input('Enter user password: ')
            customer=Customer.customer_login(customer_name,customer_password)
            if customer:
               customer_menu(customer)
        elif option == 4:
            print("\nGoodbye! Thank you for using our service.")
            break
        else:
            print("Invalid choice! Please choose a no between 1 - 4.")

#call like this to prevent auto run
if __name__=='__main__':
    main()
    
# created by @usama_hassan


