import nox


@nox.session(venv_backend="uv")
def tests(session: nox.Session) -> None:
    """Run tests"""
    session.run_install("uv", "sync", "--extra=tests", env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location})
    session.run("pytest", *session.posargs)
