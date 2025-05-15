# History

## 0.1.3 (2025-05-15)

- Drop Python 2.x support
- Updated minimum Python version to 3.10
- Modernized code for Python 3.10+:
  - Remove Python2 compatibility (removed compat.py dependency)
  - Replaced urllib with urllib.request, urllib.parse, urllib.error
  - Improved Tkinter imports to use modern syntax
  - Improved docstrings
  - Improved code formatting (applying `ruff format`)
  - Improved plugin loading with importlib.metadata for Python 3.10+
- Modernized packaging
    - Migration from setup.py and setup.cfg to pyproject.toml
    - Changed README.txt to README.md (Markdown format)
    - Moved tests.py from bucho/ directory to root directory
    - Added uv.lock for dependency management

## 0.1.2 (2012-06-13)

- bucho shows something graphically

## 0.1.1 (2011-06-17)

- bucho becomes pluggable

## 0.1.0 (2011-05-01)

- bucho now work with Python3.
- rename `bucho.wsgi.wsgi_app` into `bucho.wsgi.application`.
- fixed: all_status return only a single status.
- fixed: bucho.command cause exception when print unicode.

## 0.0.5 (2011-02-27)

- add `bucho` console script.
- add `bucho.wsgi.wsgi_app` wsgi application.
- add `main` entry point for paste.app_factory.
- some functions show(),latest_status(),all_status() stop print text and now return text. this is incompatible change.

## 0.0.4 (2010-07-10)

- add latest_status, all_status
- add torumemo

## 0.0.3 (2010-07-10)

- bucho can show !

## 0.0.2 (2010-07-10)

- you can import bucho

## 0.0.1 (2010-07-10)

- first release
