import sqlite3
from contextlib import closing

DB_PATH = "/Users/hunterdarensbourg/PycharmProjects/DatabaseApplication/grocery.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ==========================
# MEMBER INTERFACE
# ==========================

def member_login():
    email = input("Email address: ").strip()
    password = input("Password: ").strip()

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM member
            WHERE email_address = ? AND password = ?
        """, (email, password))
        row = cur.fetchone()

    if row:
        print(f"\nWelcome, {row['name']}!")
        member_menu(row["ID"], row["name"])
    else:
        print("\nInvalid email or password.\n")

def show_member_summary(member_id):
    with closing(get_connection()) as conn:
        cur = conn.cursor()

        cur.execute("SELECT points, name FROM member WHERE ID = ?", (member_id,))
        member = cur.fetchone()
        if not member:
            print("Member not found.")
            return

        print(f"\nMember: {member['name']}")
        print(f"Points: {member['points']}")

        cur.execute("""
            SELECT p.date_purchased, pr.name AS product_name,
                   pr.price, pu.quantity,
                   (pr.price * pu.quantity) AS total
            FROM purchase pu
            JOIN product pr ON pr.ID = pu.product_ID
            JOIN purchase p ON p.member_ID = pu.member_ID AND p.product_ID = pu.product_ID
        """)

def show_member_purchases(member_id):
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT pu.date_purchased,
                   pr.name AS product_name,
                   pr.price,
                   pu.quantity,
                   (pr.price * pu.quantity) AS total
            FROM purchase pu
            JOIN product pr ON pr.ID = pu.product_ID
            WHERE pu.member_ID = ?
            ORDER BY pu.date_purchased
        """, (member_id,))
        rows = cur.fetchall()

    if not rows:
        print("\nNo purchases found.")
        return

    print("\nYour purchases:")
    for r in rows:
        print(f"- {r['date_purchased']}: {r['product_name']} x{r['quantity']} "
              f"@ {r['price']:.2f} = {r['total']:.2f}")

def update_member_email(member_id):
    new_email = input("Enter new email: ").strip()
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE member SET email_address = ? WHERE ID = ?", (new_email, member_id))
            conn.commit()
            print("Email updated.")
        except sqlite3.IntegrityError as e:
            print(f"Error updating email (maybe duplicate): {e}")

def update_member_password(member_id):
    new_password = input("Enter new password: ").strip()
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE member SET password = ? WHERE ID = ?", (new_password, member_id))
        conn.commit()
        print("Password updated.")

def delete_member_profile(member_id):
    confirm = input("Are you sure you want to delete your profile? This CANNOT be undone. (y/N): ").lower()
    if confirm != "y":
        print("Cancelled.")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM purchase WHERE member_ID = ?", (member_id,))
            cur.execute("DELETE FROM member WHERE ID = ?", (member_id,))
            conn.commit()
            print("Profile and purchases deleted.")
        except sqlite3.IntegrityError as e:
            print(f"Error deleting profile: {e}")

def member_menu(member_id, member_name):
    while True:
        print(f"""
==== Member Menu ({member_name}) ====
1. View points and purchases
2. Update email
3. Update password
4. Delete profile
5. Logout
""")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_member_summary(member_id)
            show_member_purchases(member_id)
        elif choice == "2":
            update_member_email(member_id)
        elif choice == "3":
            update_member_password(member_id)
        elif choice == "4":
            delete_member_profile(member_id)
            break
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def show_member_summary(member_id):
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, points FROM member WHERE ID = ?", (member_id,))
        row = cur.fetchone()
    if not row:
        print("Member not found.")
    else:
        print(f"\nName: {row['name']}")
        print(f"Points: {row['points']}")

# ==========================
# MANAGER INTERFACE
# ==========================

def manager_login():
    try:
        manager_id = int(input("Manager ID: ").strip())
    except ValueError:
        print("Manager ID must be an integer.\n")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, name
            FROM manager
            WHERE ID = ?
        """, (manager_id,))
        row = cur.fetchone()

    if row is None:
        print("\nNo manager found with that ID.\n")
        return

    manager_name = row["name"]
    print(f"\nWelcome, Manager {manager_name} (ID {manager_id})!\n")
    manager_menu(manager_id, manager_name)


def add_associate():
    try:
        assoc_id = int(input("Associate ID (integer): "))
        name = input("Name: ").strip()
        salary = int(input("Salary (integer): "))
        dept_name = input("Department name (must exist): ").strip()
    except ValueError:
        print("Invalid numeric input.")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO associate (ID, name, salary, dept_name)
                VALUES (?, ?, ?, ?)
            """, (assoc_id, name, salary, dept_name))
            cur.execute("""
                INSERT INTO works (associate_ID, dept_name)
                VALUES (?, ?)
            """, (assoc_id, dept_name))
            conn.commit()
            print("Associate added.")
        except sqlite3.IntegrityError as e:
            print(f"Error adding associate: {e}")

