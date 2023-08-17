Tableway: Restaurant Booking & Payment System 🍽️

Tableway is a comprehensive restaurant management system built with Django and Django Rest Framework. It streamlines the process of making reservations, handling payments, and managing restaurant operations.

Features 🌟

1. User Authentication
Secure user registration and login functionality.
Distinct roles for customers, restaurant owners, and employees.
2. Reservation Management
Users can make, view, and manage their reservations.
Real-time table availability checks.
3. Payment System
Integrated payment system allowing users to make payments for their reservations.
Secure transaction processing.
4. Tip Management
Users can give tips to employees.
Employees can view and manage their tips.
5. Admin Dashboard
Comprehensive admin functionalities for managing restaurant details, tables, and employees.
Real-time data visualization for better decision-making.
Technologies Used 🛠️

Backend: Django, Django Rest Framework
Database: PostgreSQL
Task Queue: Celery (for asynchronous tasks)
Others: Redis, Docker


# Tableway
### more details soon ###
Actually working on app basics. 

29.04.2023 Update
- Basic reservation funcionality is almost done. 
- User/Restaurant/Tables/Reservation models are done. 
- No tokenization, authentication and authorisation yet (will be done next).
- Payments app is currently in "initial phase". 
- Currently working on possibility to create list of reservation connect to one table (now table can only contain one reservation) [DONE]. 
- Actually fixing Country/ City field (user not able to choose) [DONE] and writing some tests. 
- 20.05.2023 App is in tests phase.
- 30.05.2023 Tests phase for bookings app is almost done [need few more fixes].
- App is in final tests phase and funcionality check.
- App release will be delay, still working with tests and some bugfixes. 
- More updates coming soon. I am on vacations!
- This update is needed only to keep up my challange to code for 365 days in a row (even if i am on vacations, like right now). [v8]
- Now working on last test phase (last touches on tests).
- Celery will be added as a new feature in near future! (working on that now).
- Full docker deployment will be ready soon. 
Last test phase on basic funcionility is complete. Now working on Celery and Redis.
Test phase is successfully ended.
Readis and Celery is also added but couple of fixes is needed. After that next phase will start which is deployment!
