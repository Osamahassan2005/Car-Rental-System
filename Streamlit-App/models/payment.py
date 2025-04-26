import streamlit as st
class PaymentMethod:
    def __init__(self, amount, customer_name):
        self.amount = amount
        self.customer_name = customer_name
        self.payment_method = None
        self.details = [] #details store in ditionary temoporary, in future it will helps to save in file when we need real payment
        
    def process_payment(self):
        '''Processes the payment based on the selected payment method.'''
        st.subheader(f'Secure Payment Gateway for {self.customer_name}')
        self.payment_method = st.selectbox('Select payment method', ['Credit/Debit Card', 'Bank Transfer', 'Mobile Money'])
        confirmed=False
        with st.form(key=f'payment_form_{self.customer_name}'):
            if self.payment_method == 'Credit/Debit Card':
                self.payment_method='Credit/Debit Card'
                confirmed= self.credit_debit_card_payment()
            elif self.payment_method == 'Bank Transfer':
                confirmed= self.bank_transfer()
                self.payment_method='Bank Transfer'
            elif self.payment_method == 'Mobile Money':
                confirmed= self.mobile_money()
                self.payment_method='Mobile Money'
            else:
                print('Invalid Payment method.')
            return confirmed
    def credit_debit_card_payment(self):
        '''Processes credit/debit card payment.'''
        card_number = st.text_input('Enter your credit/debit card number: ')
        card_expiry = st.text_input('Enter your credit/debit card expiry date (MM/YY): ')
        card_cvv = st.text_input('Enter your credit/debit card CVV: ')
        if st.form_submit_button('Confirm & Rent'):
            if all([card_number and card_expiry and card_cvv]):
                self.details.append(f'Credit/Debit Card: {card_number}, Expiry: {card_expiry}, CVV: {card_cvv}')
                return True
            st.error('Payment failed! Please fill in all fields.')
        return False

    def bank_transfer(self):
        '''Processes bank transfer payment.'''
        bank_account_number = st.text_input('Enter your bank account number: ')
        bank_routing_number = st.text_input('Enter your bank routing number: ')
        if st.form_submit_button('Confirm & Rent'):
            if all([bank_account_number and bank_routing_number]):
                self.details.append(f'Account No: {bank_account_number}, Routing: {bank_routing_number}')
                return True
            st.error('Payment failed! Please fill in all fields.')
        return False

    def mobile_money(self):
        '''Processes mobile money payment.'''
        mobile_money_number = st.text_input('Enter your mobile money number: ')
        mobile_money_provider = st.text_input('Enter your mobile money provider: ')
        if st.form_submit_button('Confirm & Rent'):
            if all([mobile_money_number and mobile_money_provider]):
                self.details.append(f'Mobile Money: {mobile_money_number}, Provider: {mobile_money_provider}')
                return True
            st.error('Payment failed! Please fill in all fields.')
        return False

