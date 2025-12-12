import pytest
import json
import os
import tempfile
from task_manager import TaskManager


class TestTaskManager:

    def test_add_task(self):
        # Создаем экземпляр TaskManager
        task_manager = TaskManager()

        # Добавляем задач
        task_manager.add_task("Тестовая задача 1")
        task_manager.add_task("Тестовая задача 2")

        # Проверяем, что задачи добавлены
        assert len(task_manager.tasks) == 2, "Задачи должны быть добавлены"

        # Проверяем, что задачи добавлены корректно
        assert task_manager.tasks[1]["description"] == "Тестовая задача 1", "Текст задачи 1 сохраняется не корректно"
        assert task_manager.tasks[2]["description"] == "Тестовая задача 2", "Текст задачи 2 сохраняется не корректно"

        # Проверяем, что при создании задачи она не выполнена
        assert task_manager.tasks[1]["completed"] is False, "Задача должна создаваться как Невыполненая"

    def test_complete_task(self):
        # Создаем экземпляр TaskManager
        task_manager = TaskManager()

        # Добавляем задачу
        task_manager.add_task("Тестовая задача")

        # Отмечаем задачу как выполненную
        task_manager.complete_task(1)

        # Проверяем, что статус изменился на True
        assert task_manager.tasks[1]["completed"] is True, "Статус должен быть - Выполнено"

    def test_remove_task(self):
        # Создаем экземпляр TaskManager
        task_manager = TaskManager()

        # Добавляем две задачи
        task_manager.add_task("Первая задача")
        task_manager.add_task("Вторая задача")

        # Удаляем первую задачу
        task_manager.remove_task(1)

        # Проверяем, что задача удалена
        assert len(task_manager.tasks) == 1, "Задача должна быть удалена"
        # Проверяем, что удалена указанная задача
        assert "Первая задача" not in task_manager.tasks, """\"Первая задача\" должна отсутствовать"""

    def test_save_and_load_from_json(self):
        # Создаем временный файл для теста
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            # Получаем имя файла без расширения .json
            base_name = os.path.splitext(temp_path)[0]

            # Создаем первый менеджер и добавляем задачи
            task_manager_1 = TaskManager()
            task_manager_1.add_task("Задача для сохранения")
            task_manager_1.add_task("Другая задача")
            task_manager_1.complete_task(1)  # Отмечаем первую как выполненную

            # Сохраняем задачи в JSON
            task_manager_1.save_to_json(base_name)

            # Проверяем, что файл создан
            json_file = base_name + '.json'
            assert os.path.exists(json_file), f"Файл {json_file} не создан"

            # Проверяем содержимое файла
            with open(json_file, 'r', encoding='utf-8') as file:
                saved_data = json.load(file)

            # Проверяем корректность сохраненных данных
            assert len(saved_data) == 2, "Должно быть сохранено 2 задачи"
            assert saved_data["1"]["description"] == "Задача для сохранения"
            assert saved_data["1"]["completed"] is True, "Первая задача должна быть выполнена"
            assert saved_data["2"]["description"] == "Другая задача"
            assert saved_data["2"]["completed"] is False, "Вторая задача не должна быть выполнена"

            # Создаем новый менеджер и загружаем задачи
            task_manager_2 = TaskManager()
            task_manager_2.load_from_json(base_name)

            # Проверяем, что задачи загружены корректно
            assert len(task_manager_2.tasks) == len(task_manager_1.tasks), "Должно быть загружено 2 задачи"
            assert task_manager_2.tasks[1]["description"] == task_manager_1.tasks[1]["description"], "Описание первой задачи, должно соответствовать сохраненному"
            assert task_manager_2.tasks[1]["completed"] is task_manager_1.tasks[1]["completed"], "Первая задача должна быть выполнена"
            assert task_manager_2.tasks[2]["description"] == task_manager_1.tasks[2]["description"], "Описание второй задачи, должно соответствовать сохраненному"
            assert task_manager_2.tasks[2]["completed"] is task_manager_1.tasks[2]["completed"], "Вторая задача не должна быть выполнена"

            # Проверяем, что next_id установлен правильно
            assert task_manager_2.next_id == 3, "next_id должен быть равен 3 (следующий ID после 2)"

        finally:
            # Удаляем временный файл после теста
            if os.path.exists(base_name + '.json'):
                os.remove(base_name + '.json')