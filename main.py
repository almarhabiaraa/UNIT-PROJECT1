# main.py - main entry point for Happy Moments Planner CLI

from services.auth_service import signup, login
from cli.dashboards import client_dashboard, admin_dashboard
from database.seed_data import seed_data



def main():
    print("=== Welcome to Moments Planner CLI ===")
    
    # Seed default admin account
    seed_data()

    while True:
        print("\n1. Sign Up")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            full_name = input("Full Name: ").strip()
            phone_number = input("Phone Number: ").strip()
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            signup(full_name, phone_number, username, email, password)

        elif choice == "2":
            identifier = input("Username or Email: ").strip()
            password = input("Password: ").strip()
            user = login(identifier, password)

            if user:
                print(f"Welcome, {user['full_name']}!")
                if user["role"] == "admin":
                    admin_dashboard(user)
                else:
                    client_dashboard(user)
            else:
                print("Login failed. Check your credentials.")

        elif choice == "3":
            print("Exiting Moments Planner. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()