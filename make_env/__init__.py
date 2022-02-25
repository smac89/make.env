import os
import sys

from dotenv import find_dotenv, dotenv_values


def load_make_env():
    if envfile := find_dotenv(usecwd=True):
        denv = dotenv_values(envfile)
        if any((v := os.environ.get(k)) is None or v != denv[k] for k in denv):
            if not any(
                map(
                    lambda x: x in sys.argv,
                    ["-h", "--help", "--quiet", "--silent", "-s"],
                )
            ):
                print(f"\u001b[1;40;37mLoading .env from {envfile}...\u001b[0m")

        os.environ.update(
            {
                k: "" if v is None else v.replace("$", "$$")
                for k, v in denv.items()
                if os.environ.get(k) != v
            }
        )


def main():
    load_make_env()
    os.execlp("make", *sys.argv)
