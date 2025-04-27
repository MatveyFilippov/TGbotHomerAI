from enum import Enum, auto


class Direction(Enum):
    exit = 0
    update_code = auto()
    download_log = auto()
    delete_log = auto()
    delete_database = auto()
    stop_running = auto()
    start_running = auto()
    restart_running = auto()
    run_setup = auto()

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
