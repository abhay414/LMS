Library Management System

A simple, no-frills command-line Library Management System built with Python and MySQL. It handles the everyday stuff a small library needs — adding books, registering members, issuing and returning books, tracking overdue returns, and even sending WhatsApp reminders to members who are holding onto a book for too long.

No GUI, no fluff — just a menu-driven terminal app that gets the job done.


Features


Book management — add new books, view the full catalog
Member management — register new members, view member details, delete a member (only if they have no unreturned books)
Issuing & returning — issue a book to a member, mark books as returned
History tracking — view the full issue/return history, and see which books are still out
Overdue reminders — automatically finds members who've had a book for more than 15 days and sends them a WhatsApp message via pywhatkit
Safety checks built in — you can't delete a member with outstanding books, duplicate IDs are blocked, and every table uses proper foreign keys



Tech Stack


Python 3
MySQL (via mysql-connector-python)
pywhatkit (for sending WhatsApp reminders)



Requirements

Install the required Python packages:

bashpip install mysql-connector-python pywhatkit

You'll also need:


A running MySQL server (local install is fine)
WhatsApp Web logged in on your default browser, if you want to use the reminder feature (pywhatkit opens WhatsApp Web to send messages)



Setup


Clone or download this project.
Configure your database credentials. Open the script and update the connection details near the top:


python   c = mysql.connector.connect(
       host="localhost",
       user="root",
       password="YOUR_PASSWORD"
   )

Note: Don't commit your real password. For anything beyond local testing, pull it from an environment variable instead of hardcoding it — see Notes below.


Run the script:


bash   python library.py

The database (library) and all required tables (books, members, issuedbook) are created automatically the first time you run it — no manual SQL setup needed.


Database Schema

books

ColumnTypeNotesidINTPrimary keytitleVARCHAR(65)authorVARCHAR(65)genreVARCHAR(50)

members

ColumnTypeNotesidINTPrimary keyname_mVARCHAR(100)phonenoVARCHAR(13)emailVARCHAR(100)

issuedbook

ColumnTypeNotesmember_idINTForeign key → members.idbook_idINTForeign key → books.idnameVARCHAR(100)Name of the person the book was issued toissue_dateDATEreturn_dateDATENULL until returnedreminder_sentTINYINT(1)Defaults to 0, flips to 1 once a WhatsApp reminder goes out


Usage

Run the script and you'll get a menu like this:

*****WELCOME TO LIBRARY MANAGEMENT SYSTEM*****
1 = ADD NEW BOOK
2 = VIEW BOOKS
3 = ADD NEW MEMBER
4 = VIEW MEMBER DETAILS
5 = ISSUE BOOKS
6 = VIEW ISSUED/RETURNED BOOKS HISTORY
7 = RETURN BOOK
8 = VIEW NOT RETURNED BOOKS
9 = DELETE MEMBER
10 = DELETE BOOK
11 = TEXT ALL MEMBERS WHO HAVE OVERDUE BOOKS
12 = EXIT

Just type the number of the action you want and follow the prompts. IDs are entered manually, so keep track of which book/member IDs you've already used.

About option 11 — WhatsApp reminders

This checks the issuedbook table for anyone who has held a book for more than 15 days without returning it, and sends them a WhatsApp message using their phone number (auto-prefixed with +91 if no country code is given). Each message triggers pywhatkit to briefly open WhatsApp Web in your browser — make sure you're logged in beforehand, and don't touch the keyboard/mouse while it's sending.