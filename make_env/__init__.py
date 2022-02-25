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
                print(
                    f"\u001b[1;40;37mLoading .env from {envfile}...\u001b[0m",
                    file=sys.stderr,
                )

            os.environ.update(
                {
                    k: "" if v is None else v
                    for k, v in denv.items()
                    if os.environ.get(k) != v
                }
            )

            return "\n".join(f"export {k}:=$(value {k})" for k in denv)

    return None


def main():
    exports = load_make_env() or "$(call)"
    os.execlp("make", *sys.argv, "--eval", exports)
