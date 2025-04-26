#import necessary libraries or modules
import streamlit as st
import os
import time
from models.car import Car
from models.customer import Customer
from models.admin import Admin 

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "main_menu"
# apply custom CSS styles
st.markdown("""
    <style> 
            .stApp {
                color: #1a1a1a; /* dark gray */
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                text-align: left;
                padding: 0px;
                border-radius: 2px;
                margin: 0px;
                background-color: #fff
            } 
            .stApp header { 
                background-color: #fff;
                color: #ff6e00;
                padding: 10px;
                text-align: left;
                font-size: 24px;
                font-weight: bold; 
            }
            .stApp h1 {
                color:#1a1a1a; /* dark gray */
                font-family: 'Poppins',sans-serif;
                font-size: 46px;
                font-weight: bold;
                text-align: left;
            }
            .stApp h2, .stApp h3, .stApp h4 {
                color: #ff6e00; /* orange */
                font-size: 28px;
                font-weight: bold;
                text-align: left;
            }
            .stApp p {
                color: #333; /* dark gray */
                font-size: 18px;
                line-height: 1.5;
                text-align: left;
            }
            .stApp img {
                max-width: 100%;
                height: auto;
                border-radius: 10px;
                margin: 20px 0;
            }
            .stApp button {
                background-color: #ff6e00; /* orange */
                color: #fff; /* white */
                border: none;
                border-radius: 7px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }   
            .stApp button:hover {
                transition: background-color 0.3s ease;
                color: #fff; /* white */
                background-color: #e65c00; /* darker orange */
            }
            section[data-testid="stSidebar"] {
                background-color: #ff6e00; /* orange */
                color: #fff;
                padding: 20px;
                border-radius: 20px 140px;
                margin: 2px;
            }
            section[data-testid="stSidebar"] button {
                background-color: #fff; /* white */
                color: #ff6e00; /* orange */
                border: none;
                border-radius: 7px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            
            section[data-testid="stSidebar"] h2{
                color: #fff; /* white */
                font-size: 24px;
                font-weight: bold;
                text-align: left;
            }
            
            [data-testid="stSidebar"]
            [data-testid="stRadio"] label {
                color: #333; /* white */
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                padding: 5px;
            }
            
            input[type="text"],
            input[type="password"],
            input[type="date"],
            input[type="email"],
            input[type="url"],
            textarea {
                background-color: #fff; /* white */
                color: #333; /* dark gray */
                border: 2px solid #ff6e00;
                caret-color: #333; /* dark gray */
                border-radius: 5px;
                padding: 17px;
                font-size: 16px;
                width: 100%;
                outline: none;
                box-sizing: border-box;
                margin-bottom: 20px;
                transition: border-color 0.3s ease;
            }
            input[type="text"]:hover,
            input[type="password"]:hover,
            input[type="number"]:hover,
            input[type="date"]:hover,
            input[type="email"]:hover,
            input[type="url"]:hover,
            textarea:hover {
                border-color: #ff6e00; /* orange */
                outline: none;
                background-color: #f5f5f5; /* light gray */
            }
            input[type="text"]:focus,
            input[type="password"]:focus,
            input[type="number"]:focus,
            input[type="date"]:focus,
            input[type="email"]:focus,
            input[type="url"]:focus,
            textarea:focus {
                border-color: #ff6e00; /* orange */
                outline: none;
                background-color: #f5f5f5; /* light gray */
            }
            .stApp .stTextInput label {
                color: #333; /* dark gray */
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                padding: 5px;
            }
            input[type="number"]{
                background-color: #fff; /* white */
                color: #333; /* dark gray */
                border: 2px solid #ff6e00;
                border-radius: 5px;
                padding: 6px;
                font-size: 16px;
                width: 100%;
                margin-bottom: 2px;
                transition: border-color 0.3s ease;
            }
            
            /* Container styling */
            div[data-baseweb="select"] > div {
                background-color: #fff !important;  /* white bg */
                color: #333 !important;             /* dark text */
                caret-color: #333 !important;    /* dark caret */
                border: 2px solid #ff6e00 !important;  /* orange border */
                border-radius: 5px !important;
                padding: 0px 12px !important;
                font-size: 16px !important;
                width: 100% !important;
                margin-bottom: 20px !important;
                transition: border-color 0.3s ease !important;
                /* hide native arrow */
                -webkit-appearance: none !important;
                -moz-appearance: none !important;
                appearance: none !important;
                /* custom arrow icon */
                background-image: url("data:image/svg+xml;utf8,<svg fill='%23ff6e00' height='20' viewBox='0 0 24 24' width='20' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>") !important;
                background-repeat: no-repeat !important;
                background-position: right 12px center !important;
                background-size: 20px !important;
              }
              
            /* Hover on container */
            div[data-baseweb="select"] > div:hover {
                border-color: #e65c00 !important;   /* darker orange */
                background-color: #fafafa !important; /* very light gray */
              }

             </style>
    """, unsafe_allow_html=True)
