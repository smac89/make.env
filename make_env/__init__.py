import os
import sys

from dotenv import load_dotenv, find_dotenv


def main():
    if envfile := find_dotenv(usecwd=True):
        if not any(
            map(lambda x: x in sys.argv, ["-h", "--help", "--quiet", "--silent", "-s"])
        ):
            print(f"\u001b[1;40;37mLoading .env from {envfile}...\u001b[0m")
        load_dotenv(dotenv_path=envfile)
    os.execlp("make", *sys.argv)
