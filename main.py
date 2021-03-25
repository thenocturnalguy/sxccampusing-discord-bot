import os
from bot import client
from lib.keep_alive import keep_alive
from dotenv import load_dotenv


def __main__():
    # Keep alive!
    keep_alive()

    # Go live!
    load_dotenv()
    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    __main__()
