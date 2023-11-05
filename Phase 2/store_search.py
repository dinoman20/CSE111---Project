import sqlite3
from sqlite3 import Error

#use a for loop or one line
def openConnection(_dbFile):
    print("Connecting to Store")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("Connection established")
        print("\n")
    except Error as e:
        print(e)
    return conn

def closeConnection(_conn, _dbFile):
    print("Discounting from Store: ", _dbFile)

    try:
        _conn.close()
        print("Disconnected")
    except Error as e:
        print(e)

def Empty(_conn):
    print("Database Wipped")

    _conn.execute("BEGIN")
    try:
        sql = "delete from Store"
        _conn.execute(sql)

        sql = "delete from Customer"
        _conn.execute(sql)

        _conn.execute("COMMIT")
        
    except Error as e:
        _conn.execute("ROLLBACK")
        print(e)

def Inventory(_conn):
    print("Inventory of the store:")
    try:
        sql = """select *
        from Store"""
        cur = _conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            l = '{:>1} | {:>1} | {:>1} | {:>1}'.format(row[2], row[3], row[4],row[5])
            print(l)
    except Error as e:
        print(e)

def Add_to_Inventory(_conn,game,choice):
    print("logging\n")
    #game = input("Game: ")
    amount = input("Amount of copies: ")
    type = input("Type of copies: ")
    try:
        if(choice == 1):
            sql = """UPDATE Store
                SET number_of_copies = number_of_copies + ?
                WHERE Game = ? AND Form_of_copy = ?"""
            args = [amount, game, type]

            cur = _conn.cursor()
            cur.execute(sql,args)
            _conn.commit()
        else:
            price = input("Price of copies:")
            sql = "INSERT INTO Store VALUES(?,?,?,?,?,?)"
            args = ["Game Stop","LA",game, amount, type,price]

            cur = _conn.cursor()
            cur.execute(sql,args)
            _conn.commit()       

    except Error as e:
        print(e)

def game_catalog(_conn):
    print("Games catalog:")
    try:
        sql = """select *
        from Game"""
        cur = _conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            #l = '{:>10} | {:>1} | {:>1} | {:>1}'.format(row[2], row[3], row[4],row[5])
            print(row[0])
        check = True
        while(check):
            game = input("Choose: ")
            sql = """SELECT EXISTS(SELECT 1 
                    FROM Game WHERE 
                    name = ? );"""
            args = [game]

            cur = _conn.cursor()
            cur.execute(sql,args)

            rows = int(cur.fetchone()[0])
            if(rows == 1):
                check = False
            else:
                value = input("Game does not exist try again(t) or exit(e): ")
                if(value == "e"):
                    return 0
    except Error as e:
        print(e)
    return game

def search(_conn):
    print("Search")
    game = input("Game: ")
    try:
        sql = """Select number_of_copies,Game,Form_of_copy,price
            from Store
            WHERE Game = ? """
        args = [game]

        cur = _conn.cursor()
        cur.execute(sql,args)

        rows = cur.fetchall()
        for row in rows:
            #l = '{:>10} | {:>1} | ${:>1} | {:>1}'.format(row[2], row[3], row[4],row[5])
            print(row)
            #print(l)        

    except Error as e:
        print(e)

def Cost(_conn,game,amount,type):
    cost = 0
    try:
        sql = """Select price
            from Store
            WHERE Game = ? AND Form_of_copy = ?"""
        args = [game,type]
        
        cost = 0

        cur = _conn.cursor()
        cur.execute(sql,args)
        
        rows = int(cur.fetchone()[0])
        cost = rows * float(amount)
    except Error as e:
        print(e) 
    return cost

def Buy(_conn,username):
    print("Buying")
    game = input("Game: ")
    amount = input("Amount: ")
    type = input("Form: ")
    try:
        sql = """UPDATE Store
            SET number_of_copies = number_of_copies - ?
            WHERE Game = ? AND Form_of_copy = ?"""
        args = [amount,game,type]
        
        cost = Cost(_conn,game,amount,type)

        cur = _conn.cursor()
        cur.execute(sql,args)
        _conn.commit()
        sql = """UPDATE Customer
            SET amount = amount - ?
            WHERE name = ?"""
        args = [cost,username]
        
        cur = _conn.cursor()
        cur.execute(sql,args)
        _conn.commit()
    except Error as e:
        print(e)

def developing(_conn,name):
    print("Developing")
    game = input("Game: ")
    genre = input("Genre: ")
    year = input("Year: ")
    mode = input("Mode: ")
    try:
        sql = "INSERT INTO Game VALUES(?, ?, ?,?,?,?,?)"
        args = [game,genre,year,"null",mode,"null",name]
        
        cur = _conn.cursor()
        cur.execute(sql,args)
        _conn.commit()

    except Error as e:
        print(e)
    return game

def publishers(_conn):
    print("\nPublishers: ")
    try:    
        sql = """Select name
            from Publisher"""
            
        cur = _conn.cursor()
        cur.execute(sql)
        _conn.commit() 

        rows = cur.fetchall()
        for row in rows:
            print(row[0])
        check = True
        while(check):
            publisher = input("Enter the name of one: ")
            sql = """SELECT EXISTS(SELECT 1 
                    FROM Publisher WHERE 
                    name = ? );"""
            args = [publisher]

            cur = _conn.cursor()
            cur.execute(sql,args)

            rows = int(cur.fetchone()[0])
            if(rows == 1):
                check = False
            else:
                value = input("Publisher does not exist try again(t) or exit(e): ")
                if(value == "e"):
                    return 0
    except Error as e:
        print(e)        
    return publisher

