# database/create_tables.py
from database.db_connection import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('client','admin'))
    );
    """)

    # Event Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('individual','individual_kids','corporate')),
        UNIQUE(name, type)
    );
    """)

    # Venues Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        venue_type TEXT NOT NULL CHECK(venue_type IN ('indoor','outdoor','hall')),
        city TEXT NOT NULL,
        price_per_hour REAL NOT NULL,
        UNIQUE(name, city)
    );
    """)

    # Catering Menus Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS catering_menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        package_type TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        price_per_person REAL NOT NULL,
        description TEXT,
        UNIQUE(package_type, meal_type)
    );
    """)

    # Coffee Corner Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coffee_corners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        price REAL
    )
    """)

    # Cake Sizes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cake_sizes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        size TEXT NOT NULL UNIQUE,
        base_price REAL NOT NULL
    );
    """)

    # Cake Tiers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cake_tiers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tiers INTEGER NOT NULL UNIQUE,
        extra_price REAL NOT NULL
    );
    """)

    # Cake Flavors
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cake_flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor TEXT NOT NULL UNIQUE
    );
    """)

    # Cake Fillings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cake_fillings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filling TEXT NOT NULL UNIQUE
    );
    """)
    
    # Services Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN ('AV','Staff','Entertainment','Decor','Giveaways')),
        price REAL NOT NULL,
        UNIQUE(name, category)
    );
    """)

    # Bookings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        event_name TEXT NOT NULL,
        event_type TEXT NOT NULL CHECK(event_type IN ('individual','corporate')),
        company_name TEXT,
        event_category_id INTEGER NOT NULL,
        venue_id INTEGER NOT NULL,
        event_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        num_guests INTEGER NOT NULL,
        theme TEXT,
        cake TEXT,
        total_price REAL,
        preparation_time_hours REAL,
        status TEXT NOT NULL DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(event_category_id) REFERENCES event_categories(id),
        FOREIGN KEY(venue_id) REFERENCES venues(id)
    );
    """)

    # Booking Services Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS booking_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        service_type TEXT NOT NULL,
        service_id INTEGER,
        price REAL,
        description TEXT,
        FOREIGN KEY(booking_id) REFERENCES bookings(id)
    );
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()