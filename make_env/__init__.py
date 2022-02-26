import os
import sys

from dotenv import find_dotenv, dotenv_values


def load_make_env():
    if envfile := find_dotenv(usecwd=True):
        denv = dotenv_values(envfile)
        if any((v := os.environ.get(k)) is None or v != denv[k] for k in denv):
            if not any(
                x in sys.argv for x in ["-h", "--help", "--quiet", "--silent", "-s"]
            ):
                print(
                    f"\u001b[1;40;37mLoading .env from {envfile}...\u001b[0m",
                    file=sys.stderr,
                    flush=True,
                )

            os.environ.update({k: "" if v is None else v for k, v in denv.items()})

            # load all env vars into Makefile using the --eval flag
            return "\n".join(f"export {k}:=$(value {k})" for k in denv)

    return None


def main():
    if exports := load_make_env():
        os.execlp("make", *sys.argv, "--eval", exports)
    os.execlp("make", *sys.argv)
