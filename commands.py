import argparse
import shlex


def command_parser(command: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Менеджер задач")
    subparsers = parser.add_subparsers(dest="command_type", help="Команды")

    parser_view = subparsers.add_parser('view', help="Просмотр всех задач")
    parser_view.add_argument('--category', type=str, help="Категория задачи для просмотра")

    parser_add = subparsers.add_parser('add', help="Добавить задачу")
    parser_add.add_argument('title', type=str, help="Название задачи")
    parser_add.add_argument('description', type=str, help="Описание задачи")
    parser_add.add_argument('category', type=str, help="Категория задачи")
    parser_add.add_argument('due_date', type=str, help="Срок выполнения задачи")
    parser_add.add_argument('priority', type=str, help="Приоритет (низкий, средний, высокий)")

    parser_edit = subparsers.add_parser('edit', help="Редактировать задачу")
    parser_edit.add_argument('task_id', type=int, help="id задачи для редактирования или завершения")
    parser_edit.add_argument('complete', const="pass", choices=["complete", "pass"], nargs='?', type=str, help="Завершить задачу (complete)")
    parser_edit.add_argument('--title', type=str, help="Новое название задачи")
    parser_edit.add_argument('--description', type=str, help="Новое описание задачи")
    parser_edit.add_argument('--category', type=str, help="Новая категория задачи")
    parser_edit.add_argument('--due_date', type=str, help="Новый срок выполнения задачи")
    parser_edit.add_argument('--priority', type=str, help="Новый приоритет (низкий, средний, высокий)")

    parser_delete = subparsers.add_parser('delete', help="Удалить задачу")
    parser_delete.add_argument('select', const="id", choices=["all", "id"], nargs='?', type=str, help="Завершить все задачи категории (all)")
    parser_delete.add_argument('--task_id', type=int, help="id задачи для удаления")
    parser_delete.add_argument('--category', type=str, help="Категория задачи для удаления")

    parser_search = subparsers.add_parser('search', help="Поиск задач")
    parser_search.add_argument('--title', type=str, help="Ключевое слово для поиска")
    parser_search.add_argument('--category', type=str, help="Категория задачи для поиска")
    parser_search.add_argument('--status', type=str, help="Статус задачи для поиска")

    return parser.parse_args(shlex.split(command))
