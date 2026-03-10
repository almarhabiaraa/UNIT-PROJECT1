from database.db_connection import get_connection
from tabulate import tabulate
from datetime import datetime

# --- Helper functions ---
def format_time_12h(time_str):
    """Convert 'HH:MM' to 12-hour format with AM/PM"""
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M %p")

def format_date_day(date_str):
    """Return date string with day name, e.g., '2026-03-10 (Wednesday)'"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    day_name = date_obj.strftime("%A")
    return f"{date_str} ({day_name})"

# --- Main function ---
def view_my_bookings(user):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, event_name, event_date, start_time, end_time, num_guests, total_price, status
        FROM bookings
        WHERE user_id = ?
        ORDER BY event_date ASC
    """, (user["id"],))
    
    bookings = cursor.fetchall()
    if not bookings:
        print("\nYou have no bookings yet. Create your first booking!\n")
        conn.close()
        return
    
    # Display bookings in a table
    table_data = []
    for b in bookings:
        table_data.append([
            b["id"],
            b["event_name"],
            format_date_day(b["event_date"]),
            f"{format_time_12h(b['start_time'])} - {format_time_12h(b['end_time'])}",
            b["num_guests"],
            f"{b['total_price']} SAR",
            b["status"].capitalize()
        ])
    
    print("\n--- My Bookings ---")
    print(tabulate(
        table_data,
        headers=["ID", "Event", "Date", "Time", "Guests", "Total Price", "Status"],
        tablefmt="grid"
    ))

    # Ask if user wants to cancel a booking (only if pending and more than 24 hours before event)
    cancel = input("\nDo you want to cancel any booking? (y/n): ").lower()
    if cancel == "y":
        booking_id = input("Enter the Booking ID to cancel: ").strip()
        # Verify booking belongs to user and is pending
        selected_booking = next((b for b in bookings if str(b["id"]) == booking_id), None)
        if not selected_booking:
            print("Booking ID not found.")
        else:
            # Check if booking is pending 
            event_datetime = datetime.strptime(selected_booking["event_date"] + " " + selected_booking["start_time"], "%Y-%m-%d %H:%M")
            time_left = event_datetime - datetime.now()
            if time_left.total_seconds() < 3*24*3600:  # 3 days
                print("Sorry, you cannot cancel a booking within 72 hours of the event.")
            else:
                confirm = input(f"Are you sure you want to cancel '{selected_booking['event_name']}'? (y/n): ").lower()
                if confirm == "y":
                    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
                    conn.commit()
                    print("Booking cancelled successfully.")
                else:
                    print("Cancellation aborted.")

    conn.close()