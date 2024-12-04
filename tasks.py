import json
import datetime


class Task:
    def __init__(self,
                 id: int,
                 title: str,
                 description: str,
                 category: str,
                 due_date: str,
                 priority: str,
                 status: str = "Не выполнена"
                 ):
        if not title or not description or not category or not due_date or not priority:
            raise ValueError("Не все поля заполнены")
        try:
            datetime.datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Неверный формат даты")
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    @staticmethod
    def from_dict(data: dict):
        return Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            category=data['category'],
            due_date=data['due_date'],
            priority=data['priority'],
            status=data['status']
        )


class TaskManager:
    def __init__(self, path: str):
        self.path = path
        self.tasks: list[Task] = []
        self.max_id = 0
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
                for task in json_data:
                    self.tasks.append(Task.from_dict(task))
                    if task["id"] > self.max_id:
                        self.max_id = task["id"]
        except (FileNotFoundError, KeyError, ValueError) as e:
            print(e)

    def save_tasks(self):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump([vars(task) for task in self.tasks], file, indent=4)
        except FileNotFoundError as e:
            print(e)

    def create_task(self, title: str, description: str, category: str, due_date: str, priority: str) -> Task | None:
        try:
            new_task = Task(id=self.max_id+1,
                            title=title,
                            description=description,
                            category=category,
                            due_date=due_date,
                            priority=priority)
        except ValueError as e:
            print(e)
            return
        self.add_tasks(new_task)
        return new_task

    def add_tasks(self, task: Task):
        self.tasks.append(task)
        self.max_id += 1
        self.save_tasks()

    def view_tasks(self, category: str | None) -> list[Task]:
        if category:
            return [task for task in self.tasks if task.category.lower() == category.lower()]
        return self.tasks

    def edit_task(self, task_id: int, do_complete: bool, **kwargs) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if value:
                        setattr(task, key, value)
                if do_complete:
                    task.status = 'Выполнена'
                self.save_tasks()
                return task

    def delete_task(self, task_id: int | None, category: str | None) -> None:
        if category:
            self.tasks = [task for task in self.tasks if task.category != category]
            self.save_tasks()
            return
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
        return

    def search_tasks(self, **kwargs) -> list[Task]:
        results = []
        for key, value in kwargs.items():
            for task in self.tasks:
                if getattr(task, key) == value:
                    results.append(task)
        results_unique = list(dict.fromkeys(results))
        return results_unique
