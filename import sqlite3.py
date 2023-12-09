import hashlib
from datb import Database
from userrr import User
from empl import Employee
from tov import Tovar

def add_initial_tovars(db):
    tovars = [
        Tovar("Iphone 11", 42999),
        Tovar("Iphone 13", 84999),
        Tovar("Iphone 14", 114999),
        Tovar("Samsung Galaxy", 48999),
        Tovar("Samsung Galaxy Ultra", 114499),
        Tovar("HONOR X5 Plus", 10999),
        Tovar("HONOR X9a", 27999),
        Tovar("HONOR 70", 31999),
        Tovar("Xiaomi Redmi A2+", 5999),
        Tovar("Xiaomi 13T Pro", 7499),
        Tovar("Xiaomi Redmi Note 11Pro+", 29999)
    ]
    for tovar in tovars:
        db.add_tovar(tovar.name, tovar.price)

def register_user(db):
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    role = input("Выберите роль:\n 1 - Клиент\n 2 - Сотрудник\n 3 - Админ\n ")
    full_name = input("Введите ваше полное имя: ")

    if role == "1":
        role = "Клиент"
    elif role == "2":
        role = "Сотрудник"
    elif role == "3":
        role = "Админ"
    else:
        print("Неверная роль.")
        return
    db.add_user(username, password, role, full_name)
    print("Регистрация успешна!")

def login_user(db):
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    user_data = db.get_user_by_username(username)

    if user_data and hashlib.sha256(password.encode()).hexdigest() == user_data[2]:
        if user_data[3] == "Клиент":
            return User(user_data[1], user_data[2], user_data[3], user_data[4])
        elif user_data[3] == "Сотрудник":
            return Employee(user_data[1], user_data[2], user_data[3], user_data[4])
    else:
        print("Неверный логин или пароль.")
    return None
    
def client_menu(user, db):
        while True:
            print("1. Просмотр товаров")
            print("2. Добавить заказ")
            print("3. Просмотр заказов")
            print("4. Изменить данные")
            print("5. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                show_tovars(db)
            elif choice == "2":
                add_order(user, db)
            elif choice == "3":
                show_orders(user, db)
            elif choice == "4":
                update_user_data(user, db)
            elif choice == "5":
                break
            else:
                print("Неверный ввод. Попробуйте снова.")
            
def employee_menu(user, db):
        while True:
            print("1. Просмотр товаров")
            print("2. Добавить товар")
            print("3. Удалить товар")
            print("4. Изменить данные")
            print("5. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                show_tovars(db)
            elif choice == "2":
                add_tovar(db)
            elif choice == "3":
                delete_tovar(db)
            elif choice == "4":
                update_user_data(user, db)
            elif choice == "5":
                break
            else:
                print("Неверный ввод. Попробуйте снова.")

def admin_menu(user, db):
        while True:
            print("1. Просмотр всех сотрудников")
            print("2. Добавить сотрудника")
            print("3. Изменить данные")
            print("4. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                show_employees(db)
            elif choice == "2":
                add_employee(db)
            elif choice == "3":
                update_user_data(user, db)
            elif choice == "4":
                break
            else:
                print("Неверный ввод. Попробуйте снова.")
            
def show_tovars(db):
        tovars = db.cursor.execute('SELECT * FROM tovars').fetchall()
        print("Список товаров:")
        for tovar in tovars:
            print(f"{tovar[0]}. {tovar[1]} - {tovar[2]} руб.")
    
def add_tovar(db):
    name = input("Введите название товара: ")
    price = int(input("Введите цену товара: "))
    if not isinstance(price, (int)) or price < 2000:
            print("Ошибка: Цена должна быть быть больше.")
            return

    db.add_tovar(name, price)
    print("Товар добавлен успешно!")
    

def delete_tovar(db):
        show_tovars(db)
        tovar_id = int(input("Введите ID товара для удаления: "))

        db.cursor.execute('DELETE FROM tovars WHERE id = ?', (tovar_id,))
        db.conn.commit()
        print("Товар удален успешно!")

def show_orders(user, db):
    orders = db.cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user[2],)).fetchall()
    print("Ваши заказы:")
    for order in orders:
        tovar = db.cursor.execute('SELECT * FROM tovars WHERE id = ?', (order[2],)).fetchone()
        print(f"{order[0]}. {tovar[1]} - {tovar[2]} руб.")
        
def add_order(user, db):
        show_tovars(db)
        tovar_id = int(input("Введите ID товара для заказа: "))

        db.add_order(user[2], tovar_id)
        print("Заказ оформлен успешно!")

def show_employees(db):
        employees = db.cursor.execute('SELECT * FROM users WHERE role = "Сотрудник"').fetchall()
        print("Список сотрудников:")
        for employee in employees:
            print(f"{employee[0]}. {employee[4]} ({employee[1]}) - {employee[2]}")
    
def add_employee(db):
        username = input("Введите логин сотрудника: ")
        password = input("Введите пароль сотрудника: ")
        full_name = input("Введите имя сотрудника: ")

        db.add_employee(username, password, full_name)
        print("Сотрудник добавлен успешно!")

def update_user_data(user, db):
        new_username = input("Введите новый логин: ")
        new_password = input("Введите новый пароль: ")

        table_name = "users"

        query = f'''
            UPDATE {table_name} SET password = ?, full_name = ? WHERE id = ?
        '''
        db.cursor.execute(query, (hashlib.sha256(new_password.encode()).hexdigest(), new_username, user[0]))
        db.conn.commit()
        print("Данные обновлены успешно!")


def main():
    db = Database()

    while True:
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            register_user(db)
        elif choice == "2":
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            user = db.get_user_by_username(username)

            if user and user[2] == hashlib.sha256(password.encode()).hexdigest():
                print(f"Добро пожаловать, {user[4]}!")

                if user[3] == "Клиент":
                    client_menu(user,db)
                elif user[3] == "Сотрудник":
                    employee_menu(user,db)
                elif user[3] == "Админ":
                    admin_menu(user,db)
                else:
                    print("Неверная роль.")
            else:
                print("Неверный логин или пароль.")
        elif choice == "3":
            break
        else:
            print("Неверный выбор.")     

if __name__ == "__main__":
    db = Database()
    db.drop_tovars_table() 
    db.create_tables()
    add_initial_tovars(db)
    main()