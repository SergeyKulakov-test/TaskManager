import json
import os


class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add_task(self, description: str):
        task_id = self.next_id
        self.tasks[task_id] = {"description": description, "completed": False}
        print(f"Задача #{task_id} '{description}' добавлена")
        self.next_id += 1

    def complete_task(self, index: int):
        try:
            if index in self.tasks:
                self.tasks[index]["completed"] = True
                print(f"Задача #{index} отмечена как выполненная")
            else:
                print(f"Ошибка: Задача #{index} не найдена")
        except ValueError:
            print(f"Ошибка: ID задачи должен быть числом.")

    def remove_task(self, index: int):
        try:
            if index in self.tasks:
                task_text = self.tasks[index]["description"]
                del self.tasks[index]
                print(f"Задача #{index} '{task_text}' удалена.")
            else:
                print(f"Ошибка: Задача #{index} не найдена")
        except ValueError:
            print(f"Ошибка: ID задачи должен быть числом.")

    def save_to_json(self, filename: str):
        try:
            if filename.endswith('.json'):
                filename = filename[:-5]

            full_filename = f"{filename}.json"
            with open(full_filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, indent=4, ensure_ascii=False)
            print(f"Задачи успешно сохранены в файл '{full_filename}'")
            print(f"Полный путь к файлу: {os.path.abspath(full_filename)}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def load_from_json(self, filename: str):
        try:
            if filename.endswith('.json'):
                filename = filename[:-5]
            full_filename = f"{filename}.json"
            with open(full_filename, 'r', encoding='utf-8') as file:
                loaded_tasks = json.load(file)
                self.tasks = {int(k): v for k, v in loaded_tasks.items()}
                if self.tasks:
                    self.next_id = max(self.tasks.keys()) + 1
                else:
                    self.next_id = 1
                print(f"Задачи успешно загружены из файла '{full_filename}'")
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}.json' не найден")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст")
            return
        print("\nСписок задач:")
        for task_id, task_info in self.tasks.items():
            status = "Выполнено" if task_info["completed"] else "Не выполнено"
            print(f"{task_id}. [{status}] {task_info['description']}")


def get_task_id_input(prompt):
    while True:
        try:
            task_id = int(input(prompt))
            return task_id
        except ValueError:
            print("Ошибка: Введите корректный номер задачи (целое число)")