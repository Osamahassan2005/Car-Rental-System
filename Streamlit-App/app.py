import streamlit as st
import time
import os
from pathlib import Path
from models.car import Car
from models.customer import Customer
from models.admin import Admin  

# Helper function for image paths
def get_image_path(image_name):
    try:
        base_path = Path(__file__).parent
        image_path = base_path / "images" / image_name
        if not image_path.exists():
            return None
        return str(image_path)
    except Exception as e:
        st.warning(f"Image path error: {str(e)}")
        return None

# CSS Styling
st.markdown("""
    <style> 
        .stApp {
            color: #1a1a1a;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            text-align: left;
            padding: 5px;
            border-radius: 0px;
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
            color:#1a1a1a;
            font-family: 'Poppins',sans-serif;
            font-size: 46px;
            font-weight: bold;
            text-align: left;
        }
        .stApp h2, .stApp h3, .stApp h4 {
            color: #ff6e00;
            font-size: 28px;
            font-weight: bold;
            text-align: left;
        }
        .stApp p {
            color: #333;
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
            background-color: #ff6e00;
            color: #fff;
            border: none;
            border-radius: 7px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }   
        .stApp button:hover {
            transition: background-color 0.3s ease;
            color: #fff;
            background-color: #e65c00;
        }
        section[data-testid="stSidebar"] {
            background-color: #FF6e00;
            color: #fff;
            padding: 20px;
            border-radius: 20px;
            margin: 2px;
        }
        section[data-testid="stSidebar"] button {
            background-color: #fff;
            color: #ff6e00;
            border: none;
            border-radius: 7px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        section[data-testid="stSidebar"] h2{
            color: #fff;
            font-size: 24px;
            font-weight: bold;
            text-align: left;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            text-align: left;
            padding: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "main_menu"
    if "admin" not in st.session_state:
        st.session_state.admin = None
    if "customer" not in st.session_state:
        st.session_state.customer = None

# Main Menu
def main_menu():
    st.title("Car Rental Management System")
    with st.sidebar:
        choice = st.radio(
            "Select Option", 
            ['Home','Create Account', 'Admin Login', 'Customer Login', 'Exit'],
            key="main_menu_selectbox"
        )

    if choice == "Home":
        st.markdown("**Welcome & System Overview**")
        home_img = get_image_path("home.jpg")
        if home_img:
            st.image(home_img)
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
        st.subheader("User Registration Portal")
        role = st.selectbox("Role", ['admin', 'customer'], key="role_select")
        user_name = st.text_input("Username", key="reg_username")
        password = st.text_input("Password", type="password", key="reg_password")
        first_name = st.text_input("First Name", key="reg_first_name")
        last_name = st.text_input("Last Name", key="reg_last_name")
        
        if role == 'admin':
            admin_key = st.text_input("Enter Admin Key", type="password", key="admin_key")
            if st.button("Create Admin Account"):
                if not all([user_name, password, first_name, last_name, admin_key]):
                    st.error("Please fill all fields!")
                elif Admin.verify_admin_key(admin_key):
                    try:
                        new_admin = Admin(user_name, password, first_name, last_name, role)
                        new_admin.save_admin()
                        st.success("Admin account created successfully!")
                    except Exception as e:
                        st.error(f"Error creating admin: {str(e)}")
                else:
                    st.error("Invalid Admin Key!")
        
        else:  # Customer registration
            address = st.text_input("Address", key="cust_address")
            balance = st.number_input("Initial Balance", min_value=0.0, step=100.0, key="cust_balance")
            if st.button("Create Customer Account"):
                if not all([user_name, password, first_name, last_name, address]):
                    st.error("Please fill all fields!")
                else:
                    try:
                        new_cust = Customer(user_name, password, first_name, last_name, address, float(balance), role)
                        new_cust.save_customer()
                        st.success("Customer account created successfully!")
                    except ValueError:
                        st.error("Please enter a valid balance!")
                    except Exception as e:
                        st.error(f"Error creating customer: {str(e)}")

    elif choice == 'Admin Login':
        st.subheader("Admin Control Centre")
        username = st.text_input("Admin Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")
        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                with st.spinner("Authenticating..."):
                    try:
                        admin = Admin.admin_login(username, password)
                        if admin:
                            st.session_state.admin = admin
                            st.session_state.page = "admin_menu"
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Login error: {str(e)}")

    elif choice == 'Customer Login':
        st.subheader("Customer Service Portal")
        cust_name = st.text_input("Customer Username", key="cust_username")
        cust_password = st.text_input("Password", type="password", key="cust_password")
        if st.button("Login"):
            if not cust_name or not cust_password:
                st.error("Please enter both username and password")
            else:
                with st.spinner("Authenticating..."):
                    try:
                        customer = Customer.customer_login(cust_name, cust_password)
                        if customer:
                            st.session_state.customer = customer
                            st.session_state.page = "customer_menu"
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Login error: {str(e)}")

    elif choice == 'Exit':
        st.info("Goodbye! Thank you for using our service.")
        st.stop()

# Admin Menu
def admin_menu():
    admin = st.session_state.get('admin')
    if not admin:
        st.error("Admin session expired. Redirecting to login...")
        st.session_state.page = "main_menu"
        time.sleep(2)
        st.rerun()
        return

    with st.sidebar:
        st.subheader(f"Welcome {admin.first_name.upper()}")
        menu_options = [
            "View Personal Info", "Add New Car", "Remove Car", "View Cars",
            "View Rental History", "View Customer History", "Logout"
        ]
        choice = st.radio(
            "Admin Options",
            menu_options,
            key="admin_menu_radio"
        )

    st.title('Admin Dashboard')
    
    try:
        if choice == "View Personal Info":
            profile_img = get_image_path('userprofile.jpg')
            if profile_img:
                st.image(profile_img)
            st.subheader("Administrator Profile Summary") 
            st.write(admin)

        elif choice == "Add New Car":
            st.subheader("Vehicle Onboarding System")
            car_img = get_image_path('addcar.jpg')
            if car_img:
                st.image(car_img)
            with st.form("add_car_form"):
                car_id = st.text_input("Car ID", key="add_car_id")
                brand = st.text_input("Brand").lower()
                model = st.text_input("Model").lower()
                seating_capacity = st.number_input("Seating Capacity", min_value=1, step=1)
                price_per_day = st.number_input("Rent per Day", min_value=0.0, step=100.0)
                available = st.checkbox("Available", value=True)
                
                if st.form_submit_button("Add Car"):
                    if not all([car_id, brand, model]):
                        st.error("Please fill all required fields!")
                    else:
                        try:
                            car = Car(car_id, brand, model, seating_capacity, price_per_day, available)
                            car.add_car()
                            st.success(f"Car {car_id} added successfully!")
                        except Exception as e:
                            st.error(f"Error adding car: {str(e)}")

        elif choice == "Remove Car":
            st.subheader("Vehicle Removal Console")
            car_id = st.text_input("Enter Car ID to remove", key="remove_car_id")
            if st.button("Remove Car"):
                if not car_id:
                    st.error("Please enter a car ID")
                else:
                    try:
                        result = admin.remove_car(car_id)
                        if result:
                            st.success(f"Car {car_id} removed successfully")
                        else:
                            st.error(f"Failed to remove car {car_id}")
                    except Exception as e:
                        st.error(f"Error removing car: {str(e)}")

        elif choice == "View Cars":
            st.subheader("Fleet Management Overview")
            try:
                Admin.display_cars()
            except Exception as e:
                st.error(f"Error displaying cars: {str(e)}")

        elif choice == "View Rental History":
            st.subheader("System Wide Rental Log")
            try:
                Admin.view_rentals_history()
            except Exception as e:
                st.error(f"Error viewing rental history: {str(e)}")

        elif choice == "View Customer History":
            st.subheader("Customer Database Records")
            try:
                Admin.view_customers()
            except Exception as e:
                st.error(f"Error viewing customers: {str(e)}")

        elif choice == "Logout":
            st.subheader("Terminate Admin Session")
            if st.button("Confirm Logout"):
                st.session_state.clear()
                st.session_state.page = "main_menu"
                st.success("Logout Successful! Redirecting...")
                time.sleep(2)
                st.rerun()

    except Exception as e:
        st.error(f"Admin menu error: {str(e)}")
        st.session_state.clear()
        st.session_state.page = "main_menu"
        st.rerun()

# Customer Menu
def customer_menu():
    customer = st.session_state.get('customer')
    if not customer:
        st.error("Customer session expired. Redirecting to login...")
        st.session_state.page = "main_menu"
        time.sleep(2)
        st.rerun()
        return

    with st.sidebar:
        st.subheader(f"Welcome {customer.first_name.upper()}")
        menu_options = [
            "View Personal Info", "Rent Car", "Add Balance",
            "View Rental History", "Return Car", "View Available Cars", "Logout"
        ]
        choice = st.radio(
            "Customer Options",
            menu_options,
            key="customer_menu_radio"
        )

    st.title('Customer Dashboard')
    
    try:
        if choice == "View Personal Info":
            st.subheader("Account Details")
            profile_img = get_image_path('userprofile.jpg')
            if profile_img:
                st.image(profile_img)
            st.write(customer)

        elif choice == "View Available Cars":
            st.subheader("Live Vehicle Listing")
            try:
                Car.display_available_cars()
            except Exception as e:
                st.error(f"Error displaying cars: {str(e)}")

        elif choice == "Rent Car":
            st.subheader("Vehicle Booking Section")
            car_img = get_image_path('addcar.jpg')
            if car_img:
                st.image(car_img)
            with st.form("rent_car_form"):
                rent_car_id = st.text_input("Enter Car ID", key="rent_car_id")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                
                if st.form_submit_button("Rent Car"):
                    if not rent_car_id:
                        st.error("Please enter a car ID")
                    elif start_date >= end_date:
                        st.error("End date must be after start date")
                    else:
                        try:
                            result = customer.rent_car(rent_car_id, str(start_date), str(end_date))
                            if result:
                                st.success("Car rented successfully!")
                            else:
                                st.error("Failed to rent car")
                        except Exception as e:
                            st.error(f"Error renting car: {str(e)}")

        elif choice == "Add Balance":
            st.subheader("Wallet Top-Up")
            amount = st.number_input("Enter Amount", min_value=0.0, step=100.0, key="add_balance")
            if st.button("Add Balance"):
                try:
                    result = customer.add_balance(float(amount))
                    if result:
                        st.success(f"Added {amount:.2f} to balance. New balance: {customer.balance:.2f}")
                    else:
                        st.error("Failed to add balance")
                except ValueError:
                    st.error("Please enter a valid amount")
                except Exception as e:
                    st.error(f"Error adding balance: {str(e)}")

        elif choice == "View Rental History":
            st.subheader("Your Booking History")
            try:
                customer.view_rental_history()
            except Exception as e:
                st.error(f"Error viewing rental history: {str(e)}")

        elif choice == "Return Car":
            st.subheader("Vehicle Return Interface")
            return_car_id = st.text_input("Enter Car ID to Return", key="return_car_id")
            return_date = st.date_input("Return Date")
            if st.button("Return Car"):
                if not return_car_id:
                    st.error("Please enter a car ID")
                else:
                    try:
                        result = customer.return_car(return_car_id, str(return_date))
                        if result:
                            st.success("Car returned successfully!")
                        else:
                            st.error("Failed to return car")
                    except Exception as e:
                        st.error(f"Error returning car: {str(e)}")

        elif choice == "Logout":
            st.subheader("Sign Out Of Account")
            if st.button("Confirm Logout"):
                st.session_state.clear()
                st.session_state.page = "main_menu"
                st.info("Logout successful! Redirecting...")
                time.sleep(2)
                st.rerun()

    except Exception as e:
        st.error(f"Customer menu error: {str(e)}")
        st.session_state.clear()
        st.session_state.page = "main_menu"
        st.rerun()

# Main Controller
def main():
    init_session_state()
    
    try:
        if st.session_state.page == 'main_menu':
            main_menu()
        elif st.session_state.page == 'admin_menu':
            admin_menu()
        elif st.session_state.page == 'customer_menu':
            customer_menu()
            
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.session_state.clear()
        st.session_state.page = "main_menu"
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main()
