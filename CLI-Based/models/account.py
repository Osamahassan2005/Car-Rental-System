class Account:
    def __init__(self,role,user_name,password,first_name,last_name):
        self.role=role
        self.user_name=user_name
        self.first_name=first_name
        self.last_name=last_name
        self.password=password
    def __str__(self):
        return f"\n{self.role.upper()} Info: \n{'-'*20}\n Role: {self.role}\n Username: {self.user_name}\n Password: {self.password}\n First name: {self.first_name}\n Last name: {self.last_name}\n"
    @classmethod
    def login(cls,accounts,user_name,password):
        try:
            if accounts.empty:
               print(f'No Account availables.')
               return None
            user_name=str(user_name).strip().lower()
            password=str(password).strip()
            matched_account= accounts[(accounts['user_name'].astype(str).str.lower() == user_name) & (accounts['password'].astype(str) ==password)]
            if not matched_account.empty:
                accounts_data=matched_account.iloc[0].to_dict()
                print('Login Succesfully!')
                return cls(**accounts_data)
            else:
                print('Account not found.')
                return None
        except Exception as e:
            print(f'LogIn Error:',e)
            return None  

#client code for test 
# c=Account('xyz123','2468xyz','john','boby')
# print(a)
    