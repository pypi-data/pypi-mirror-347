# bucho

`bucho` is a package for exercises. Yes, we love bucho!

## Setup

```
$ pip install bucho
```

## Plugin

Plugin entry point is `bucho.commands`.

## Development

Install uv:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Build package:
```
uvx --from build pyproject-build
```

Formatting:
```
uvx ruff format .
```

Testing:
```
uvx pytest
```
