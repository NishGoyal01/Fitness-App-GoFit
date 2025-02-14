import mysql.connector as sql
from prettytable import PrettyTable

# to create database 'go_fit'
def create_database():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE go_fit;")
    print("Database has been created.")
    print()
    mycursor.execute("SHOW DATABASES;")
    d = mycursor.fetchall()
    print("Databases available are: ")
    for i in d:
        print(i)
    mydb.commit()
    mydb.close()

create_database()

# to create a users table to store login
def create_users():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    mycursor = mydb.cursor()
    mycursor.execute("""
    CREATE TABLE users(
        user_id INT(15),
        user_name VARCHAR(10),
        passw VARCHAR(10),
        gen VARCHAR(1),
        age INT(3),
        subscription INT(10)
    );
    """)
    mytable = PrettyTable(["user id", "user name", "password", "gender", "age", "subscription"])
    mycursor.execute("DESC users;")
    a = mycursor.fetchall()
    for i in a:
        mytable.add_row(i)
    print(mytable)
    mydb.commit()
    mydb.close()

create_users()

# to display the user's table's data
def show():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users;")
        d = mycursor.fetchall()
        mytable1 = PrettyTable(["user id", "user name", "password", "gender", "age", "subscription"])
        for i in d:
            mytable1.add_row(i)
        print(mytable1)
    else:
        print("Error in connectivity")
    mydb.close()

# for signing up
def users_signup():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    if mydb.is_connected():
        mycursor = mydb.cursor()
        user = input("Enter your user name: ")
        passw = input("Enter your password: ")
        gen = input("Enter your gender(M/F/other): ")
        age = input("Enter your age: ")
        ask = input("Want to take our subscription: ")
        if ask == "y" or ask == "Y":
            subs = int(input("Enter time period of subscription in months: "))
        else:
            subs = 0
        mycursor.execute("SELECT user_id FROM users;")
        data = mycursor.fetchall()
        if data == []:
            u_id = 101
        else:
            u_id = data[-1][0] + 1
        mycursor.execute("""
        INSERT INTO users (user_id, user_name, passw, gen, age, subscription) 
        VALUES({}, '{}', '{}', '{}', {}, {});
        """.format(u_id, user, passw, gen, age, subs))
        print("Signup successful!!!")
        print("Your user ID is", u_id)
        mydb.commit()
    else:
        print("Error in connectivity")
    mydb.close()

# for hydration
def hydration():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    if mydb.is_connected():
        mycursor = mydb.cursor()
        qty = int(input("How many glasses of water have you taken today? "))
        if qty < 8:
            print("Your target is just", 8 - qty, "glasses far")
        elif qty == 8:
            print("Good job :) Keep it up !!")
        else:
            print("Woohoo, doing great !!!")
        mydb.commit()
    else:
        print("Error in connectivity")
    mydb.close()

# to enter user's fitness data
def fitdata():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    if mydb.is_connected():
        mycursor = mydb.cursor()
        uid = int(input("Enter your user id: "))
        
        # BMI
        height = float(input("Enter your height in cm: "))
        weight = float(input("Enter your weight in kg: "))
        the_BMI = weight / (height / 100) ** 2
        print("Your Body Mass Index is", the_BMI)
        
        if the_BMI < 18.5:
            print("You are underweight")
        elif 18.5 <= the_BMI <= 24.9:
            print("You are completely healthy and fine :)")
        elif 25.0 <= the_BMI <= 29.9:
            print("You are overweight")
        elif 30 <= the_BMI <= 34.9:
            print("You are obese")
        else:
            print("You are extremely obese")
        
        # Sugar level
        sugar = int(input("Enter your blood sugar level (in mg/dL): "))
        if sugar < 70:
            print("Low sugar level")
        elif 70 <= sugar <= 99:
            print("Normal sugar level :)")
        else:
            print("Sugar level is high")

        # Heart rate
        heart = int(input("Enter your heart rate (in bpm): "))
        if heart < 60:
            print("Your heart rate is low")
        elif 60 <= heart <= 100:
            print("Your heart rate is normal :)")
        else:
            print("Your heart rate is high")
        
        # Blood pressure
        sys = int(input("Enter your systolic pressure (in mmHg): "))
        dia = int(input("Enter your diastolic pressure (in mmHg): "))
        if sys < 90 or dia < 60:
            print("Low BP!!!")
        elif 90 <= sys < 130 and 60 <= dia < 80:
            print("Your BP is absolutely normal")
        else:
            print("High BP")
        
        # Calorie intake
        cal = int(input("Enter your calorific value (in kcal): "))
        if cal < 2700:
            print("Low calorific value")
        elif cal == 2700:
            print("Normal calorific value")
        
        mycursor.execute("""
        INSERT INTO fit (user_id, the_BMI, sugar_level, heart_rate, systolic, diastolic, calorific_value) 
        VALUES({}, {}, {}, {}, {}, {}, {});
        """.format(uid, the_BMI, sugar, heart, sys, dia, cal))
        
        mycursor.execute("SELECT * FROM fit WHERE user_id = {};".format(uid))
        t = mycursor.fetchall()
        mytable7 = PrettyTable(["user id", "BMI", "sugar level", "heart rate", "systolic pressure", "diastolic pressure", "calorific value"])
        for row in t:
            mytable7.add_row(row)
        print(mytable7)
        mydb.commit()
    else:
        print("Error in connectivity")
    mydb.close()

