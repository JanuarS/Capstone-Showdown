Capstone: Showdown-App

API: www.7timer.info Free weather api with no authentication needed. 
Display temp information and chance of rain underneath nav bar.

Schema Design: 

Schools Table:
School code (primary key) 
School name
City
State

Users Table:
ID (primary key)
First name
Last name
Gener
School_code (foreign key to Schools table)
Email 
Password

Knowledge Bowl:
ID (primary key
Competition name
School code (foreign key to schools table)
Captain (foreign key to users table)
Player 2 (foreign key to users table)
Player 3 (foreign key to users table)
Player 4 (foreign key to users table)


Basketball Table:
ID (primary key)
Competition name
Gender (Men’s/Women’s)
School code (foreign to schools table
Captain (foreign key to users table)
Player 2 (foreign key to users table)
Player 3 (foreign key to users table)
Player 4 (foreign key to users table)
Player 5 (foreign key to users table)
Player 6 (foreign key to users table)
Player 7 (foreign key to users table)
Player 8 (foreign key to users table)
Player 9 (foreign key to users table)
Player 10 (foreign key to users table)

Spoken Word:
ID (primary key)
Competition name
School code (foreign key to schools table)
Player 1 (foreign key to users table)
Player 2 (foreign key to users table)
Player 3 (foreign key to users table)