# Admin Menu
def admin_menu(admin):
    '''Admin Menu for managing the car rental system.'''
    with st.sidebar:
        choice = st.radio("Admin Options", [
        "View Personal Info", "Add New Car", "Remove Car", "View Cars",
        "View Rental History", "View Customer History", "Logout"
        ],
        key="admin_menu_radio",  # Unique key for this radio
        )
    st.title('Admin Dashboard')
    if choice == "View Personal Info":
        image_path=get_image_path('userprofile.jpg')
        st.image(image_path,caption='Visualize')
        st.subheader("Administrator Profile Summary") 
        st.write(admin)
    elif choice == "Add New Car":
        st.subheader("Vehicle Onboarding System")
        image_path=get_image_path('addcar.jpg')
        st.image(image_path,caption='Visualize')
        car_id = st.text_input("Car ID")
        brand = st.text_input("Brand").lower()
        model = st.text_input("Model").lower()
        seating_capacity = st.number_input("Seating Capacity", step=1)
        price_per_day = st.number_input("Rent per Day",step=100)
        available = st.checkbox("Available", value=True)
        if st.button("Add Car",key="add_car_button"):
            car = Car(car_id, brand, model, seating_capacity, price_per_day, available)
            car.add_car()

    elif choice == "Remove Car":
        st.subheader("Vehicle Removal Console")
        car_id = st.text_input("Enter Car ID to remove")
        if st.button("Remove",key="remove_car_button"):
            try:
                admin - car_id
            except Exception as e:
                st.error(f"Error: {e}")

    elif choice == "View Cars":
        st.subheader("Fleet Management Overview")
        image_path=get_image_path('allcars.jpg')
        st.image(image_path,caption='Visualize')
        Admin.display_cars()

    elif choice == "View Rental History":
        st.subheader("System Wide Rental Log")
        Admin.view_rentals_history()

    elif choice == "View Customer History":
        st.subheader("Customer Database Records")
        Admin.view_customers()

    elif choice == "Logout":
        st.subheader("Terminate Admin Session")
        st.session_state.page = "main_menu"  # Return to main menu
        st.session_state.pop("admin", None)  # Clear admin data
        st.success("Logout Successful!")
        time.sleep(2) #wait for 2 seconds
        st.rerun()
# Customer Menu
def customer_menu(customer):
    '''Customer Menu for managing the car rental system.'''
    with st.sidebar:
        choice = st.radio("Customer Options", [
        "View Personal Info", "Rent Car", "Add Balance",
        "View Rental History", "Return Car", "View Available Cars", "Logout"
    ],
        key="customer_menu_radio",
    )
    st.subheader('Customer Dashboard')
    if choice == "View Personal Info":
        st.subheader("Account Details")
        image_path=get_image_path('userprofile.jpg')
        st.image(image_path,caption='Visualize')
        st.write(customer)

    elif choice == "View Available Cars":
        st.subheader("Live Vehicle Listing")
        image_path=get_image_path('availablecars.jpg')
        st.image(image_path,caption='Visualize')
        Car.display_available_cars()

    elif choice == "Rent Car":
        st.subheader("Vehicle Booking Section")
        image_path=get_image_path('addcar.jpg')
        st.image(image_path,caption='Visualize')
        rent_car_id = st.text_input("Enter Car ID")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        if 'rental_in_progress' not in st.session_state:
            st.session_state.rental_in_progress = False

        if st.button("Book My Ride",key="rent_car_button") or st.session_state.rental_in_progress:
            st.session_state.rental_in_progress = True
            try:
                start_date = str(start_date)
                end_date = str(end_date)
                customer.rent_car(rent_car_id, start_date, end_date)
            except Exception as e:
                st.error(f"Error while booking ride : {e}")
        if not st.session_state.get('processing_payment'):
            st.session_state.rental_in_progress = False

    elif choice == "Add Balance":
        st.subheader("Wallet Top-Up")
        amount = st.number_input("Enter Amount",step=100)
        if st.button("Add",key="add_balance_button"):
            try:
                amount = float(amount)
                customer + amount
            except Exception as e:
                st.error(f"Error: {e}")

    elif choice == "View Rental History":
        st.subheader("Your Booking History")
        customer.view_rental_history()

    elif choice == "Return Car":
        st.subheader("Vehicle Return Interface")
        return_car_id = st.text_input("Enter Car ID to Return")
        return_date = st.date_input("Return Date")
        if st.button("Return",key="return_car_button"):
            customer.return_car(customer.user_name, return_car_id, str(return_date))

    elif choice == "Logout":
        st.subheader("Sign Out Of Account")
        st.session_state.page = "main_menu"  # Return to main menu
        st.session_state.pop("customer", None)  # Clear customer data
        st.info("Returning to the main menu...")
        time.sleep(2)
        st.rerun()  # Force rerun to update the UI
