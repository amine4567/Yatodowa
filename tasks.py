from invoke import task

from backend.yatodowa_api.app import create_app


# Python reqs
@task
def update_app_reqs(c):
    c.run("pip-compile backend/requirements.in")


@task
def update_combined_reqs(c):
    c.run(
        "pip-compile backend/requirements.in requirements-dev.in -o requirements-combined.txt"
    )


# Run
@task
def run_backend(c):
    create_app().run()


@task
def run(c):
    run_backend(c)
