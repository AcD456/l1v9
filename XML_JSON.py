import json
import xml.etree.ElementTree as ETree


class JSONFileHandler:
    """Класс для работы с JSON-файлами."""

    @staticmethod
    def save_to_file(data, filename="users.json"):
        """Сохраняет данные в JSON-файл."""
        try:
            with open(filename, "w", encoding="utf-8") as file:
                # noinspection PyTypeChecker
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Данные успешно сохранены в JSON файл: {filename}")
        except Exception as e:
            print(f"Ошибка записи в JSON файл: {e}")

    @staticmethod
    def load_from_file(filename="users.json"):
        """Загружает данные из JSON-файла."""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            print(f"Данные успешно загружены из JSON файла: {filename}")
            return data
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON файла {filename}.")
        except Exception as e:
            print(f"Ошибка: {e}")
        return None

class XMLFileHandler:
    """Класс для работы с XML-файлами."""

    @staticmethod
    def save_to_file(data, filename="users.xml"):
        """Сохраняет данные в XML-файл."""
        try:
            root = ETree.Element("Users")
            for user in data:
                user_element = ETree.SubElement(root, "User")
                ETree.SubElement(user_element, "UserID").text = str(user["user_id"])
                ETree.SubElement(user_element, "Username").text = user["username"]
                ETree.SubElement(user_element, "Status").text = user["status"]

            tree = ETree.ElementTree(root)
            tree.write(filename, encoding="utf-8", xml_declaration=True)
            print(f"Данные успешно сохранены в XML файл: {filename}")
        except Exception as e:
            print(f"Ошибка записи в XML файл: {e}")

    @staticmethod
    def load_from_file(filename="users.xml"):
        """Загружает данные из XML-файла."""
        try:
            tree = ETree.parse(filename)
            root = tree.getroot()
            data = []
            for user_element in root.findall("User"):
                user_data = {
                    "user_id": int(user_element.find("UserID").text),
                    "username": user_element.find("Username").text,
                    "status": user_element.find("Status").text,
                }
                data.append(user_data)
            print(f"Данные успешно загружены из XML файла: {filename}")
            return data
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except ETree.ParseError:
            print(f"Ошибка чтения XML файла {filename}.")
        except Exception as e:
            print(f"Ошибка: {e}")
        return None