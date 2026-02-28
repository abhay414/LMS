import mysql.connector           #MYSQL CONNECTION
import pywhatkit
c=mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD"
    )
cursor = c.cursor()              #CURSOR=IT ALLOW PYTHON CODE TO EXECUTE SQL COMMAND IN A DATABASE SESSION(IT ACTUALLY POINTS TO RESULT,DATA ETC)
cursor.execute("create database if not exists library")#TO CREATE DATABASE IF IT DOES NOT EXIST
cursor.execute("use library")
cursor.execute("create table if not exists books(id int not null primary key,title varchar(65) not null,author varchar(65) not null,genre varchar(50))")#TO CREATE TABLE BOOKS
cursor.execute("create table if not exists  members(id int not null primary key,name_m varchar(100) not null,phoneno varchar(13) not null,email varchar(100))")#TO CREATE TABLE MEMBERS
cursor.execute("create table if not exists issuedbook(member_id int not null,book_id int not null,name varchar(100) not null,issue_date date,return_date date,reminder_sent TINYINT(1) DEFAULT(0),foreign key (book_id) references books(id),foreign key (member_id) references members(id))")


def add_new_book():              #TO ADD NEW BOOK
    id=int(input("ENTER BOOK ID:"))
    b_query="select id from books where id=%s"
    cursor.execute(b_query,(id,))#EXECUTE()=TO EXECUTE QUERY IN MYSQL
    ext_book=cursor.fetchone()
    if ext_book:
        print("***BOOK ALREADY EXIST***")
    else:
        title=input("ENTER BOOK TITLE:")
        author=input("ENTER NAME OF THE AUTHOR:")
        genre=input("ENTER GENRE OF BOOK:")
        query="insert into books(id,title,author,genre) values(%s,%s,%s,%s)"
        values=(id,title,author,genre)

        cursor.execute(query,values)#QUERY IS A MENDATORY ARGUMENT AND WILL BE IN THE FORM OF STRING
        c.commit()                  #COMMIT()=USED TO SAVE INSERTED ROW IN THE TABLE,IT IS REQUIRED TO MAKE THE CHANGES OTHERWISE NO CHANGES ARE MADE TO THE TABLE
        print("***BOOK IS ADDED***")#AUTOCOMMIT() IS AVAILABLE IN SQL BUT WE CANNOT USE IT THROUGH PYTHON SCRIPT


def view_books():                   #TO VIEW BOOKS SAVED IN BOOKS TABLE
    cursor.execute("select * from books")
    result=cursor.fetchall()
    if result:
        print("\n================= BOOKS TABLE =================")
        print(f"{'ID':<10}{'TITLE':<30}{'AUTHOR':<25}{'GENRE':<20}")
        print("-"*90)
        for r in result:
            print(f"{r[0]:<10}{r[1]:<30}{r[2]:<25}{r[3]:<20}")
        print("-"*90)
    else:
        print("***NO BOOKS AVAILABLE***")


import datetime                    
def new_member_details():          #TO ADD NEW MEMBER
    id=int(input("ENTER MEMBER ID:"))
    m_query="select id from members where id=%s" #%S=PLACE HOLDER
    cursor.execute(m_query,(id,))
    mem=cursor.fetchone()
    if mem:
        print("***MEMBER ALREADY EXIST***")
    else:
        name=input("ENTER MEMBER'S NAME:")
        phone=input("ENTER MEMBER'S CONTACT NUMBER:")
        email=input("ENTER MEMBER'S EMAIL ID:")
        query="insert into members(id,name_m,phoneno,email) values(%s,%s,%s,%s)"
        values=(id,name,phone,email)
        cursor.execute(query,values)
        c.commit()
        print("***MEMBER IS ADDED***")


def view_members():                #TO VIEW MEMBERS SAVED IN MEMBERS TABLE
    cursor.execute("select * from members")
    result=cursor.fetchall()
    if result:
        print("\n================= MEMBERS TABLE =================")
        print(f"{'ID':<10}{'NAME':<30}{'PHONE':<20}{'EMAIL':<30}")
        print("-"*100)
        for r in result:
            print(f"{r[0]:<10}{r[1]:<30}{r[2]:<20}{r[3]:<30}")
        print("-"*100)
    else:
        print("***NO MEMBER***")


def issue_bookes():               #TO ISSUE A BOOK
    member_id=int(input("ENTER MEMBER ID:"))
    book_id=int(input("ENTER BOOK ID:"))
    cursor.execute("select * from members where id=%s",(member_id,))
    if cursor.fetchone() is None:
        print("***NO SUCH MEMBER***")
        return
    cursor.execute("select *from books where id=%s",(book_id,))
    if cursor.fetchone() is None:
        print("***NO SUCH BOOK***")
        return
    name=input("ENTER NAME OF STUDENT:")
    issue_date=datetime.date.today() #RETURN CURRENT DATE OF THE SYSTEM
    query="insert into issuedbook(member_id,book_id,name,issue_date) values(%s,%s,%s,%s)"
    values=(member_id,book_id,name,issue_date)

    cursor.execute(query,values)
    c.commit()
    print("***BOOK ISSUED***")


def return_bookes():            #TO RETURN BOOK
     member_id=int(input("ENTER MEMBER ID:"))
     book_id=int(input("ENTER BOOK ID:"))
     return_date=datetime.date.today()
     update="""update issuedbook set return_date=%s where member_id=%s
     and book_id=%s and return_date is null"""
     values=(return_date,member_id,book_id)
     cursor.execute(update,values)
     c.commit()
     if cursor.rowcount>0:
         print("***RETURN DATE UPDATED SUCCESSFULLY***")
     else:
         print("***NO MATCHING RECORD FOUND OR BOOK IS RETURNED***")


