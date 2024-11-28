import nox

NEED_STUB: list[str] = [
    "aurum/__init__.py",
    "aurum/commands/__init__.py",
    "aurum/commands/decorators/__init__.py",
    "aurum/commands/impl/__init__.py",
]


def _generate_stubs(session: nox.Session) -> None:
    session.run("stubgen", *NEED_STUB, "-o", ".", "--include-private", "--no-import")

    stub_paths = [path + "i" for path in NEED_STUB]

    session.run("ruff", "format", *stub_paths)
    session.run("ruff", "check", "--select", "I", "--fix", *stub_paths)

    for stub_path in stub_paths:
        with open(stub_path, "r") as fp:
            content = fp.read()

        with open(stub_path, "w", encoding="UTF-8") as fp:
            fp.write("# DO NOT MANUALLY EDIT THIS FILE!\n")
            fp.write("# This file was automatically generated by `nox -s generate_stubs`\n\n")
            fp.write(content)


@nox.session(venv_backend="uv")
def generate_stubs(session: nox.Session) -> None:
    """Generate the stubs for the module"""
    session.run_install(
        "uv",
        "sync",
        "--extra=typing",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    _generate_stubs(session)