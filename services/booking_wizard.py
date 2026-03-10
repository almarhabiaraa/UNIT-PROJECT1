from datetime import datetime, timedelta
from database.db_connection import get_connection
from tabulate import tabulate

# -----------------------------
# PRICE ENGINE
# -----------------------------

def calculate_price_breakdown(booking):
    venue_cost = booking["venue_price_per_hour"] * booking["duration_hours"]
    catering_cost = booking["catering_price_per_person"] * booking["num_guests"]
    services_cost = booking.get("services_total", 0)
    giveaways_cost = booking["giveaway_price_per_person"] * booking["num_guests"]
    coffee_cost = booking.get("coffee_corner_price", 0)
    cake_cost = booking.get("cake_price", 0)

    total = venue_cost + catering_cost + services_cost + giveaways_cost + coffee_cost + cake_cost

    return {
        "venue": venue_cost,
        "catering": catering_cost,
        "services": services_cost,
        "giveaways": giveaways_cost,
        "coffee_corner": coffee_cost,
        "cake": cake_cost,
        "total": total
    }
    
    
# -----------------------------
# PRICE ENGINE: Show Price
# -----------------------------
def show_price(booking):
    breakdown = calculate_price_breakdown(booking)

    print("\n------ Current Price Breakdown ------")
    print(f"Guests: {booking['num_guests']}")
    print(f"Duration: {booking['duration_hours']:.2f} hours")
    print(f"Venue: {breakdown['venue']:.2f} SAR")
    print(f"Catering: {breakdown['catering']:.2f} SAR")
    print(f"Services: {breakdown['services']:.2f} SAR")
    print(f"Giveaways: {breakdown['giveaways']:.2f} SAR")
    print(f"Coffee Corner: {breakdown['coffee_corner']:.2f} SAR")
    print(f"Cake: {breakdown['cake']:.2f} SAR")
    print("-------------------------------------")
    print(f"Estimated Total: {breakdown['total']:.2f} SAR")
    print("-------------------------------------")


# -----------------------------
# BOOKING WIZARD
# -----------------------------