def develop_catalog(_conn,developer):
    print("Games developed:")
    try:
        sql = """SELECT name
                FROM Game 
                WHERE Developer = ?"""
        args = [developer]
        cur = _conn.cursor()
        cur.execute(sql,args)

        rows = cur.fetchall()
        for row in rows:
            print(row[0])
    except Error as e:
        print(e)      

def publishing(_conn,game,developer):
    print("Publishing")
    value = input("Self publish(s) or through a company(c)")
    try:
        if(value == "s"):
            platform = input("Platform: ")
            sql = """UPDATE Game
            SET Platform = ?, Publisher = ?
            WHERE name = ?"""
            args = [platform,developer,game]
            
            cur = _conn.cursor()
            cur.execute(sql,args)
            _conn.commit()

        elif(value == "c"):
            publisher = publishers(_conn)
            platform = input("Platform: ")
            sql = """UPDATE Game
            SET Platform = ?, Publisher = ?
            WHERE name = ?"""
            args = [platform,publisher,game]
            
            cur = _conn.cursor()
            cur.execute(sql,args)
            _conn.commit()
    except Error as e:
        print(e)


def Creating_acc(_conn):
    print("\nMaking account")
    name = input("Name: ")
    amount = input("Amount: ")
    location = input("loaction: ")

    try:
        sql = "INSERT INTO Customer VALUES(?, ?, ?,0)"
        args = [name,amount,location]

        cur = _conn.cursor()
        cur.execute(sql,args)
        _conn.commit()

    except Error as e:
        print(e)
    return name
    
def logg_in(_conn,username):
    print("\nChecking account")
    try:
        sql = """SELECT EXISTS(SELECT 1 
                FROM Customer WHERE 
                name = ? );"""
        args = [username]

        cur = _conn.cursor()
        cur.execute(sql,args)

        rows = int(cur.fetchone()[0])

        value = rows

    except Error as e:
        print(e)
    return value

def logg_ing(_conn,ID):
    print("\nChecking account")
    try:
        sql = """SELECT EXISTS(SELECT 1 
                FROM employee WHERE 
                employee_id = ? );"""
        args = [ID]

        cur = _conn.cursor()
        cur.execute(sql,args)

        rows = int(cur.fetchone()[0])

        value = rows
        if(value == 1):
            sql = """SELECT name
                    FROM employee WHERE 
                    employee_id = ?"""
            args = [ID]

            cur = _conn.cursor()
            cur.execute(sql,args)

            row = cur.fetchone()[0]           
            print(row + " logged in")
    
    except Error as e:
        print(e)
    return value

def main():
    database = r"Video_store.sqlite"
    # create a database connection
    conn = openConnection(database)
    

    user = input("customer(c) or employee(e) or developer(d): ")
    if(user not in ['c','e','d','p']):
        In = False
        print("user not recognized")
    else:
        In = True

    if(user == "c"):
        siging_in = True
        while(siging_in):
            c_login = input("login(l) or Create account(c):")
            if(c_login == "c"):
                c_acc = Creating_acc(conn)
                siging_in = False
            if(c_login == "l"):
                c_acc = input("Username: ")
                value = logg_in(conn,c_acc)
                if(value == 0):
                    print("Account does not exist\n")
                    status = input("Try Again(t) or leave(n):")
                    if(status in ['N','n']): 
                        siging_in = False
                        In = False
                elif(value == 1):
                    print("Logged in\n")
                    siging_in = False
    if(user == "e"):
        siging_in = True
        while(siging_in):
            ID = input("Employee ID: ")
            value = logg_ing(conn,ID)
            if(value == 0):
                print("Account does not exist\n")
                status = input("Try Again(t) or leave(n):")
                if(status in ['N','n']): 
                    siging_in = False
                    In = False
            elif(value == 1):
                siging_in = False

    if(user == "d"):
        In == False
        Develop = True
        d_acc = input("Studio: ")
        while(Develop):
            with conn:
                action = input("Actions:\nGames developed(g)\ndevelop a game(d)\n")
                if(action == "d"):
                    game = developing(conn,d_acc)
                    publishing(conn,game,d_acc)
                elif(action == 'g'):
                    develop_catalog(conn,d_acc)
                else:
                    print("command not recognized")
                status = input("Stay logged in Y or N:")
                if(status in ['N','n']): 
                    Develop = False
               

    while(In):
        with conn:
            if(user == "e"):
                action = input("Actions:\nCheck Inventory(c)\nAdd to Inventory(a)\n")
                if(action == 'c'):
                    Inventory(conn)
                elif(action == 'a'):
                    stock = input("Actions:\nAdd a new game(n)\nReplenish Inventory(r)\n")
                    if(stock == 'n'):
                        game = game_catalog(conn)
                        if(game != 0):                     
                            Add_to_Inventory(conn,game,0)
                    elif(stock == 'r'):
                        Inventory(conn)
                        game = input("Game: ")
                        Add_to_Inventory(conn,game,1)
                elif(action == 'Delete'):
                    Empty(conn)
                else:
                    print("command not recognized")
                status = input("Stay logged in Y or N:")
                if(status in ['N','n']):
                    In = False
            elif(user == "c"):
                action = input("Actions:\nSearch for a game(g)\nBuy a game(b)\n")
                if(action == 'g'):
                    search(conn)
                elif(action == 'b'):
                    Buy(conn,c_acc)
                else:
                    print("command not recognized")
                status = input("Stay logged in Y or N:")
                if(status in ['N','n']):
                    In = False
            else:
                In = False

    closeConnection(conn, database)


if __name__ == '__main__':
    main()