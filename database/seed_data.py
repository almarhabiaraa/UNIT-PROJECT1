# database/seed_data.py

from database.db_connection import get_connection
from services.auth_service import hash_password

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert default admin account (only if not exists)
    cursor.execute("""
    INSERT OR IGNORE INTO users (full_name, username, email, phone_number, password, role)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "System Administrator",   # full_name
        "admin",                  # username
        "admin@example.com",      # email
        "0000000000",             # phone_number
        hash_password("admin123"),# hashed password
        "admin"                   # admin role
    ))

    # Event Categories
    cursor.executemany("""
    INSERT OR IGNORE INTO event_categories (name,type)
    VALUES (?,?)
    """, [

        # Kids
        ("Birthday","individual_kids"),
        ("Baby Shower","individual_kids"),
        ("Gender Reveal","individual_kids"),

        # Individual
        ("Wedding","individual"),
        ("Anniversary","individual"),
        ("Graduation","individual"),
        ("Ramadan Gathering","individual"),
        ("Eid Celebration","individual"),
        ("Others","individual"),

        # Corporate
        ("Conference","corporate"),
        ("Exhibition","corporate"),
        ("Product Launch","corporate"),
        ("Annual Celebration","corporate"),
        ("Booth","corporate"),
        ("Workshop","corporate"),
        ("Meeting","corporate"),
        ("Team Building","corporate"),
        ("Others","corporate")
    ])

    # Venues
    cursor.executemany("""
    INSERT OR IGNORE INTO venues (name, venue_type, city, price_per_hour)
    VALUES (?, ?, ?, ?)
    """, [
        ("Coral Lounge","indoor","Jeddah",500),
        ("Palm Garden","outdoor","Jeddah",450),
        ("Red Sea Hall","hall","Jeddah",700),

        ("Noor Lounge","indoor","Mecca",550),
        ("Zamzam Garden","outdoor","Mecca",500),
        ("Kaaba Hall","hall","Mecca",750),

        ("Riyadh Elite Lounge","indoor","Riyadh",600),
        ("Desert Garden","outdoor","Riyadh",550),
        ("Kingdom Hall","hall","Riyadh",800),

        ("Pearl Lounge","indoor","Dammam",480),
        ("Sea Breeze Garden","outdoor","Dammam",430),
        ("Gulf Hall","hall","Dammam",650)
    ])

    # Catering Menus
    cursor.executemany("""
    INSERT OR IGNORE INTO catering_menus
    (package_type, meal_type, price_per_person, description)
    VALUES (?, ?, ?, ?)
    """, [
        ("Silver","breakfast",55,"Scrambled Eggs, Shakshuka, Foul + Croissants + Muffins + Coffee & Juice"),
        ("Gold","breakfast",85,"Omelette Station + Sausages + Pancakes + Fresh Juices"),
        ("VIP","breakfast",130,"Live Egg Station + Halloumi + Artisan Bread + French Pastries"),

        ("Silver","lunch",95,"Chicken Kabsa OR Pasta + Salad + Dessert"),
        ("Gold","lunch",145,"Kabsa + Grilled Chicken + 2 Salads + Cheesecake"),
        ("VIP","lunch",210,"Mixed Grill + Lamb Ouzi + Dessert Table"),

        ("Silver","dinner",110,"Chicken Biryani + Soup + Chocolate Cake"),
        ("Gold","dinner",165,"Grilled Chicken + Beef Steak + Arabic Sweets"),
        ("VIP","dinner",240,"Premium Mixed Grill + Seafood + Luxury Desserts")
    ])

    # Coffee Corners
    cursor.executemany("""
    INSERT OR IGNORE INTO coffee_corners (name, description, price)
    VALUES (?, ?, ?)
    """, [
        ("Basic Coffee Corner","Arabic coffee, tea, dates",500),
        ("Premium Coffee Corner","Arabic coffee, specialty coffee, tea, cookies",900),
        ("Luxury Coffee Corner","Barista station, espresso drinks, pastries",1500)
    ])

    # Cake Sizes
    cursor.executemany("""
    INSERT OR IGNORE INTO cake_sizes (size, base_price)
    VALUES (?, ?)
    """, [
        ("S",100),
        ("M",180),
        ("L",250)
    ])

    # Cake Tiers
    cursor.executemany("""
    INSERT OR IGNORE INTO cake_tiers (tiers, extra_price)
    VALUES (?, ?)
    """, [
        (1,0),
        (2,60),
        (3,120)
    ])

    # Cake Flavors
    cursor.executemany("""
    INSERT OR IGNORE INTO cake_flavors (flavor)
    VALUES (?)
    """, [
        ("Chocolate",),
        ("Vanilla",),
        ("Red Velvet",),
        ("Lemon",),
        ("Carrot",)
    ])

    # Cake Fillings
    cursor.executemany("""
    INSERT OR IGNORE INTO cake_fillings (filling)
    VALUES (?)
    """, [
        ("Chocolate Cream",),
        ("Strawberry Cream",),
        ("Cream Cheese",),
        ("Custard",),
        ("Hazelnut Cream",),
        ("Caramel Cream",)
    ])

    # Services
    cursor.executemany("""
    INSERT OR IGNORE INTO services (name, category, price)
    VALUES (?, ?, ?)
    """, [
        # AV
        ("Sound System","AV",500),
        ("Wireless Microphones","AV",200),
        ("DJ Setup","AV",800),
        ("LED Screens","AV",700),
        ("Projector and Screen","AV",400),

        # Staff
        ("Waiters","Staff",150),
        ("Host / Hostess","Staff",200),
        ("Event Coordinator","Staff",500),
        ("Photographer","Staff",600),
        ("Videographer","Staff",700),
        ("Makeup Artist","Staff",300),
        ("Hair Stylist","Staff",300),

        # Entertainment
        ("Live Band","Entertainment",2500),
        ("Singer","Entertainment",1200),
        ("Oud Player","Entertainment",900),
        ("Violinist","Entertainment",1000),
        ("DJ","Entertainment",800),
        ("Magician","Entertainment",900),
        ("Clown","Entertainment",700),

        # Decor
        ("Photo Booth","Decor",900),
        ("Balloon Decoration","Decor",400),
        ("Flower Decoration","Decor",700),
        ("Entrance Arch","Decor",500),
        ("Table Centerpieces","Decor",350),

        # Giveaways
        ("Customized Gift Bags","Giveaways",15),
        ("Branded Mugs","Giveaways",20),
        ("Mini Perfumes","Giveaways",25),
        ("Chocolate Boxes","Giveaways",18)
    ])

    conn.commit()
    conn.close()
    print("Seed data inserted successfully!")

if __name__ == "__main__":
    seed_data()