import json
import random
import string
from pathlib import Path



class Bank:

    database='data.json'
    data=[]
    try:
        if Path(database).exists():
            with open(database) as fs:
                content =fs.read()
                
                data=json.loads(content)
        else:
            print("no sch file exists")
    except Exception as err:
        print(f"an  error occered as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        sp_ch=random.choices("@#$%^&*!",k=1)
        id=alpha+num+sp_ch
        random.shuffle(id)
        return "".join(id)

    def Createaccount(self):
        info={"name":input("tell your name:-"),
              "age":int(input("tell your age:-")),
              "email":input("tell your email:-"),
              "pin":int(input("tell your pin:-")),
              "accountNo.": Bank.__accountgenerate(),
              "balance":0
                }
        if info['age']<18 or len(str(info['pin']))!=4:
            print("sorry you cannot create your account")
        else:
            print("your account created successfully")
            for i in info:
                print(f"{i}:{info[i]}")
            print("please note down your account number")

            Bank.data.append(info)
            
            Bank.__update()
    
    def depositmoney(self):
        accnumber=input("please tell your account number:-")
        pin=int(input("tell your pin number:-"))

        userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
        if userdata==False:
            print("sorry  no data found")
        else:
            amount=int(input("how much amount you want to deposit:-"))
            if amount>10000 or amount<0:
                print("sorry the amount is too much you can deposit below 10000 or above 0 ")
            else:
                userdata[0]['balance']+=amount
                Bank.__update()
                print("Amount deposited successfully")
    def withdrawmoney(self):
        accnumber=input("please tell your account number:-")
        pin=int(input("tell your pin number:-"))

        userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
        if userdata==False:
            print("sorry  no data found")
        else:
            amount=int(input("how much amount you want to withdraw:-"))
            if userdata[0]['balance']<amount:
                print("sorry you do not have that much money")
            else:
                userdata[0]['balance']-=amount
                Bank.__update()
                print("Amount withdraw successfully")
    def showdetails(self):
        accnumber=input("please tell your account number:-")
        pin=int(input("tell your pin number:-"))

        userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
        print("your information are\n")
        for i in userdata[0]:
            print(f"{i}:{userdata[0][i]}")
    def updatedetails(self):
        accnumber=input("please tell your account number:-")
        pin=int(input("tell your pin number:-"))

        userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
        
        if userdata==False:
            print("no such user found")
        else:
            print("you cannot change age,account number,balance")
            print("fill the details for change or leave it empty if no change ")

            newdata={
                "name":input("tell your newname:-"),
                "email":input("tell your new email:-"),
                "pin":input("tell your new pin:-")
            }
            if newdata['name']=="":
                newdata['name']=userdata['name']
            if newdata['email']=="":
                newdata['email']=userdata['email']
            if newdata['pin']=="":
                newdata['pin']=userdata['pin']
                
            newdata['age']=userdata[0]['age']
            newdata['accountNo.']=userdata[0]['accountNo.']
            newdata['balance']=userdata[0]['balance']
            if type(newdata['pin'])==str:
                newdata['pin']=int(newdata['pin'])
            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]
            Bank.__update()
            print("details updated successfully")
    def delete(self):
        accnumber=input("please tell your account number:-")
        
        pin=int(input("tell your pin number:-"))
        

        userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
        
        if userdata==False:
            print("no such user found")
        else:
            Bank.data.remove(userdata[0])
            Bank.__update()
            print("account deleted successfully")
            

user=Bank()
print("press 1 for creating an account")
print("press 2 for depositing the money in the bank")
print("press 3 for withdrawing the money ")
print("press 4 for accessing the details")
print("press 5 for  update details")
print("press 6 for deleting an account")

check =int(input("tell your respose:-"))
if check ==1:
    user.Createaccount()
elif check ==2:
    user.depositmoney()
elif check ==3:
    user.withdrawmoney()
elif check ==4:
    user.showdetails()
elif check ==5:
    user.updatedetails()
elif check ==6:
    user.delete()
else:
    print("invalid choice")
    