# to manage subscription functionality
def manage_subscription():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    if mydb.is_connected():
        mycursor = mydb.cursor()
        
        # User selects the subscription management option
        user_id = int(input("Enter your user ID to manage subscription: "))
        mycursor.execute("SELECT subscription FROM users WHERE user_id = {};".format(user_id))
        result = mycursor.fetchone()

        if result:
            current_subscription = result[0]
            if current_subscription > 0:
                print(f"Your current subscription is active for {current_subscription} months.")
                renew_choice = input("Do you want to renew your subscription? (y/n): ")
                if renew_choice.lower() == 'y':
                    additional_months = int(input("How many additional months do you want to subscribe for? "))
                    new_subscription = current_subscription + additional_months
                    mycursor.execute("""
                    UPDATE users
                    SET subscription = {}
                    WHERE user_id = {};
                    """.format(new_subscription, user_id))
                    print(f"Your subscription has been renewed for {additional_months} months. Total subscription is now {new_subscription} months.")
                else:
                    print("You chose not to renew your subscription.")
            else:
                print("You don't have an active subscription.")
                new_subscription = int(input("Do you want to subscribe? Enter the number of months: "))
                mycursor.execute("""
                UPDATE users
                SET subscription = {}
                WHERE user_id = {};
                """.format(new_subscription, user_id))
                print(f"Your subscription has been activated for {new_subscription} months.")
        else:
            print("User ID not found.")
        
        mydb.commit()
    else:
        print("Error in connectivity")
    mydb.close()


# for login and sign-up window
def start():
    mydb = sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")
    if mydb.is_connected():
        mycursor = mydb.cursor()
        print("1. Log in")
        print("2. Sign up")
        print("3. Manage Subscription")

        ch = int(input("Enter your choice: "))
        
        if ch == 1:
            print("""LOGIN
            1. Administrator
            2. User""")
            ch2 = int(input("Enter user type: "))
            
            if ch2 == 1:
                ctr = 0
                while ctr < 3:
                    password = input("Enter your password: ")
                    if password == "admin01":
                        print("1. View users")
                        print("2. Delete users")
                        ch3 = int(input("Enter your choice: "))
                        
                        if ch3 == 1:
                            show()
                        elif ch3 == 2:
                            mycursor.execute("SELECT * FROM users;")
                            m = mycursor.fetchall()
                            print(m)
                            users_id = int(input("Enter user id: "))
                            mycursor.execute("DELETE FROM fit WHERE user_id = {};".format(users_id))
                            mycursor.execute("DELETE FROM users WHERE user_id = {};".format(users_id))
                            print("User has been removed !!!")
                            mycursor.execute("SELECT * FROM users;")
                            r2 = mycursor.fetchall()
                            print(r2)
                            mycursor.execute("SELECT * FROM fit;")
                            r3 = mycursor.fetchall()
                            print(r3)
                        else:
                            print("Invalid choice")
                        ctr = 4
                    else:
                        print("Wrong password")
                        ctr += 1
            elif ch2 == 2:
                j = 0
                while j < 3:
                    uid = int(input("Enter your user id: "))
                    pw = input("Enter your password: ")
                    mycursor.execute("SELECT user_id, passw FROM users;")
                    data = mycursor.fetchall()
                    f = 0
                    for i in data:
                        if uid == i[0] and pw == i[1]:
                            print("WELCOME")
                            fitdata()
                            f = 1
                            j = 4
                            print("1. View details")
                            print("2. Update details")
                            print("3. Routine check-up")
                            print("4. Exit")
                            ch4 = int(input("Enter your choice: "))
                            if ch4 == 1:
                                show()
                            elif ch4 == 2:
                                users_signup()
                            elif ch4 == 3:
                                hydration()
                            elif ch4 == 4:
                                print("Thanks for using our app")
                                break
                            else:
                                print("Invalid choice")
                            break
                    if f == 0:
                        print("Incorrect id/password, please try again")
                        j += 1
        elif ch == 2:
            users_signup()
        elif ch == 3:
            manage_subscription()
        else:
            print("Invalid choice")
    else:
        print("Error in connectivity")
    mydb.close()

start()