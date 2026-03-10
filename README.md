#  UNIT-PROJECT-1 Happy Moments Planner 🎉

## Project Overview
**Happy Moments Planner** is a role-based Command Line Interface (CLI) system designed to help clients and event organizers plan, manage, and organize events seamlessly.  
The system guides users step-by-step through the booking process, allowing them to select venues, catering, services, and more. All data is persistently stored in a SQLite database for reliability.  

The system supports two main roles:  
- **Client** – Can create and manage bookings.  
- **Admin** – Can manage services, venues, catering menus, view reports, and oversee all bookings.  

---

## Project Structure


```
HappyMomentsPlanner/
│
├─ cli/ # CLI interface for user interactions
├─ database/ # Database connection and seed data
├─ services/ # Business logic and service handlers
├─ .gitignore # Git ignore file
├─ README.md # Project documentation
├─ main.py # Entry point for the CLI system
├─ moments_planner.db # SQLite database file
├─ requirements.txt # Python dependencies
└─ .DS_Store
```

---

## Main Features

- **User Authentication**
  - Sign up and login with hashed passwords
  - Role-based access (Client / Admin)

- **Event Booking Wizard**
  - Step-by-step event booking for clients
  - Select event type, category, venue, catering, cake, coffee corners, services, giveaways
  - Real-time calculation of total price

- **Admin Dashboard**
  - Manage bookings, services, venues, and catering menus
  - View detailed reports
  - Update, add, or delete entries

- **Database Integration**
  - Persistent storage using SQLite
  - Pre-populated seed data for services, venues, menus, and coffee corners

---
## User Stories

- **As a Client**:
  - I want to create a new booking for an event.
  - I want to choose a venue, catering menu, and additional services.
  - I want to see the total price as I select services.
  - I want to see my previous bookings.
  - I want to cancel any of my bookings.
  - I want to delete my account.

- **As an Admin**:
  - I want to manage available services, venues, and menus (CRUD: create, read, update, delete).
  - I want to view all client bookings.
  - I want to approve or reject a client booking.
  - I want to generate simple reports on bookings and revenue.
    
 ---

## Installation & Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd HappyMomentsPlanner
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```
