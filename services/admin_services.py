# services/admin_services.py
from database.db_connection import get_connection
from tabulate import tabulate
from datetime import datetime

# -------------------------
# BOOKINGS MANAGEMENT
# -------------------------
def manage_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.id, u.full_name, b.event_name, b.event_date, b.start_time, b.end_time,
               b.num_guests, b.total_price, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.event_date ASC
    """)
    bookings = cursor.fetchall()
    
    if not bookings:
        print("No bookings found.")
        conn.close()
        return
    
    table = []
    for b in bookings:
        table.append([
            b["id"], b["full_name"], b["event_name"], b["event_date"],
            f"{b['start_time']} - {b['end_time']}", b["num_guests"],
            f"{b['total_price']} SAR", b["status"].capitalize()
        ])
    print(tabulate(table, headers=["ID", "Client", "Event", "Date", "Time", "Guests", "Total", "Status"], tablefmt="grid"))
    
    choice = input("\nEnter Booking ID to Approve/Reject or 'b' to go back: ").strip()
    if choice.lower() == "b":
        conn.close()
        return
    
    cursor.execute("SELECT * FROM bookings WHERE id = ?", (choice,))
    booking = cursor.fetchone()
    if not booking:
        print("Invalid Booking ID.")
        conn.close()
        return
    
    action = input("Approve (a) / Reject (r) / Cancel (c): ").lower()
    if action == "a":
        cursor.execute("UPDATE bookings SET status='approved' WHERE id=?", (choice,))
        print("Booking approved!")
    elif action == "r":
        cursor.execute("UPDATE bookings SET status='rejected' WHERE id=?", (choice,))
        print("Booking rejected!")
    else:
        print("No changes made.")
    
    conn.commit()
    conn.close()

# -------------------------
# SERVICES MANAGEMENT
# -------------------------
def manage_services():
    conn = get_connection()
    cursor = conn.cursor()
    while True:
        print("\n--- Manage Services ---")
        print("1. Add Service")
        print("2. Update Service")
        print("3. Delete Service")
        print("4. View Services")
        print("5. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Service Name: ").strip()
            price = float(input("Price: "))
            cursor.execute("INSERT INTO services (name, price) VALUES (?, ?)", (name, price))
            conn.commit()
            print("Service added successfully!")

        elif choice == "2":
            cursor.execute("SELECT * FROM services")
            services = cursor.fetchall()
            for s in services:
                print(f"{s['id']}. {s['name']} - {s['price']} SAR")
            sid = input("Enter Service ID to update: ").strip()
            new_name = input("New Name: ").strip()
            new_price = float(input("New Price: "))
            cursor.execute("UPDATE services SET name=?, price=? WHERE id=?", (new_name, new_price, sid))
            conn.commit()
            print("Service updated successfully!")

        elif choice == "3":
            cursor.execute("SELECT * FROM services")
            services = cursor.fetchall()
            for s in services:
                print(f"{s['id']}. {s['name']} - {s['price']} SAR")
            sid = input("Enter Service ID to delete: ").strip()
            cursor.execute("DELETE FROM services WHERE id=?", (sid,))
            conn.commit()
            print("Service deleted successfully!")

        elif choice == "4":
            cursor.execute("SELECT * FROM services")
            services = cursor.fetchall()
            table = [[s["id"], s["name"], s["price"]] for s in services]
            print(tabulate(table, headers=["ID", "Service", "Price"], tablefmt="grid"))

        elif choice == "5":
            break
        else:
            print("Invalid option.")
    conn.close()

# -------------------------
# VENUES MANAGEMENT
# -------------------------
def manage_venues():
    conn = get_connection()
    cursor = conn.cursor()
    while True:
        print("\n--- Manage Venues ---")
        print("1. Add Venue")
        print("2. Update Venue")
        print("3. Delete Venue")
        print("4. View Venues")
        print("5. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Venue Name: ").strip()
            price = float(input("Price per Hour: "))
            cursor.execute("INSERT INTO venues (name, price_per_hour) VALUES (?, ?)", (name, price))
            conn.commit()
            print("Venue added successfully!")

        elif choice == "2":
            cursor.execute("SELECT * FROM venues")
            venues = cursor.fetchall()
            for v in venues:
                print(f"{v['id']}. {v['name']} - {v['price_per_hour']} SAR/hr")
            vid = input("Enter Venue ID to update: ").strip()
            new_name = input("New Name: ").strip()
            new_price = float(input("New Price per Hour: "))
            cursor.execute("UPDATE venues SET name=?, price_per_hour=? WHERE id=?", (new_name, new_price, vid))
            conn.commit()
            print("Venue updated successfully!")

        elif choice == "3":
            cursor.execute("SELECT * FROM venues")
            venues = cursor.fetchall()
            for v in venues:
                print(f"{v['id']}. {v['name']} - {v['price_per_hour']} SAR/hr")
            vid = input("Enter Venue ID to delete: ").strip()
            cursor.execute("DELETE FROM venues WHERE id=?", (vid,))
            conn.commit()
            print("Venue deleted successfully!")

        elif choice == "4":
            cursor.execute("SELECT * FROM venues")
            venues = cursor.fetchall()
            table = [[v["id"], v["name"], v["price_per_hour"]] for v in venues]
            print(tabulate(table, headers=["ID", "Venue", "Price/hr"], tablefmt="grid"))

        elif choice == "5":
            break
        else:
            print("Invalid option.")
    conn.close()

# -------------------------
# CATERING MENUS MANAGEMENT
# -------------------------
def manage_catering():
    conn = get_connection()
    cursor = conn.cursor()
    while True:
        print("\n--- Manage Catering Menus ---")
        print("1. Add Menu")
        print("2. Update Menu")
        print("3. Delete Menu")
        print("4. View Menus")
        print("5. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Menu Name: ").strip()
            price = float(input("Price per Person: "))
            cursor.execute("INSERT INTO catering_menus (name, price_per_person) VALUES (?, ?)", (name, price))
            conn.commit()
            print("Menu added successfully!")

        elif choice == "2":
            cursor.execute("SELECT * FROM catering_menus")
            menus = cursor.fetchall()
            for m in menus:
                print(f"{m['id']}. {m['name']} - {m['price_per_person']} SAR/person")
            mid = input("Enter Menu ID to update: ").strip()
            new_name = input("New Name: ").strip()
            new_price = float(input("New Price per Person: "))
            cursor.execute("UPDATE catering_menus SET name=?, price_per_person=? WHERE id=?", (new_name, new_price, mid))
            conn.commit()
            print("Menu updated successfully!")

        elif choice == "3":
            cursor.execute("SELECT * FROM catering_menus")
            menus = cursor.fetchall()
            for m in menus:
                print(f"{m['id']}. {m['name']} - {m['price_per_person']} SAR/person")
            mid = input("Enter Menu ID to delete: ").strip()
            cursor.execute("DELETE FROM catering_menus WHERE id=?", (mid,))
            conn.commit()
            print("Menu deleted successfully!")

        elif choice == "4":
            cursor.execute("SELECT * FROM catering_menus")
            menus = cursor.fetchall()
            table = [[m["id"], m["package_type"], m["meal_type"], m["price_per_person"]] for m in menus]
            print(tabulate(table, headers=["ID", "Menu", "Price/person"], tablefmt="grid"))

        elif choice == "5":
            break
        else:
            print("Invalid option.")
    conn.close()

# -------------------------
# REPORTS - BOOKINGS SUMMARY BY STATUS 
# -------------------------
def generate_reports():
    conn = get_connection()
    cursor = conn.cursor()
    print("\n--- Reports ---")
    cursor.execute("SELECT status, COUNT(*) as count FROM bookings GROUP BY status")
    rows = cursor.fetchall()
    for r in rows:
        print(f"{r['status'].capitalize()}: {r['count']}")
    conn.close()