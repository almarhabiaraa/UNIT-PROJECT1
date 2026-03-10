from services.auth_service import signup, validate_phone, validate_email, login

def signup_cli():
    print("\n--- Sign Up ---")

    # --------- FULL NAME ---------
    full_name = input("Full Name: ").strip()

    # --------- PHONE NUMBER ---------
    while True:
        phone_number = input("Phone Number: ").strip()
        if validate_phone(phone_number):
            break
        print("❌ Invalid phone number. Must start with 05 and be 10 digits.")

    # --------- USERNAME ---------
    username = input("Username: ").strip()

    # --------- EMAIL ---------
    while True:
        email = input("Email: ").strip()
        if validate_email(email):
            break
        print("❌ Invalid email format. Must contain '@' and a domain.")

    # --------- PASSWORD ---------
    password = input("Password: ").strip()

    # --------- SIGNUP ---------
    success = signup(full_name, phone_number, username, email, password)
    if success:
        print("You can now login with your credentials!")

def login_cli():
    print("\n--- Login ---")
    identifier = input("Username or Email: ").strip()
    password = input("Password: ").strip()
    user = login(identifier, password)
    if user:
        print(f"✅ Welcome, {user['full_name']}!")
        return user
    return None