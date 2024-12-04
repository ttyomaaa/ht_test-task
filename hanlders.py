from tasks import TaskManager


def view_handler(task_manager: TaskManager, args):
    tasks = task_manager.view_tasks(args.category)
    for task in tasks:
        print(vars(task))


def edit_handler(task_manager: TaskManager, args):
    kwargs = vars(args)
    kwargs.pop('command_type')
    id_task = kwargs.pop('task_id')
    complete = kwargs.pop('complete')
    if complete == 'complete':
        do_complete = True
    else:
        do_complete = False
    updated_task = task_manager.edit_task(id_task, do_complete=do_complete, **kwargs)
    if updated_task:
        print(f"Обновлено: {vars(updated_task)}")
    else:
        print("Задача не найдена")


def add_handler(task_manager: TaskManager, args):
    new_task = task_manager.create_task(title=args.title,
                                        description=args.description,
                                        category=args.category,
                                        due_date=args.due_date,
                                        priority=args.priority)
    if new_task:
        print(f"Добавлено: {vars(new_task)}")
    else:
        print("Ошибка в данных")


def delete_handler(task_manager: TaskManager, args):
    if args.select == "all":
        if args.category:
            task_manager.delete_task(task_id=None, category=args.category)
        else:
            print("Категория не указана")
    else:
        if args.task_id:
            task_manager.delete_task(task_id=args.task_id, category=None)
        else:
            print("id не указан")


def search_handler(task_manager: TaskManager, args):
    kwargs = vars(args)
    kwargs.pop('command_type')
    tasks = task_manager.search_tasks(**kwargs)
    for task in tasks:
        print(vars(task))


def pass_handler(task_manager: TaskManager, args):
    pass