def update_associate():
    try:
        assoc_id = int(input("Associate ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    name = input("New name (leave blank to keep current): ").strip()
    salary_input = input("New salary (leave blank to keep current): ").strip()
    dept_name = input("New department (leave blank to keep current): ").strip()

    with closing(get_connection()) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM associate WHERE ID = ?", (assoc_id,))
        row = cur.fetchone()
        if not row:
            print("Associate not found.")
            return

        new_name = name if name else row["name"]
        new_salary = row["salary"]
        if salary_input:
            try:
                new_salary = int(salary_input)
            except ValueError:
                print("Invalid salary, keeping old value.")
        new_dept = dept_name if dept_name else row["dept_name"]

        try:
            cur.execute("""
                UPDATE associate
                SET name = ?, salary = ?, dept_name = ?
                WHERE ID = ?
            """, (new_name, new_salary, new_dept, assoc_id))
            cur.execute("UPDATE works SET dept_name = ? WHERE associate_ID = ?", (new_dept, assoc_id))
            conn.commit()
            print("Associate updated.")
        except sqlite3.IntegrityError as e:
            print(f"Error updating associate: {e}")

def delete_associate():
    try:
        assoc_id = int(input("Associate ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    confirm = input("Are you sure you want to delete this associate? (y/N): ").lower()
    if confirm != "y":
        print("Cancelled.")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM works WHERE associate_ID = ?", (assoc_id,))
            cur.execute("DELETE FROM associate WHERE ID = ?", (assoc_id,))
            conn.commit()
            print("Associate deleted.")
        except sqlite3.IntegrityError as e:
            print(f"Error deleting associate: {e}")

def list_associates():
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT ID, name, salary, dept_name FROM associate ORDER BY ID")
        rows = cur.fetchall()
    print("\nAssociates:")
    for r in rows:
        print(f"- {r['ID']}: {r['name']} ({r['dept_name']}) salary={r['salary']}")

def manager_menu(manager_id, manager_name):
    while True:
        print(f"""
==== Manager Menu ({manager_name}, ID {manager_id}) ====
1. List associates
2. Add associate
3. Update associate
4. Delete associate
5. Back to main menu
""")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_associates()
        elif choice == "2":
            add_associate()
        elif choice == "3":
            update_associate()
        elif choice == "4":
            delete_associate()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


# ==========================
# INVENTORY INTERFACE
# ==========================

def list_products(limit=20):
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, name, price, quantity_in_stock, dept_name
            FROM product
            ORDER BY ID
            LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
    print(f"\nFirst {limit} products:")
    for r in rows:
        print(f"- {r['ID']}: {r['name']} ({r['dept_name']}) "
              f"price={r['price']}, qty={r['quantity_in_stock']}")

def add_product():
    try:
        prod_id = int(input("Product ID (integer): "))
        name = input("Name: ").strip()
        brand = input("Brand: ").strip()
        price = float(input("Price: "))
        qty = int(input("Quantity in stock: "))
        date_added = input("Date added (YYYY-MM-DD): ").strip()
        aisle_id = input("Aisle ID (e.g. A1, B3): ").strip()
        dept_name = input("Department name (must match aisle/department): ").strip()
    except ValueError:
        print("Invalid numeric input.")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO product
                    (ID, name, brand, price, quantity_in_stock, date_added, aisle_id, dept_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (prod_id, name, brand, price, qty, date_added, aisle_id, dept_name))
            conn.commit()
            print("Product added.")
        except sqlite3.IntegrityError as e:
            print(f"Error adding product: {e}")

def update_product():
    try:
        prod_id = int(input("Product ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product WHERE ID = ?", (prod_id,))
        row = cur.fetchone()
        if not row:
            print("Product not found.")
            return

        print(f"Current: {row['name']} price={row['price']} qty={row['quantity_in_stock']}")
        price_input = input("New price (leave blank to keep current): ").strip()
        qty_input = input("New quantity (leave blank to keep current): ").strip()

        new_price = row["price"]
        if price_input:
            try:
                new_price = float(price_input)
            except ValueError:
                print("Invalid price, keeping old value.")

        new_qty = row["quantity_in_stock"]
        if qty_input:
            try:
                new_qty = int(qty_input)
            except ValueError:
                print("Invalid quantity, keeping old value.")

        cur.execute("""
            UPDATE product
            SET price = ?, quantity_in_stock = ?
            WHERE ID = ?
        """, (new_price, new_qty, prod_id))
        conn.commit()
        print("Product updated.")

def delete_product():
    try:
        prod_id = int(input("Product ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    confirm = input("This will delete related rows (purchase, supplies, product_aisle). Continue? (y/N): ").lower()
    if confirm != "y":
        print("Cancelled.")
        return

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM purchase WHERE product_ID = ?", (prod_id,))
            cur.execute("DELETE FROM supplies WHERE product_ID = ?", (prod_id,))
            cur.execute("DELETE FROM product_aisle WHERE product_ID = ?", (prod_id,))
            cur.execute("DELETE FROM product WHERE ID = ?", (prod_id,))
            conn.commit()
            print("Product and related records deleted.")
        except sqlite3.IntegrityError as e:
            print(f"Error deleting product: {e}")

def inventory_menu():
    while True:
        print("""
==== Inventory Menu ====
1. List products (first 20)
2. Add product
3. Update product (price/quantity)
4. Delete product
5. Back to main menu
""")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# ==========================
# MAIN MENU
# ==========================

def main():
    while True:
        print("""
==== Grocery Store Application ====
1. Member login
2. Manager login
3. Inventory management (no login / or manager login)
4. Exit
""")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            member_login()
        elif choice == "2":
            manager_login()
        elif choice == "3":
            inventory_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