def booking_wizard(user):
    conn = get_connection()
    cursor = conn.cursor()

    booking = {
        "event_name": "",
        "event_date": "",
        "event_day": "",
        "start_time": "",
        "end_time": "",
        "duration_hours": 0,
        "city": "",
        "num_guests": 0,
        "event_type": "",
        "company_name": None,
        "category_id": None,
        "category_name": None,
        "category_type": None,
        "venue_id": None,
        "venue_price_per_hour": 0,
        "theme": "",
        "catering_price_per_person": 0,
        "services_price_per_hour": 0,
        "services_total": 0,
        "giveaway_price_per_person": 0,
        "coffee_corner_price": 0,
        "cake_price": 0
    } 

    step = 1

    while True:

        # ---------------- STEP 1 ----------------
        if step == 1:
            print("\n=== STEP 1: Event Information ===")
            booking["event_name"] = input("Event Name: ")

            while True:
                try:
                    event_date = input("Event Date (YYYY-MM-DD): ")
                    event_date_obj = datetime.strptime(event_date, "%Y-%m-%d")
                    if event_date_obj >= datetime.today() + timedelta(days=3):
                        booking["event_date"] = event_date
                        break
                    else:
                        print("Event must be booked at least 3 days in advance.")
                except:
                    print("Invalid date format.")

            while True:
                booking["start_time"] = input("Start Time (HH:MM): ")
                booking["end_time"] = input("End Time (HH:MM): ")
                try:
                    start = datetime.strptime(booking["start_time"], "%H:%M")
                    end = datetime.strptime(booking["end_time"], "%H:%M")
                    duration = (end - start).total_seconds() / 3600
                    if duration <= 0:
                        print("End time must be after start time.")
                        continue
                    booking["duration_hours"] = duration
                    break
                except:
                    print("Invalid time format.")

            while True:
                print("\nSelect City")
                cities = ["Jeddah", "Mecca", "Riyadh", "Dammam"]
                for i, city in enumerate(cities, 1):
                    print(f"{i}. {city}")
                try:
                    choice = int(input("Choose city: "))
                    booking["city"] = cities[choice - 1]
                    break
                except:
                    print("Invalid choice")

            booking["num_guests"] = int(input("Number of Guests: "))
            step += 1

        # ---------------- STEP 2 ----------------
        elif step == 2:
            print("\n=== STEP 2: Event Type ===\n")

            print("1. Private Event")
            print("   Personal, family, or social events.\n")

            print("2. Corporate Event")
            print("   Company, university, or professional events.\n")

            choice = input("Select (or b to go back): ")

            if choice.lower() == "b":
                step -= 1
                continue

            if choice == "1":
                booking["event_type"] = "individual"
                step += 1
            elif choice == "2":
                booking["event_type"] = "corporate"
                step += 1
            else:
                print("Invalid option. Please select 1 or 2.")
                
        # ---------------- STEP 3 ----------------
        elif step == 3:
            print("\n=== STEP 3: Event Category ===")
            if booking["event_type"] == "individual":
                cursor.execute("""
                    SELECT id, name, type FROM event_categories
                    WHERE type IN ('individual', 'individual_kids')
                """)
            else:
                cursor.execute("SELECT id, name, type FROM event_categories WHERE type='corporate'")

            categories = cursor.fetchall()
            if not categories:
                print("No categories found for this event type.")
                step -= 1
                continue

            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat[1]}")

            choice = input("Choose category (or b to go back): ")
            if choice == "b":
                step -= 1
                continue

            try:
                selected = categories[int(choice)-1]
                booking["category_id"] = selected[0]
                booking["category_name"] = selected[1]
                booking["category_type"] = selected[2]
            except:
                print("Invalid selection")
                continue
            
            # Helper function to convert 24-hour time to 12-hour format
            def format_time_12h(time_str_24h):
                """Convert 'HH:MM' 24-hour string to 12-hour format with AM/PM"""
                time_obj = datetime.strptime(time_str_24h, "%H:%M")
                return time_obj.strftime("%I:%M %p")

            # Helper function to get day name from date
            def get_day_name(date_str):
                """Return the day name (e.g., Monday) for a given date string 'YYYY-MM-DD'"""
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%A")
            event_date_obj = datetime.strptime(booking['event_date'], "%Y-%m-%d")
            event_day_name = event_date_obj.strftime("%A")
            booking["event_day"] = event_day_name

            # --------- Basic Summary ---------
            print("\n" + "="*35)
            print("      BOOKING SUMMARY (Basic Info)      ")
            print("="*35)
            print(f"Event Name : {booking['event_name']}")
            print(f"Event Date : {booking['event_date']} ({event_day_name})")
            print(f"Start Time : {format_time_12h(booking['start_time'])}  |  End Time : {format_time_12h(booking['end_time'])}")
            print(f"Duration   : {booking['duration_hours']:.2f} hours")
            print(f"City       : {booking['city']}")
            print(f"Guests     : {booking['num_guests']}")
            print(f"Event Type : {booking['event_type'].capitalize()}  |  Category : {booking['category_name']}")
            print("="*35)

            nav = input("\nDo you want to continue filling booking details or cancel? (n for next / c for cancel): ")
            if nav.lower() == "n":
                step += 1
            else:
                conn.close()
                return
        
        # ---------------- STEP 4 ----------------
        elif step == 4:
            print("\n=== STEP 4: Venue Selection ===")

            cursor.execute(
                "SELECT id, name, venue_type, price_per_hour FROM venues WHERE city=?",
                (booking["city"],)
            )
            venues = cursor.fetchall()

            if not venues:
                print("No venues available in this city.")
                step -= 1
                continue

            table_data = []
            for i, v in enumerate(venues, 1):
                table_data.append([
                    i,
                    v["name"],
                    v["venue_type"],
                    f"{v['price_per_hour']} SAR/hour"
                ])

            print()
            print(tabulate(
                table_data,
                headers=["#", "Venue Name", "Type", "Price"],
                tablefmt="grid"
            ))

            choice = input("\nChoose venue (or b to go back): ")

            if choice == "b":
                step -= 1
                continue

            try:
                venue = venues[int(choice) - 1]
                booking["venue_id"] = venue["id"]
                booking["venue_price_per_hour"] = venue["price_per_hour"]
            except (ValueError, IndexError):
                print("Invalid choice")
                continue

            show_price(booking)
            step += 1
            
        # ---------------- STEP 5 ----------------
        elif step == 5:
            print("\n=== STEP 5: Event Theme ===")
            category_type = booking.get("category_type")

            if category_type == "individual_kids":
                themes = {"1": "Cartoon", "2": "Pastel", "3": "Theme Party", "4": "None"}
            elif category_type == "individual":
                themes = {"1": "Luxury","2":"Elegant","3":"Minimal","4":"Pastel",
                        "5":"Romantic","6":"Vintage","7":"Traditional","8":"None"}
            else:
                themes = {"1": "Luxury","2":"Elegant","3":"Modern","4":"Industrial","5":"Minimal","6":"None"}

            while True:
                for key,val in themes.items():
                    print(f"{key}. {val}")

                choice = input("Choose theme (or b to go back): ")
                if choice == "b":
                    step -= 1
                    break 

                if choice in themes:
                    booking["theme"] = themes[choice]
                    step += 1
                    break  
                else:
                    print("Invalid choice, please select a valid theme number.")

        # ---------------- STEP 6 ----------------

        elif step == 6:
            print("\n=== STEP 6: Catering ===")

            add = input("Do you want catering? (y/n or b to go back): ")

            if add == "b":
                step -= 1
                continue
            elif add.lower() != "y":
                booking["catering_price_per_person"] = 0
                step += 1
                continue
            
            # ------------------ Meal type selection ------------------
            meals = {
                "1": ["breakfast"],
                "2": ["lunch"],
                "3": ["dinner"],
                "4": ["breakfast","lunch"],
                "5": ["breakfast","dinner"],
                "6": ["lunch","dinner"],
                "7": ["breakfast","lunch","dinner"]
            }

            print("""
            1. Breakfast                
            2. Lunch                    
            3. Dinner                  
            4. Breakfast + Lunch
            5. Breakfast + Dinner
            6. Lunch + Dinner
            7. Full Day (Breakfast + Lunch + Dinner)
            """)

            meal_choice = input("Select meal type (or b to go back): ")

            if meal_choice == "b":
                step -= 1
                continue

            selected_meals = meals.get(meal_choice, ["breakfast"])
            total_catering_price = 0

            # ------------------ Loop through selected meals ------------------
            for meal in selected_meals:
                print(f"\n=== {meal.capitalize()} Packages ===")

                cursor.execute("""
                    SELECT package_type, description, price_per_person
                    FROM catering_menus
                    WHERE meal_type=?
                """, (meal,))

                packages = cursor.fetchall()

                if not packages:
                    print("No packages available.")
                    continue

                # Prepare table data
                table_data = []
                for i, p in enumerate(packages, 1):
                    table_data.append([
                        i,
                        p["package_type"],
                        p["description"],
                        f"{p['price_per_person']} SAR"
                    ])

                # Display table
                print()
                print(tabulate(
                    table_data,
                    headers=["#", "Package", "Menu Description", "Price / Person"],
                    tablefmt="grid"
                ))

                # User selects package
                while True:
                    choice = input("\nChoose package (or b to go back): ")
                    if choice == "b":
                        step -= 1
                        break
                    try:
                        selected = packages[int(choice)-1]
                        total_catering_price += selected["price_per_person"]
                        print(
                            f"Selected: {meal.capitalize()} - {selected['package_type']} "
                            f"({selected['price_per_person']} SAR)"
                        )
                        break
                    except (ValueError, IndexError):
                        print("Invalid selection. Please choose a valid number from the table.")

            booking["catering_price_per_person"] = total_catering_price
            show_price(booking)
            step += 1
        # ---------------- STEP 7 ----------------
        elif step == 7:
            print("\n=== Coffee Break Corner ===")
            add = input("Do you want a coffee corner? (y/n or b to go back): ")
            
            if add.lower() == "b":
                step -= 1
                continue
            elif add.lower() != "y":
                booking["coffee_corner_price"] = 0
                step += 1
                continue

            # Fetch coffee corner options from database
            cursor.execute("SELECT id, name, description, price FROM coffee_corners")
            options = cursor.fetchall()

            if not options:
                print("No coffee corner options available.")
                booking["coffee_corner_price"] = 0
                step += 1
                continue

            # Prepare table data
            table_data = []
            for opt in options:
                table_data.append([opt['id'], opt['name'], opt['description'], f"{opt['price']} SAR"])

            # Display table without None option inside the table
            print("\nAvailable Coffee Corner Packages:")
            print(tabulate(table_data, headers=["ID", "Package Name", "Description", "Price"], tablefmt="grid"))

            # Loop for user selection
            while True:
                choice = input("\nChoose a package by ID (or 0 for None, b to go back): ")
                if choice.lower() == "b":
                    step -= 1
                    break
                try:
                    choice_int = int(choice)
                    if choice_int == 0:
                        booking["coffee_corner_price"] = 0
                        break
                    else:
                        cursor.execute("SELECT price FROM coffee_corners WHERE id=?", (choice_int,))
                        res = cursor.fetchone()
                        if res:
                            booking["coffee_corner_price"] = res[0]
                            break
                        else:
                            print("Invalid option. Please choose a valid ID from the table.")
                except ValueError:
                    print("Please enter a valid number.")

            show_price(booking)
            step += 1
        # ---------------- STEP 8 ----------------
        elif step == 8:
            print("\n=== STEP 8: Cake Selection ===")
            add = input("Do you want a cake? (y/n or b to go back): ")

            if add.lower() == "b":
                step -= 1
                continue
            elif add.lower() != "y":
                booking["cake_price"] = 0
                step += 1
                continue

            # Fetch data from database
            cursor.execute("SELECT size, base_price FROM cake_sizes")
            sizes = cursor.fetchall()

            cursor.execute("SELECT tiers, extra_price FROM cake_tiers")
            tiers = cursor.fetchall()

            cursor.execute("SELECT flavor FROM cake_flavors")
            flavors = cursor.fetchall()

            cursor.execute("SELECT filling FROM cake_fillings")
            fillings = cursor.fetchall()

            # ---------- Step 8.1: Display Sizes ----------
            size_table = []
            for i, s in enumerate(sizes, 1):
                size_table.append([i, s['size'], f"{s['base_price']} SAR"])
            print("\nAvailable Cake Sizes:")
            print(tabulate(size_table, headers=["#", "Size", "Base Price"], tablefmt="grid"))

            while True:
                size_choice = input("Choose cake size by number: ")
                if size_choice.isdigit() and 1 <= int(size_choice) <= len(sizes):
                    size_index = int(size_choice) - 1
                    size_selected = sizes[size_index]['size']
                    base_price = sizes[size_index]['base_price']
                    break
                else:
                    print("Invalid selection. Please choose a valid number from the table.")

            # ---------- Step 8.2: Display Tiers ----------
            tier_table = []
            for i, t in enumerate(tiers, 1):
                tier_table.append([i, t['tiers'], f"+{t['extra_price']} SAR"])
            print("\nAvailable Cake Tiers:")
            print(tabulate(tier_table, headers=["#", "Number of Tiers", "Extra Price"], tablefmt="grid"))

            while True:
                tier_choice = input("Choose number of tiers by number: ")
                if tier_choice.isdigit() and 1 <= int(tier_choice) <= len(tiers):
                    tier_index = int(tier_choice) - 1
                    tier_selected = tiers[tier_index]['tiers']
                    extra_price = tiers[tier_index]['extra_price']
                    break
                else:
                    print("Invalid selection. Please choose a valid number from the table.")

            # ---------- Step 8.3: Display Flavors ----------
            flavor_table = []
            for i, f in enumerate(flavors, 1):
                flavor_table.append([i, f['flavor']])
            print("\nAvailable Cake Flavors:")
            print(tabulate(flavor_table, headers=["#", "Flavor"], tablefmt="grid"))

            while True:
                flavor_choice = input("Choose cake flavor by number: ")
                if flavor_choice.isdigit() and 1 <= int(flavor_choice) <= len(flavors):
                    flavor_selected = flavors[int(flavor_choice)-1]['flavor']
                    break
                else:
                    print("Invalid selection. Please choose a valid number from the table.")

            # ---------- Step 8.4: Display Fillings ----------
            filling_table = []
            for i, f in enumerate(fillings, 1):
                filling_table.append([i, f['filling']])
            print("\nAvailable Cake Fillings:")
            print(tabulate(filling_table, headers=["#", "Filling"], tablefmt="grid"))

            while True:
                filling_choice = input("Choose cake filling by number: ")
                if filling_choice.isdigit() and 1 <= int(filling_choice) <= len(fillings):
                    filling_selected = fillings[int(filling_choice)-1]['filling']
                    break
                else:
                    print("Invalid selection. Please choose a valid number from the table.")

            # ---------- Calculate price ----------
            booking["cake_size"] = size_selected
            booking["cake_tiers"] = tier_selected
            booking["cake_flavor"] = flavor_selected
            booking["cake_filling"] = filling_selected
            booking["cake_price"] = base_price + extra_price

            show_price(booking)
            step += 1
            
        # ---------------- STEP 9 ----------------
        elif step == 9:

            service_categories = ["AV", "Staff", "Entertainment", "Decor"]

            go_back = False

            for category in service_categories:

                add_category = input(f"\nDo you want {category} services? (y/n or b to go back): ").lower()

                if add_category == "b":
                    go_back = True
                    break

                if add_category != "y":
                    continue

                print(f"\n=== {category} Services ===")

                cursor.execute(
                    "SELECT id, name, price FROM services WHERE category=?",
                    (category,)
                )
                services = cursor.fetchall()

                if not services:
                    print(f"No {category} services available.")
                    continue

                table_data = []
                for i, s in enumerate(services, 1):
                    table_data.append([i, s["name"], f"{s['price']} SAR"])

                print(tabulate(
                    table_data,
                    headers=["#", "Service", "Price"],
                    tablefmt="grid"
                ))

                print("Select services (0 to finish this category)")

                while True:

                    choice = input("Service number (0 to finish, b to go back): ")

                    if choice.lower() == "b":
                        go_back = True
                        break

                    if choice == "0":
                        break

                    try:
                        choice_int = int(choice)

                        if 1 <= choice_int <= len(services):

                            selected_service = services[choice_int - 1]

                            booking["services_total"] += selected_service["price"]

                            print(
                                f"Added: {selected_service['name']} ({selected_service['price']} SAR)"
                            )

                        else:
                            print("Invalid number.")

                    except ValueError:
                        print("Enter a valid number.")

                if go_back:
                    break

            if go_back:
                step -= 1
                continue

            show_price(booking)
            step += 1
        # ---------------- STEP 10 ----------------
        elif step == 10:

            print("\n=== Giveaways ===")
            add = input("Do you want giveaways? (y/n or b to go back): ")

            if add.lower() == "b":
                step -= 1
                continue
            elif add.lower() != "y":
                booking["giveaway_price_per_person"] = 0
                step += 1
                continue

            # Fetch giveaway options from database
            cursor.execute(
                "SELECT id, name, price FROM services WHERE category='Giveaways'"
            )
            gifts = cursor.fetchall()

            if not gifts:
                print("No giveaways available.")
                booking["giveaway_price_per_person"] = 0
                step += 1
                continue

            # Prepare
            table_data = []
            for i, g in enumerate(gifts, 1):
                table_data.append([i, g["name"], f"{g['price']} SAR per guest"])

            print(tabulate(table_data,
                        headers=["ID", "Giveaway", "Price"],
                        tablefmt="grid"))

            # User selection loop
            while True:
                choice = input("Choose giveaway (0 for None, b to go back): ")

                if choice.lower() == "b":
                    step -= 1
                    break

                if choice == "0":
                    booking["giveaway_price_per_person"] = 0
                    break

                try:
                    choice_int = int(choice)
                    if 1 <= choice_int <= len(gifts):
                        selected = gifts[choice_int - 1]
                        booking["giveaway_price_per_person"] = selected["price"]
                        print(f"Added: {selected['name']} ({selected['price']} SAR per guest)")
                        break
                    else:
                        print("Invalid number. Choose from the table.")
                except ValueError:
                    print("Enter a valid number.")

            show_price(booking)
            step += 1
        
        # ---------------- STEP 11 ----------------
        elif step == 11:
            breakdown = calculate_price_breakdown(booking)
            print("\n===== BOOKING SUMMARY =====")
            print("Event:", booking["event_name"])
            print("Date:", booking["event_date"])
            print(f"Start Time : {format_time_12h(booking['start_time'])}  |  End Time : {format_time_12h(booking['end_time'])}")
            print("Duration:", booking["duration_hours"], "hours")
            print("City:", booking["city"])
            print("Event Type:", booking["event_type"])
            print("Category:", booking["category_name"])
            print("Guests:", booking["num_guests"])
            print("Theme:", booking["theme"])
            print("\n--- Price Breakdown ---")
            print(f"Venue: {breakdown['venue']} SAR")
            print(f"Catering: {breakdown['catering']} SAR")
            print(f"Services: {breakdown['services']} SAR")
            print(f"Giveaways: {breakdown['giveaways']} SAR")
            print(f"Coffee Corner: {breakdown['coffee_corner']} SAR")
            print(f"Cake: {breakdown['cake']} SAR")
            print("-------------------------")
            print(f"TOTAL: {breakdown['total']} SAR")

            confirm = input("\nConfirm booking? (y / b): ")
            if confirm == "b":
                step -= 1
                continue
            if confirm == "y":
                cursor.execute("""
                    INSERT INTO bookings(
                        user_id,event_name,event_type,company_name,event_category_id,
                        venue_id,event_date,start_time,end_time,num_guests,
                        theme,total_price,preparation_time_hours,status
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    user["id"], booking["event_name"], booking["event_type"], booking["company_name"],
                    booking["category_id"], booking["venue_id"], booking["event_date"],
                    booking["start_time"], booking["end_time"], booking["num_guests"],
                    booking["theme"], breakdown["total"], booking["duration_hours"] + 4, "pending"
                ))
                conn.commit()
                conn.close()
                print("\nYour booking has been successfully submitted.")
                print("Please wait for approval from the Happy Moments Planner team.")
                print("Cancellation allowed within 24 hours.")
                return