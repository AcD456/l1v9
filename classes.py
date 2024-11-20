from datetime import datetime
from XML_JSON import JSONFileHandler, XMLFileHandler

class Messenger:
    def __init__(self):
        self.users = []
        self.chats = []

    # --- РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ---
    def add_user(self, username): #добавление нового User
        # Проверяем, существует ли пользователь с таким именем
        if any(user.username == username for user in self.users):
            raise ValueError(f"Пользователь с именем '{username}' уже существует.")
        #если нет User с таким именем, то добавляем его
        user_id = len(self.users) + 1
        new_user = User(user_id, username)
        self.users.append(new_user)
        print("Пользователь успешно добавлен!")


    def delete_user(self, username): #удаление User
        for user in self.users:
            if user.username == username:
                self.users.remove(user)
    def print_users(self):
        for user in self.users:
            print(f"Имя пользователя: {user.username}, user_id: {user.user_id}, статус: {user.status}")

    # --- РАБОТА С ЧАТОМ ---
    def add_private_chat(self, username1, username2):
        if not all(any(user.username == name for user in self.users) for name in [username1, username2]):
            raise ValueError("Один из пользователей не найден.")
        chat_id = len(self.chats) + 1
        private_chat = PrivateChat(chat_id, username1, username2)
        self.chats.append(private_chat)
        print(f"Приватный чат между {username1} и {username2} успешно создан!")
    def print_chats(self):
        for chat in self.chats:
            print(f"Chat_id: {chat.chat_id}, участники: {chat.participants[0]} и {chat.participants[1]}.")

    # --- РАБОТА С СООБЩЕНИЯМИ ---
    def send_message(self, chat_id, sender, content):
        # Найти чат по ID
        chat = next((c for c in self.chats if c.chat_id == chat_id), None)
        if not chat:
            raise ValueError(f"Чат с ID {chat_id} не существует.")
        # Проверить, что отправитель является участником чата
        if sender not in chat.participants:
            raise ValueError(f"Пользователь {sender} не является участником чата.")
        # Добавить сообщение в чат
        chat.add_message(sender, content)
        print(f"Сообщение от {sender} успешно отправлено в чат {chat_id}!")

    # --- РАБОТА СО СТАТУСОМ ---
    def change_user_status(self, username, new_status):
        user = next((u for u in self.users if u.username == username), None)
        if not user:
            raise ValueError(f"Пользователь с именем '{username}' не найден.")
        user.update_status(new_status)
        print(f"Статус пользователя {username} успешно обновлен на '{new_status}'.")

    # --- РАБОТА СО СПИСКОМ КОНТАКТОВ ---
    def add_contact(self, owner_name, contact_name):
        owner = next((u for u in self.users if u.username == owner_name), None)
        contact = next((u for u in self.users if u.username == contact_name), None)

        if not owner:
            raise ValueError(f"Пользователь '{owner_name}' не найден.")
        if not contact:
            raise ValueError(f"Пользователь '{contact_name}' не найден.")

        owner.contact_list.add_contact(contact_name)
        print(f"Пользователь {contact_name} успешно добавлен в контакты {owner_name}.")

    def remove_contact(self, owner_name, contact_name):
        owner = next((u for u in self.users if u.username == owner_name), None)
        if not owner:
            raise ValueError(f"Пользователь '{owner_name}' не найден.")

        owner.contact_list.remove_contact(contact_name)
        print(f"Пользователь {contact_name} успешно удален из контактов {owner_name}.")

    def show_contacts(self, owner_name):
        owner = next((u for u in self.users if u.username == owner_name), None)
        if not owner:
            raise ValueError(f"Пользователь '{owner_name}' не найден.")
        print(owner.contact_list)

    # --- ЗАПИСЬ И СЧИТЫВАНИЕ ДАННЫХ В ФАЙЛ И ИЗ ФАЙЛА ---
    def prepare_users_data(self):
        """Подготовить данные пользователей в виде списка словарей."""
        return [
            {
                "user_id": user.user_id,
                "username": user.username,
                "status": user.status.value,
            }
            for user in self.users
        ]

    def prepare_contacts_data(self):
        """Подготовить данные контактов для сохранения в JSON."""
        contacts_data = {}
        for user in self.users:
            contacts_data[user.username] = user.contact_list.to_dict()
        print(f"Контакты для сохранения: {contacts_data}")
        return contacts_data

    def load_users_from_json(self, filename="users.json"):
        data = JSONFileHandler.load_from_file(filename)
        if not data:
            print("Нет данных для загрузки.")
            return
        for user_data in data:
            try:
                self.add_user(user_data["username"])
                user = next(user for user in self.users if user.username == user_data["username"])
                user.update_status(user_data["status"])
            except ValueError as e:
                print(f"Ошибка загрузки пользователя {user_data['username']}: {e}")

    def load_users_from_xml(self, filename="users.json"):
        data = XMLFileHandler.load_from_file(filename)
        if not data:
            print("Нет данных для загрузки.")
            return
        for user_data in data:
            try:
                self.add_user(user_data["username"])
                user = next(user for user in self.users if user.username == user_data["username"])
                user.update_status(user_data["status"])
            except ValueError as e:
                print(f"Ошибка загрузки пользователя {user_data['username']}: {e}")

    # --- РАБОТА С ГРУППОВЫМИ ЧАТАМИ ---
    def add_group_chat(self, group_name, admin_name):
        if not any(user.username == admin_name for user in self.users):
            raise ValueError(f"Пользователь {admin_name} не найден.")
        chat_id = len(self.chats) + 1
        group_chat = GroupChat(chat_id=chat_id, group_name=group_name, admin=admin_name)
        self.chats.append(group_chat)
        print(f"Групповой чат '{group_name}' и успешно создан! Chat_ID: {chat_id}")

    def add_participant_to_group(self, chat_id, username):
        chat = next((c for c in self.chats if isinstance(c, GroupChat) and c.chat_id == chat_id), None)
        if not chat:
            raise ValueError(f"Групповой чат с ID {chat_id} не найден.")
        if not any(user.username == username for user in self.users):
            raise ValueError(f"Пользователь {username} не найден.")
        chat.add_participant(username)
        print(f"Пользователь {username} добавлен в группу '{chat.group_name}'.")

    def remove_participant_from_group(self, chat_id, username):
        chat = next((c for c in self.chats if isinstance(c, GroupChat) and c.chat_id == chat_id), None)
        if not chat:
            raise ValueError(f"Групповой чат с ID {chat_id} не найден.")
        chat.remove_participant(username)
        print(f"Пользователь {username} удален из группы '{chat.group_name}'.")

    def get_group_info(self, chat_id):
        chat = next((c for c in self.chats if isinstance(c, GroupChat) and c.chat_id == chat_id), None)
        if not chat:
            raise ValueError(f"Групповой чат с ID {chat_id} не найден.")
        info = chat.get_info()
        print(f"Групповой чат: {info['group_name']}, Админ: {info['admin']}")
        print(f"Участники: {', '.join(info['participants'])}")
        if info['messages']:
            print("Сообщения:")
            for msg in info['messages']:
                print(f"[{msg['timestamp']}] {msg['sender']}: {msg['content']}")
        else:
            print("В группе пока нет сообщений.")

    def save_contacts_to_json(self, filename="contacts.json"):
        """Сохранить список контактов в JSON-файл."""
        contacts_data = self.prepare_contacts_data()
        JSONFileHandler.save_to_file(contacts_data, filename)
        print(f"Контакты успешно сохранены в файл {filename}.")

    def load_contacts_from_json(self, filename="contacts.json"):
        """Загрузить список контактов из JSON-файла."""
        contacts_data = JSONFileHandler.load_from_file(filename)
        if not contacts_data:
            print("Нет данных для загрузки контактов.")
            return

        for username, contact_list_data in contacts_data.items():
            user = next((u for u in self.users if u.username == username), None)
            if not user:
                print(f"Пользователь {username} из файла контактов не найден. Пропускаем.")
                continue
            user.contact_list.contacts = contact_list_data.get("contacts", [])
            print(f"Контакты пользователя {username} успешно загружены.")

    def prepare_chats_data(self):
        """Подготовить данные чатов для сохранения в JSON."""
        chats_data = []
        for chat in self.chats:
            if isinstance(chat, PrivateChat):
                chat_type = "private"
                participants = chat.participants
            elif isinstance(chat, GroupChat):
                chat_type = "group"
                participants = chat.participants
            else:
                continue

            chats_data.append({
                "chat_id": chat.chat_id,
                "type": chat_type,
                "participants": participants,
                "messages": [
                    {
                        "sender": message.sender,
                        "content": message.content,
                        # Преобразование timestamp в строку, если это datetime, иначе оставляем как есть
                        "timestamp": message.timestamp.isoformat() if isinstance(message.timestamp, datetime) else message.timestamp
                    }
                    for message in chat.messages
                ]
            })
        return chats_data

    def save_chats_to_json(self, filename="chats.json"):
        """Сохранить чаты в JSON-файл."""
        try:
            chats_data = self.prepare_chats_data()
            JSONFileHandler.save_to_file(chats_data, filename)
            print(f"Чаты успешно сохранены в файл {filename}.")
        except Exception as e:
            print(f"Ошибка при сохранении чатов: {e}")





