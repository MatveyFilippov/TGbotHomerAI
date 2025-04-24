from enum import Enum


class Direction(Enum):
    exit = 0
    update_code = 1
    download_logs = 2
    delete_logs = 3
    delete_database = 4
    stop_running = 5
    start_running = 6
    restart_running = 7
    run_setup = 8

    @classmethod
    def get_direction(cls) -> 'Direction':
        print("Choose what will be done")
        for direction in cls:
            name = direction.name.replace("_", " ").title()
            print(f" * {name} ({direction.value})")
        try:
            return cls(int(input(": ").strip()))
        except ValueError:
            print("No such variant -> exit")
            return cls.exit
