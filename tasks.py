from invoke import task
from yatodowa_api.app import create_app


# Python reqs
@task
def update_app_reqs(c):
    c.run("pip-compile backend/src/requirements.in")


@task
def update_combined_reqs(c):
    c.run(
        "pip-compile backend/src/requirements.in backend/requirements-dev.in -o backend/requirements-combined.txt"
    )


# Run
@task
def run_back(c):
    create_app().run()


@task
def run_front(c):
    c.run("cd frontend; ng serve")


@task
def run(c):
    c.run("invoke run-back & invoke run-front")


# Flask-migrate
@task
def db_init(c):
    c.run("cd backend/src/yatodowa_api; flask db init")


@task
def db_migrate(c, message):
    c.run(f'cd backend/src/yatodowa_api; flask db migrate -m "{message}"')


@task
def db_upgrade(c):
    c.run("cd backend/src/yatodowa_api; flask db upgrade")
