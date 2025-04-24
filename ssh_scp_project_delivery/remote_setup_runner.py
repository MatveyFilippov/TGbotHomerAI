import sspd


def __send_script():
    sspd.tasks.send_file_to_remote_server(
        local_filepath="remote_setup_script.py", remote_filepath=f"{sspd.base.REMOTE_PROJECT_DIR_PATH}/setup.py",
    )


def __remove_unused_files():
    sspd.tasks.execute_remote_command(
        f"find {sspd.base.REMOTE_PROJECT_DIR_PATH}"+""" -type f -name "*.py" -not -path "*/venv/*" -exec rm -f {} +""",
        print_response=True, ignore_error=True,
    )
    sspd.tasks.execute_remote_command(
        f"find {sspd.base.REMOTE_PROJECT_DIR_PATH}"+""" -type f -name "*.c" -not -path "*/venv/*" -exec rm -f {} +""",
        print_response=True, ignore_error=True,
    )
    sspd.tasks.execute_remote_command(
        f"find {sspd.base.REMOTE_PROJECT_DIR_PATH}"+""" -type d -name "__pycache__" -not -path "*/venv/*" -exec rm -rf {} +""",
        print_response=True, ignore_error=True,
    )
    sspd.tasks.execute_remote_command(
        "rm -rf build", in_dir=sspd.base.REMOTE_PROJECT_DIR_PATH, print_response=True, ignore_error=True,
    )


def __execute_script():
    sspd.tasks.execute_remote_command(
        f"{sspd.base.REMOTE_PROJECT_DIR_PATH}/{sspd.base.REMOTE_VENV_DIR_NAME}/bin/pip install -U cython",
        print_response=True
    )
    sspd.tasks.execute_remote_command(
        f"{sspd.base.REMOTE_VENV_DIR_NAME}/bin/python3 setup.py build_ext --inplace",
        in_dir=sspd.base.REMOTE_PROJECT_DIR_PATH, print_response=True, ignore_error=True,
    )


def run_remote_setup():
    __send_script()
    __execute_script()
    __remove_unused_files()
    sspd.tasks.send_file_to_remote_server(
        local_filepath="../main.py", remote_filepath=f"{sspd.base.REMOTE_PROJECT_DIR_PATH}/main.py",
    )