class User:
    def __init__(self, user_id, username, status=None):
        self.user_id = user_id
        self.username = username
        self.status = status or Status()  # По умолчанию статус "offline"
        self.contact_list = ContactList(username)
        self.contacts = []  # Список контактов пользователя

    def update_status(self, new_status):
        self.status.set_status(new_status)


class Chat:
    def __init__(self, chat_id: int, participants: list):
        self.chat_id = chat_id
        self.participants = participants  # Список участников
        self.messages = []  # Сообщения в чате

    def add_message(self, sender, content, timestamp=None):
        timestamp = timestamp or datetime.now().isoformat()
        self.messages.append(Message(sender, content, timestamp))

    def print_messages(self):
        # Вывод всех сообщений в чате
        if not self.messages:
            print(f"В чате {self.chat_id} пока нет сообщений.")
            return
        print(f"Сообщения в чате {self.chat_id}:")
        for message in self.messages:
            print(f"[{message.timestamp}] {message.sender}: {message.content}")

class PrivateChat(Chat):
    def __init__(self, chat_id: int, username1: str, username2: str):
        participants = [username1, username2]
        super().__init__(chat_id=chat_id, participants=participants) # Вызываем конструктор родительского класса CHat

class GroupChat(Chat):
    def __init__(self, chat_id: int, group_name: str, admin: str, participants=None):
        participants = participants or []  # Участники по умолчанию
        if admin not in participants:
            participants.append(admin)  # Администратор автоматически добавляется

        super().__init__(chat_id=chat_id, participants=participants)  # Вызываем конструктор родительского класса CHat
        self.group_name = group_name
        self.admin = admin

    def add_participant(self, user):
        if user in self.participants:
            raise ValueError(f"Пользователь {user} уже в группе.")
        self.participants.append(user)

    def remove_participant(self, user):
        if user not in self.participants:
            raise ValueError(f"Пользователь {user} не найден в группе.")
        if user == self.admin:
            raise ValueError("Нельзя удалить администратора группы.")
        self.participants.remove(user)

    def get_info(self):
        return {
            "group_name": self.group_name,
            "admin": self.admin,
            "participants": self.participants,
            "messages": [{"sender": m.sender, "content": m.content, "timestamp": m.timestamp} for m in self.messages]
        }

