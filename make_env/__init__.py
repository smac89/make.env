import os
import sys
from typing import Optional, List

from dotenv import find_dotenv, dotenv_values


def normalize_make_env(envs=os.environ) -> Optional[str]:
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

    >>> print(normalize_make_env({}))
    None
    """
    if envs:
        return "\n".join(f"export {k}:='$(value {k})'" for k in envs)
    return None


def load_make_env(args: List[str] = sys.argv) -> Optional[str]:
    """load the environment variables from the .env file

    Args:
        args (List[str], optional): The command line arguments. Defaults to sys.argv.

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
    ...     print(load_make_env(["make.env", "-C", tmpdir]))
    None
    export FOO:='$(value FOO)'
    """

    if any(x in args for x in ("-h", "--help", "-v", "--version")):
        return None

    arg_name = next(filter(lambda arg: arg in args, ("-C", "--directory")), None)
    if not arg_name:
        dot_env_dir_path = os.getcwd()
    elif args[-1] != arg_name:
        dot_env_dir_path = os.path.abspath(args[args.index(arg_name) + 1])
    else:
        return None

    envfile = find_dotenv(usecwd=True, filename=os.path.join(dot_env_dir_path, ".env"))
    if envfile:
        denv = dotenv_values(envfile)
        if any(os.environ.get(k) != v for k, v in denv.items()):

            if not any(x in args for x in ("--quiet", "--silent", "-s")):
                print(
                    f"\u001b[1;40;37mLoading .env from {envfile}...\u001b[0m",
                    file=sys.stderr,
                )

            os.environ.update({k: "" if v is None else v for k, v in denv.items()})

        return normalize_make_env(denv)

    return None


def main():
    exports = load_make_env()
    if exports:
        os.execlp("make", *sys.argv, "--eval", exports)
    os.execlp("make", *sys.argv)
