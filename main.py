if __name__ == "__main__":
    import ai
    import settings
    import tg_bot
    ai.write_or_rewrite_new_user_info(
        user_id=settings.BOT_DEVELOPER_TG_ID, user_full_name="HOMER", note="MatveyFilippov"
    )
    tg_bot.start()
