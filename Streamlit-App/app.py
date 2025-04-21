import streamlit as st
import time
import os
from models.car import Car
from models.customer import Customer
from models.admin import Admin  

#css
st.markdown("""
    <style> 
        .stApp {
            background-size: cover;
            color: #333;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            text-align: left;
            padding: 20px;
            border-radius: 20px;
            margin: 20px;
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
                background-color: #FF6e00; /* orange */
                color: #fff; /* white */
                padding: 20px;
                border-radius: 20px;
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
                color: #fff; /* white */
                font-size: 18px;
                font-weight: bold;
                text-align: left;
            padding: 5px;
            }
             </style>
    """, unsafe_allow_html=True)

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "main_menu"

# Main Menu
def main_menu():
    st.title("Car Rental Management System")
    with st.sidebar:
        choice = st.radio("Select Option", ['Home','Create Account', 'Admin Login', 'Customer Login', 'Exit']
                          , key="main_menu_selectbox",)
    if choice == "Home":
        st.markdown("**Welcome & System Overview**")
        st.image(os.path.join(os.getcwd(), "Streamlit-App/image/home.jpg"))
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
        user_name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        address = st.text_input("Address") if role == 'customer' else ''

        if role == 'admin':
            admin_key = st.text_input("Enter Admin Key", type="password")
            if st.button("Administrator Access Panel"):
                if Admin.verify_admin_key(admin_key):
                    new_admin = Admin(user_name, password, first_name, last_name, role)
                    new_admin.save_admin()
                else:
                    st.error("Invalid Admin Key!")
        else:
            balance = st.text_input("Initial Balance")
            if st.button("Customer Access Panel"):
                try:
                    balance = float(balance)
                    new_cust = Customer(user_name, password, first_name, last_name, address, balance, role)
                    new_cust.save_customer()
                    st.success("Customer account created!")
                except ValueError:
                    st.error("Enter a valid balance!")

    elif choice == 'Admin Login':
        st.subheader("Admin Control Centre ")
        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")
        if st.button("Login") and username and password:
            st.session_state.admin = Admin.admin_login(username, password)
            st.session_state.page = "admin_menu"  # Navigate to admin menu
            st.rerun()  # Force rerun to update the UI
        else:
            st.info("Please enter your name and password to login.")
            
    elif choice == 'Customer Login':
        st.subheader("Customer Service Portal ")
        cust_name = st.text_input("Customer Username")
        cust_password = st.text_input("Password", type="password")
        if st.button("Login") :
            st.session_state.customer = Customer.customer_login(cust_name, cust_password)
            st.session_state.page = "customer_menu"  # Navigate to customer menu
            st.rerun()  # Force rerun to update the UI  # Force rerun to update the UI
        else:
            st.info("Please enter your name and password to login.")
    elif choice == 'Exit':
        st.info("Goodbye! Thank you for using our service.")
        st.stop()

# Admin Menu
def admin_menu(admin):
    with st.sidebar:
        st.subheader(f"Welcome {admin.first_name.upper()}")
        choice = st.radio("Admin Options", [
        "View Personal Info", "Add New Car", "Remove Car", "View Cars",
        "View Rental History", "View Customer History", "Logout"
        ],
        key="admin_menu_radio",  # Unique key for this radio
        )
    st.title('Admin Dashboard')
    if choice == "View Personal Info":
        st.image('Streamlit-App/image/userprofile.jpg')
        st.subheader("Administrator Profile Summary") 
        st.write(admin)
    elif choice == "Add New Car":
        st.subheader("Vehicle Onboarding System")
        st.image('Streamlit-App/image/addcar.jpg')
        car_id = st.text_input("Car ID")
        brand = st.text_input("Brand").lower()
        model = st.text_input("Model").lower()
        seating_capacity = st.number_input("Seating Capacity", step=1)
        price_per_day = st.number_input("Rent per Day",step=100)
        available = st.checkbox("Available", value=True)
        if st.button("Add Car"):
            car = Car(car_id, brand, model, seating_capacity, price_per_day, available)
            car.add_car()

    elif choice == "Remove Car":
        st.subheader("Vehicle Removal Console")
        car_id = st.text_input("Enter Car ID to remove")
        if st.button("Remove"):
            try:
                admin - car_id
            except Exception as e:
                st.error(f"Error: {e}")

    elif choice == "View Cars":
        st.subheader("Fleet Management Overview")
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
    with st.sidebar:
        st.subheader(f"Welcome {customer.first_name.upper()}")
        choice = st.radio("Customer Options", [
        "View Personal Info", "Rent Car", "Add Balance",
        "View Rental History", "Return Car", "View Available Cars", "Logout"
    ],
        key="customer_menu_radio",
    )
    st.subheader('Customer Dashboard')
    if choice == "View Personal Info":
        st.subheader("Account Details")
        st.image('Streamlit-App/image/userprofile.jpg')
        st.write(customer)

    elif choice == "View Available Cars":
        st.subheader("Live Vehicle Listing")
        Car.display_available_cars()

    elif choice == "Rent Car":
        st.subheader("Vehicle Booking Section")
        st.image('Streamlit-App/image/addcar.jpg')
        rent_car_id = st.text_input("Enter Car ID")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        st.write('''**Payment Form Proccessing...**
                 Please fill the given requirements first!''')
        customer.rent_car(rent_car_id, str(start_date), str(end_date))

    elif choice == "Add Balance":
        st.subheader("Wallet Top-Up")
        amount = st.number_input("Enter Amount",step=500)
        if st.button("Add"):
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
        if st.button("Return"):
            customer.return_car(customer.user_name, return_car_id, str(return_date))


    elif choice == "Logout":
        st.subheader("Sign Out Of Account")
        st.session_state.page = "main_menu"  # Return to main menu
        st.session_state.pop("customer", None)  # Clear customer data
        st.info("Returning to the main menu...")
        time.sleep(2)
        st.rerun()  # Force rerun to update the UI

# Main Controller
def main():
    if st.session_state.page == 'main_menu':
        main_menu()
    
    elif st.session_state.page == 'admin_menu':
        if 'admin' in st.session_state and st.session_state.admin is not None:
            admin_menu(st.session_state.admin)
        else:
            st.error("Admin not logged in. Please log in first.")
            st.session_state.page = 'main_menu'
    
    elif st.session_state.page == 'customer_menu':
        if 'customer' in st.session_state and st.session_state.customer is not None:
            customer_menu(st.session_state.customer)
        else:
            st.error("Customer not logged in. Please log in first.")
            st.session_state.page = 'main_menu'

main()


