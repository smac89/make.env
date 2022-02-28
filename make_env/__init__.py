import os
import sys
from typing import Optional

from dotenv import find_dotenv, dotenv_values


def normalize_make_env(envs=os.environ) -> str:
    """normalize the environment variables for make

    `Make` still attempts to expand environment variables in the Makefile,
    so we need to redeclare them literally to avoid further expansion
    See: https://stackoverflow.com/q/27822266/2089675

    Args:
        envs (dict, optional): The environment variables. Defaults to os.environ.

    Returns:
        str: a snippet of Makefile to re-export the environment variables to be compatible with make

    >>> print(normalize_make_env({'FOO': 'bye', 'BAR': 'hello'}))
    export FOO:='$(value FOO)'
    export BAR:='$(value BAR)'

    >>> print(normalize_make_env({'FOO': 'hello$world', 'BAR': 'bye#world'}))
    export FOO:='$(value FOO)'
    export BAR:='$(value BAR)'
    """
    return "\n".join(f"export {k}:='$(value {k})'" for k in envs)


def load_make_env(args: list[str] = sys.argv) -> Optional[str]:
    """load the environment variables from the .env file

    Returns:
        Optional[str]: returns an eval snippet to be used with make

    >>> import tempfile
    >>> import os
    >>> print(load_make_env(["make", "-h"]))
    None
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     with open(os.path.join(tmpdir, ".env"), "w") as f:
    ...         print ("", file=f)
    ...     print(load_make_env(["make.env", "--directory", tmpdir]))
    ...     with open(os.path.join(tmpdir, ".env"), "w") as f:
    ...         print ("FOO=hello", file=f)
    ...     print(load_make_env(["make.env", "--directory", tmpdir]))
    None
    export FOO:='$(value FOO)'
    """

    if any(x in args for x in ("-h", "--help", "-v", "--version")):
        return None

    if any((arg_name := arg) in args for arg in ("-C", "--directory")):
        if args[-1] == arg_name:
            return None
        dot_env_dir_path = os.path.abspath(args[args.index(arg_name) + 1])
    else:
        dot_env_dir_path = os.getcwd()

    if envfile := find_dotenv(
        usecwd=True, filename=os.path.join(dot_env_dir_path, ".env")
    ):
        denv = dotenv_values(envfile)
        if any((v := os.environ.get(k)) is None or v != denv[k] for k in denv):

            if not any(x in args for x in ("--quiet", "--silent", "-s")):
                print(
                    f"\u001b[1;40;37mLoading .env from {envfile}...\u001b[0m",
                    file=sys.stderr,
                )

            os.environ.update({k: "" if v is None else v for k, v in denv.items()})

            return normalize_make_env(denv)

    return None


def main():
    if exports := load_make_env():
        os.execlp("make", *sys.argv, "--eval", exports)
    os.execlp("make", *sys.argv)
