import pytest
import json
import os
import tempfile
from task_manager import TaskManager


class TestTaskManager:

    def test_add_and_complete_task(self):
        # Создаем экземпляр TaskManager
        task_manager = TaskManager()

        # Добавляем задачу
        task_manager.add_task("Тестовая задача")

        # Проверяем, что задача добавлена
        assert 1 in task_manager.tasks  # ID должен быть 1
        assert task_manager.tasks[1]["description"] == "Тестовая задача"

        # Проверяем начальный статус (должен быть False)
        assert task_manager.tasks[1]["completed"] == False

        # Отмечаем задачу как выполненную
        task_manager.complete_task(1)

        # Проверяем, что статус изменился на True
        assert task_manager.tasks[1]["completed"] == True

    def test_remove_task(self):
        # Создаем экземпляр TaskManager
        task_manager = TaskManager()

        # Добавляем две задачи
        task_manager.add_task("Первая задача")
        task_manager.add_task("Вторая задача")

        # Проверяем, что задачи добавлены
        assert len(task_manager.tasks) == 2  # Должно быть 2 задачи
        assert 1 in task_manager.tasks  # Первая задача
        assert 2 in task_manager.tasks  # Вторая задача

        # Удаляем первую задачу
        task_manager.remove_task(1)

        # Проверяем, что первая задача удалена
        assert len(task_manager.tasks) == 1  # Осталась только 1 задача
        assert 1 not in task_manager.tasks  # Первой задачи нет
        assert 2 in task_manager.tasks  # Вторая задача осталась

        # Проверяем, что вторая задача не изменилась
        assert task_manager.tasks[2]["description"] == "Вторая задача"

    def test_save_and_load_from_json(self):
        # Создаем временный файл для теста
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            # Получаем имя файла без расширения .json
            base_name = os.path.splitext(temp_path)[0]

            # Создаем первый менеджер и добавляем задачи
            task_manager1 = TaskManager()
            task_manager1.add_task("Задача для сохранения")
            task_manager1.add_task("Другая задача")
            task_manager1.complete_task(1)  # Отмечаем первую как выполненную

            # Сохраняем задачи в JSON
            task_manager1.save_to_json(base_name)

            # Проверяем, что файл создан
            json_file = base_name + '.json'
            assert os.path.exists(json_file), f"Файл {json_file} не создан"

            # Проверяем содержимое файла
            with open(json_file, 'r', encoding='utf-8') as file:
                saved_data = json.load(file)

            # Проверяем корректность сохраненных данных
            assert len(saved_data) == 2, "Должно быть сохранено 2 задачи"
            assert saved_data["1"]["description"] == "Задача для сохранения"
            assert saved_data["1"]["completed"] == True, "Первая задача должна быть выполнена"
            assert saved_data["2"]["description"] == "Другая задача"
            assert saved_data["2"]["completed"] == False, "Вторая задача не должна быть выполнена"

            # Создаем новый менеджер и загружаем задачи
            task_manager2 = TaskManager()
            task_manager2.load_from_json(base_name)

            # Проверяем, что задачи загружены корректно
            assert len(task_manager2.tasks) == 2, "Должно быть загружено 2 задачи"
            assert task_manager2.tasks[1]["description"] == "Задача для сохранения"
            assert task_manager2.tasks[1]["completed"] == True, "Первая задача должна быть выполнена"
            assert task_manager2.tasks[2]["description"] == "Другая задача"
            assert task_manager2.tasks[2]["completed"] == False, "Вторая задача не должна быть выполнена"

            # Проверяем, что next_id установлен правильно
            assert task_manager2.next_id == 3, "next_id должен быть равен 3 (следующий ID после 2)"

        finally:
            # Удаляем временный файл после теста
            if os.path.exists(base_name + '.json'):
                os.remove(base_name + '.json')