def get_image_path(image_name):
        try:
           current_directory = os.path.dirname(__file__)
           return os.path.join(current_directory,'images',image_name)
        except Exception as e:
            st.error(f'Error image path: {e}')
def main_menu():
    '''Main Menu for the Car Rental Management System.'''
    st.title("Car Rental Management System")
    with st.sidebar:
        choice = st.radio("Select Option", ['Home','Create Account', 'Admin Login', 'Customer Login', 'Exit']
                          , key="main_menu_selectbox",)
    if choice == "Home":
        st.markdown("**Welcome & System Overview**")
        image_path=get_image_path('home.jpg')
        st.image(image_path,caption='Visualize')
        st.subheader("Instructions :")
        st.write("1. Please select an option from the sidebar to continue.")
        st.write('2. You can Create account as an admin or customer.')
        st.write('3. You can login as an admin or customer.')
        st.write('4. You can exit the program.')
        st.write('5. You can view the Available cars and rent them.')
        st.write('6. You can return it and view your rental history.')
        st.write("📍*Developed by*: Osama Hassan")
        st.markdown('https://github.com/Osamahassan2005')

    elif choice == 'Create Account':
        st.subheader(" User Registeration Portal")
        role = st.selectbox("Role", ['admin', 'customer'])
        #unique username
        user_name = st.text_input("Username")
        if user_name and len(user_name) < 4:
            st.error("Username must be at least 4 characters long.")
        #atleast one digit
        if user_name and not any(char.isdigit() for char in user_name):
            st.error("Username must contain at least one digit.")
        password = st.text_input("Password", type="password")
        if password and len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        address = st.text_input("Address") if role == 'customer' else ''

        if role == 'admin':
            admin_key = st.text_input("Enter Admin Key", type="password")
            if st.button("Administrator Access Panel",key="admin_access_button"):
                if Admin.verify_admin_key(admin_key):
                    new_admin = Admin(user_name, password, first_name, last_name, role)
                    new_admin.save_admin()
                else:
                    st.error("Invalid Admin Key!")
        else:
            balance = st.number_input("Initial Balance", step=100)
            if st.button("Customer Access Panel",key="customer_access_button"):
                try:
                    balance = float(balance)
                    new_cust = Customer(user_name, password, first_name, last_name, address, balance, role)
                    new_cust.save_customer()
                except ValueError:
                    st.error("Enter a valid balance!")

    elif choice == 'Admin Login':
        st.subheader("Admin Control Centre ")
        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")
        if st.button("Login",key="admin_login ") and username and password:
            admin= Admin.admin_login(username, password)
            if admin is None:
                st.error("Invalid username or password!")
                return
            st.session_state.admin = admin
            st.session_state.page = "admin_menu"  # Navigate to admin menu
            st.rerun()  # Force rerun to update the UI
            
    elif choice == 'Customer Login':
        st.subheader("Customer Service Portal ")
        cust_name = st.text_input("Customer Username")
        cust_password = st.text_input("Password", type="password")
        if st.button("Login",key="customer_login") and cust_name and cust_password:
            customer = Customer.customer_login(cust_name, cust_password)
            if customer is None:
                st.error("Invalid username or password!")
                return
            st.session_state.customer = customer
            st.session_state.page = "customer_menu"  # Navigate to customer menu
            st.rerun()  # Force rerun to update the UI  # Force rerun to update the UI
    elif choice == 'Exit':
        st.info("Goodbye! Thank you for using our service.")
        st.stop()
# Main Controller
def main():
    '''Main function to control the flow of the application.'''
    if st.session_state.page == 'main_menu':
        main_menu()
    elif st.session_state.page == 'admin_menu':
        admin_menu(st.session_state.admin)
    elif st.session_state.page == 'customer_menu':
        customer_menu(st.session_state.customer)
main()


