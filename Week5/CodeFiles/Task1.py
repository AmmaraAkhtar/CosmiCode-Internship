class bankAccount:
    def __init__(self,accountnumber,balance, owner_name):
        self.accountnumber=accountnumber
        self.balance=balance
        self.owner_name=owner_name

    def deposit(self,balance1):
        self.balance =self.balance + balance1
        print(f"New Balance after depoist is:, {self.balance}")
    def withdrawal(self,balance):
        if(self.balance>balance):
            self.balance = self.balance- balance
            print(f"New Balance after withdrwal is:, {self.balance}")
        else:
            print("You are not elible for withdrwal")

    def transfer(self,accountnumber,balance):
        if(self.balance> balance):
            self.balance -= balance
            print(f"The balance {balance } is transfer to {accountnumber} from {self.owner_name}")
        else:
            print("You are not elible for withdrwal")




BA=bankAccount("12345",12000,"Ammara Akhtar")
BA.deposit(20000)
BA.transfer("89087",5000)