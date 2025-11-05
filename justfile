run_checks:
    uv run mypy src/wheel_getter/
    ty check src/wheel_getter/
    pyrefly check src/wheel_getter/
    uv run --with pyright pyright src/wheel_getter/
    ruff check src/wheel_getter/
