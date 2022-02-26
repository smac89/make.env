# make.env
[![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/smac89/make.env/Python%20application?event=push&label=tests&style=for-the-badge)](https://github.com/smac89/make.env/actions/workflows/python-app.yml)
[![PyPI](https://img.shields.io/pypi/v/make.env?style=for-the-badge)](https://pypi.org/project/make.env/)
[![GitHub](https://img.shields.io/github/license/smac89/make.env?style=for-the-badge)](https://github.com/smac89/make.env/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/make.env?style=for-the-badge)](https://pypi.org/project/make.env/)

Infuses [GNU make](https://www.gnu.org/software/make/) with the ability to read .env files

## Motivation
Often when working with Makefiles, you might have the need to read environment variables from a `.env` file, and have `make` treat them as if the environment variables were actually variables in the Makefile.

The most [popular](https://unix.stackexchange.com/a/348432/44793) solution is to import the `.env` file into the Makefile, and then export every varaible declared so far:

```makefile
include .env
export
```

The problem with this is that it is prone to errors. For example, if your `.env` file contains the following:

```sh
APP_PASSWORD='8oyy!r#vNpRy2TT'
```

The variable `APP_PASSWORD` will be exported with the value `'8oyy!r`. Likewise, if your `.env` file contains the following:

```sh
APP_PASSWORD='Qy%$%J9$rD#jqVw'
```

The variable `APP_PASSWORD` will be exported with the value `'Qy%J9D`.

What's more, any attempt to use this variable will result in an error in `make` concerning the lack of a closing quote:

> unexpected EOF while looking for matching `''

### Explanaition

In both cases, `APP_PASSWORD` contained values which `make` treats specially.

_The `#` is used to start comments, therefore as soon as make sees a `#`, it will ignore the rest of the line._

_The `$` is used to reference a variable or function, so when make sees a `$`, it will treat whatever comes after it as a variable or function reference._

## The solution
That's where this wrapper comes in. *It allows us to read a `.env` file and pass them to `make`* in a way that allows `make` to treat them as variables and copy their values literally rather than attempting to interpret them.
