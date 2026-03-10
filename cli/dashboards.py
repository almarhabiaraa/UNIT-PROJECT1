# cli/dashboards.py
from services.booking_wizard import booking_wizard
from services.booking_queries import view_my_bookings
from database.db_connection import get_connection
from services.admin_services import (
    manage_bookings, manage_services, manage_venues, manage_catering, generate_reports
)

# -------------------------
# CLIENT DASHBOARD
# -------------------------
def client_dashboard(user):
    while True:
        print("\n--- Client Dashboard ---")
        print("1. Create New Booking")
        print("2. View My Bookings")
        print("3. Delete Account")
        print("4. Logout")

        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            booking_wizard(user)  
        elif choice == "2":
            view_my_bookings(user)
        elif choice == "3":
            confirm = input("Are you sure you want to delete your account? (y/n): ").lower()
            if confirm == "y":
                conn = get_connection()
                cursor = conn.cursor()
                
                # Delete user's bookings first
                cursor.execute("DELETE FROM bookings WHERE user_id = ?", (user["id"],))
                
                # Delete the user account
                cursor.execute("DELETE FROM users WHERE id = ?", (user["id"],))
                
                conn.commit()
                conn.close()
                
                print("Your account and all related bookings have been deleted successfully.")
                break  # Exit dashboard after deletion
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

# -------------------------
# ADMIN DASHBOARD
# -------------------------
def admin_dashboard(user):
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Manage Bookings")
        print("2. Manage Services")
        print("3. Manage Venues")
        print("4. Manage Catering Menus")
        print("5. Reports")
        print("6. Logout")

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            manage_bookings()
        elif choice == "2":
            manage_services()
        elif choice == "3":
            manage_venues()
        elif choice == "4":
            manage_catering()
        elif choice == "5":
            generate_reports()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")