class Message:
    def __init__(self, sender, content, timestamp=None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()

# --- СТАТУС ---
class Status:
    def __init__(self, value="offline"):
        valid_statuses = ["online", "offline", "busy", "away"]
        if value not in valid_statuses:
            raise ValueError(f"Недопустимый статус: {value}. Допустимые статусы: {', '.join(valid_statuses)}.")
        self.value = value

    def set_status(self, new_status):
        valid_statuses = ["online", "offline", "busy", "away"]
        if new_status not in valid_statuses:
            raise ValueError(f"Недопустимый статус: {new_status}. Допустимые статусы: {', '.join(valid_statuses)}.")
        self.value = new_status

    def __str__(self):
        return self.value

#--- СПИСОК КОНТАКТОВ ---
class ContactList:
    def __init__(self, owner):
        self.owner = owner
        self.contacts = []

    def add_contact(self, username):
        if username in self.contacts:
            raise ValueError(f"Контакт {username} уже добавлен.")
        self.contacts.append(username)

    def remove_contact(self, username):
        if username not in self.contacts:
            raise ValueError(f"Контакт {username} не найден.")
        self.contacts.remove(username)

    def to_dict(self):
        """Преобразует список контактов в словарь для сохранения в JSON."""
        return {
            "owner": self.owner,
            "contacts": self.contacts
        }

    def __str__(self):
        return f"Контакты пользователя {self.owner}: {', '.join(self.contacts) if self.contacts else 'Нет контактов'}"