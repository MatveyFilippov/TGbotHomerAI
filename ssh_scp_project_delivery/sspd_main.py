if __name__ == "__main__":
    from directions import Direction
    import sspd
    try:
        while True:
            user_decision = Direction.get_direction()
            if user_decision == Direction.exit:
                break
            elif user_decision == Direction.download_log:
                sspd.tasks.download_log_file()
            elif user_decision == Direction.delete_log:
                sspd.tasks.execute_remote_command(
                    command="rm ChatGPTBot.log", in_dir=sspd.base.REMOTE_PROJECT_DIR_PATH, ignore_error=True,
                )
            elif user_decision == Direction.delete_database:
                sspd.tasks.execute_remote_command(
                    command="rm ChatGPTBot.db", in_dir=sspd.base.REMOTE_PROJECT_DIR_PATH,
                )
            elif user_decision == Direction.run_setup:
                from remote_setup_runner import run_remote_setup
                run_remote_setup()
            elif user_decision == Direction.update_code:
                sspd.tasks.update_remote_code()
            elif user_decision == Direction.restart_running:
                sspd.tasks.restart_running_remote_code()
            elif user_decision == Direction.stop_running:
                sspd.tasks.stop_running_remote_code()
            elif user_decision == Direction.start_running:
                sspd.tasks.start_running_remote_code()
            print()
    finally:
        sspd.close_connections()
