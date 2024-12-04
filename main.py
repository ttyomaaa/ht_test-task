from commands import command_parser
from tasks import TaskManager
from hanlders import view_handler, edit_handler, add_handler, delete_handler, search_handler, pass_handler

COMMANDS = {
    'view': view_handler,
    'edit': edit_handler,
    'add': add_handler,
    'delete': delete_handler,
    'search': search_handler,
    None: pass_handler
}


def main():
    task_manager = TaskManager('tasks.json')
    while True:
        command = input("> Введите --help для списка доступных опций или exit для выхода: ")
        if command == "exit":
            break
        try:
            args = command_parser(command)
        except SystemExit:
            continue

        COMMANDS[args.command_type](task_manager, args)


if __name__ == "__main__":
    main()