def view_issued_books():       #TO VIEW ISSUED/RETURNED BOOKS HISTORY
    cursor.execute("select * from issuedbook")
    result=cursor.fetchall()
    if result:
        print("\n================= ISSUED BOOKS TABLE =================")
        print(f"{'MEMBER_ID':<12}{'BOOK_ID':<10}{'NAME':<25}{'ISSUE_DATE':<15}{'RETURN_DATE':<15}{'REMINDER':<10}")
        print("-"*110)
        for r in result:
            print(f"{r[0]:<12}{r[1]:<10}{r[2]:<25}{str(r[3]):<15}{str(r[4]):<15}{str(r[5]):<10}")
        print("-"*110)
    else:
        print("***NO BOOK IS ISSUED***")


def not_returned_books():     #TO VIEW NOT RETURNED BOOKS
    query=""" select m.name_m,m.phoneno,b.title,i.issue_date 
              from issuedbook i
              join members m on i.member_id=m.id
              join books b on i.book_id=b.id
              where i.return_date is null
              order by i.issue_date"""
    cursor.execute(query)
    result=cursor.fetchall()
    if result:
         print("\n================= NOT RETURNED BOOKS =================")
         print(f"{'NAME':<30}{'PHONE':<18}{'BOOK TITLE':<30}{'ISSUE DATE':<15}")
         print("-"*100)
         for r in result:
             print(f"{r[0]:<30}{r[1]:<18}{r[2]:<30}{str(r[3]):<15}")
         print("-"*100)
    else:
        print("***ALL BOOKS HAVE BEEN RETURNED***")


def delete_mem():           #TO DELETE A MEMBER
    id=int(input("ENTER MEMBER ID TO DELETE:"))
    cursor.execute("select * from members where id=%s",(id,))
    member=cursor.fetchone()
    if not member:
        print("***NO SUCH MEMBER***")
        return
    cursor.execute("select * from issuedbook where member_id=%s and return_date is null",(id,))
    issued_book=cursor.fetchall()
    if issued_book:
        print("***CANNOT DELETE THIS MEMBER THERE ARE BOOKS THAT HAVE NOT RETURNED***")
        return
    cursor.execute("delete from issuedbook where member_id=%s",(id,))
    cursor.execute("delete from members where id=%s",(id,))
    c.commit()
    print("***MEMBER DELETED SUCCESSFULLY***")


def delete_book():        #TO DELETE A BOOK
    id=int(input("ENTER BOOK ID TO DELETE:"))
    cursor.execute("select * from books where id=%s",(id,))
    book=cursor.fetchall()
    if book:
        cursor.execute("delete from books where id=%s",(id,))
        c.commit()
        print(f"***BOOK_ID:{id} DELETED SUCCESSFULLY***")
    else:
        print("***NO SUCH BOOK***")


from datetime import date

from datetime import date
def wattsaap():
    today = date.today()
    c = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhay.1111",
        database="library"
    )
    cursor = c.cursor(dictionary=True)

    query = """
        SELECT m.name_m, m.phoneno, b.title, i.issue_date, m.id AS member_id
        FROM issuedbook i
        JOIN members m ON i.member_id = m.id
        JOIN books b ON b.id = i.book_id
        WHERE 
            i.return_date IS NULL 
            AND DATEDIFF(CURDATE(), i.issue_date) > 15 """
    
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        issue_date = row["issue_date"]
        phone = row["phoneno"]

        message = (
            f"Hello {row['name_m']},\n"
            f"Your book '{row['title']}' is overdue by more than 15 days "
            f"(Issued on {issue_date}). Please return it immediately."
        )

        if not phone.startswith("+"):
            phone = "+91" + phone

        try:
            pywhatkit.sendwhatmsg_instantly(
                phone,
                message,
                wait_time=10,
                tab_close=True
            )

            cursor.execute(
                "UPDATE issuedbook SET reminder_sent=1 WHERE member_id=%s",
                (row['member_id'],)
            )
            c.commit()
            print(f"Message sent to {row['name_m']}")

        except Exception as e:
            print(f"Failed to send message to {phone}: {e}")

    cursor.close()
    c.close()



while True:
    print("*****WELCOME TO LIBRARY MANAGEMENT SYSTEM*****")#
    print("1=ADD NEW BOOK")                                  #
    print("2=VIEW BOOKS")                                      #
    print("3=ADD NEW MEMBER")                                   #
    print("4=VIEW MEMBER DETAILS")                               #
    print("5=ISSUE BOOKS")                                         #               
    print("6=TO VIEW ISSUED/RETURNED BOOKS HISTORY")                 # TO PRINT ALL CHOICES USER CAN HAVE
    print("7=TO RETURN BOOK")                                      #
    print("8=TO VIEW NOT RETURNED BOOKS")                        #
    print("9=TO DELETE MEMBER")                                #
    print("10=TO DELETE BOOK")                               #
    print("11=Text all members who have books")
    print("12=Exit")
    choice=input("ENTER CHOICE:")                       

    if(choice=='1'):            #
        add_new_book()           #
    elif(choice=='2'):            #
        view_books()               #
    elif(choice=='3'):              #
        new_member_details()         #
    elif(choice=='4'):                #
        view_members()                 #
    elif(choice=='5'):                  #
        issue_bookes()                   #
    elif(choice=='6'):                    #
        view_issued_books()                #TO CALL FUNCTIONS
    elif(choice=='7'):                     #BASED ON USER INPUT
        return_bookes()                   #
    elif(choice=='8'):                   #
        not_returned_books()            #
    elif(choice=='9'):                 #
        delete_mem()                  #
    elif(choice=='10'):              #
        delete_book()               #
    elif(choice=='11'):            #
        wattsaap()
    elif(choice=='12'):
        break
    else:                        #
        print("INVALID CHOICE")#

