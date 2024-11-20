from classes import Messenger
from XML_JSON import JSONFileHandler, XMLFileHandler

#основное меню
def main_menu():
    print("Главное меню:")
    print("1. Работа с пользователями")
    print("2. Работа с чатами")
    print("3. Действия с файлами")
    print("0. Выйти")

#меню работы с пользователями
def user_menu():
    print("\nРабота с пользователями:")
    print("1. Добавить пользователя")
    print("2. Вывести список пользователей")
    print("3. Изменить статус пользователя")
    print("4. Добавить контакт")
    print("5. Удалить контакт")
    print("6. Показать контакты пользователя")
    print("0. Назад")

#меню работы с чатами
def chat_menu():
    print("\nРабота с чатами:")
    print("1. Создать приватный чат")
    print("2. Вывести список чатов")
    print("3. Отправить сообщение")
    print("4. Вывести сообщения чата")
    print("5. Групповые чаты")
    print("0. Назад")

def group_chat_menu():
    print("\nРабота с групповыми чатами:")
    print("1. Создать групповой чат")
    print("2. Посмотреть информацию о групповом чате")
    print("3. Добавить участника в групповой чат")
    print("4. Удалить участника из группового чата")
    print("0. Назад")

#меню работы с файлами
def file_menu():
    print("\nДействия с файлами:")
    print("1. Записать пользователей в JSON")
    print("2. Записать пользователей в XML")
    print("3. Считать пользователей из JSON")
    print("4. Считать пользователей из XML")
    print("5. Записать контакты в JSON")
    print("6. Считать контакты из JSON")
    print("7. Записать чаты в JSON")
    print("8. Считать чаты из JSON")
    print("0. Назад")

#создаем мессенджер
messenger = Messenger()
while True:
    main_menu()
    main_choice = input("Выберите категорию: ")

    if main_choice == "1":  # Работа с пользователями
        while True:
            user_menu()
            user_choice = input("Выберите действие: ")
            if user_choice == "1":
                username = input("Введите имя пользователя: ")
                try:
                    messenger.add_user(username)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif user_choice == "2":
                messenger.print_users()
            elif user_choice == "3":
                username = input("Введите имя пользователя: ")
                new_status = input("Введите новый статус (online, offline, busy, away): ")
                try:
                    messenger.change_user_status(username, new_status)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif user_choice == "4":
                owner_name = input("Введите имя пользователя, который добавляет контакт: ")
                contact_name = input("Введите имя добавляемого контакта: ")
                try:
                    messenger.add_contact(owner_name, contact_name)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif user_choice == "5":
                owner_name = input("Введите имя пользователя, который удаляет контакт: ")
                contact_name = input("Введите имя удаляемого контакта: ")
                try:
                    messenger.remove_contact(owner_name, contact_name)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif user_choice == "6":
                owner_name = input("Введите имя пользователя: ")
                try:
                    messenger.show_contacts(owner_name)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif user_choice == "0":
                print("\n")
                break

    elif main_choice == "2":  # Работа с чатами
        while True:
            chat_menu()
            chat_choice = input("Выберите действие: ")
            # Здесь аналогично обрабатываем все команды из меню чатов
            if chat_choice == "1":
                if len(messenger.users) < 2:
                    print("Ошибка: для создания чата должно быть добавлено минимум два пользователя.")
                else:
                    username1 = input("Введите имя первого участника: ")
                    username2 = input("Введите имя второго участника: ")
                    try:
                        messenger.add_private_chat(username1, username2)
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                print("\n")

            elif chat_choice == "2":
                if len(messenger.chats) == 0:
                    print("Не создано ни одного чата!\n")
                else:
                    messenger.print_chats()
                print("\n")

            elif chat_choice == "3":
                chat_id = int(input("Введите ID чата для отправки сообщения: "))
                sender = input("Введите имя отправителя: ")
                content = input("Введите текст сообщения: ")
                try:
                    messenger.send_message(chat_id, sender, content)
                except ValueError as e:
                    print(f"Ошибка: {e}")
                print("\n")

            elif chat_choice == "4":
                chat_id = int(input("Введите ID чата для просмотра сообщений: "))
                chat = next((c for c in messenger.chats if c.chat_id == chat_id), None)
                if chat:
                    chat.print_messages()
                else:
                    print(f"Чат с ID {chat_id} не найден.")
                print("\n")

            elif chat_choice == "5":
                while True:
                    group_chat_menu()
                    choice = input("Введите действие: ")

                    if choice == "1":
                        group_name = input("Введите название группы: ")
                        admin_name = input("Введите имя администратора: ")
                        try:
                            messenger.add_group_chat(group_name, admin_name)
                        except ValueError as e:
                            print(f"Ошибка: {e}")

                    elif choice == "2":
                        chat_id = int(input("Введите ID группы: "))
                        try:
                            messenger.get_group_info(chat_id)
                        except ValueError as e:
                            print(f"Ошибка: {e}")

                    elif choice == "3":
                        chat_id = int(input("Введите ID группы: "))
                        username = input("Введите имя пользователя: ")
                        try:
                            messenger.add_participant_to_group(chat_id, username)
                        except ValueError as e:
                            print(f"Ошибка: {e}")

                    elif choice == "4":
                        chat_id = int(input("Введите ID группы: "))
                        username = input("Введите имя пользователя: ")
                        try:
                            messenger.remove_participant_from_group(chat_id, username)
                        except ValueError as e:
                            print(f"Ошибка: {e}")

                    elif choice == "0":
                        print("\n")
                        break

            elif chat_choice == "0":
                print("\n")
                break

    elif main_choice == "3":  # Действия с файлами
        while True:
            file_menu()
            file_choice = input("Выберите действие: ")

            if file_choice == "1":
                data = messenger.prepare_users_data()
                JSONFileHandler.save_to_file(data)

            elif file_choice == "2":
                data = messenger.prepare_users_data()
                XMLFileHandler.save_to_file(data)

            elif file_choice == "3":
                filename = input("Введите имя JSON файла (по умолчанию: users.json): ")
                filename = filename.strip() or "users.json"
                messenger.load_users_from_json(filename)

            elif file_choice == "4":
                filename = input("Введите имя XML файла (по умолчанию: users.xml): ")
                filename = filename.strip() or "users.xml"
                messenger.load_users_from_xml(filename)

            elif file_choice == "5":
                filename = input("Введите имя файла для сохранения контактов (по умолчанию: contacts.json): ")
                filename = filename.strip() or "contacts.json"
                messenger.save_contacts_to_json(filename)

            elif file_choice == "6":
                filename = input("Введите имя файла для загрузки контактов (по умолчанию: contacts.json): ")
                filename = filename.strip() or "contacts.json"
                messenger.load_contacts_from_json(filename)

            elif file_choice == "7":
                filename = input("Введите имя файла для сохранения чатов (по умолчанию: chats.json): ")
                filename = filename.strip() or "chats.json"
                messenger.save_chats_to_json(filename)

            elif file_choice == "0":
                print("\n")
                break

    elif main_choice == "0":
        print("Завершение работы программы.")
        break


