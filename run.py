import multiprocessing
import subprocess

"""
 This file for working Flask and aiogram at the same time
"""

api_process = multiprocessing.Process(
    target=subprocess.run,
    kwargs={"args": f"python -m flask_app.app", "shell": True},
)


bot_process = multiprocessing.Process(
    target=subprocess.run,
    kwargs={"args": f"python -m bot.main", "shell": True},
)


if __name__ == "__main__":
    api_process.start()
    bot_process.start()
