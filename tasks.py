from invoke import task


# Python reqs
@task
def update_app_reqs(c):
    c.run("pip-compile src/requirements.in")


@task
def update_combined_reqs(c):
    c.run(
        "pip-compile src/requirements.in requirements-dev.in -o requirements-combined.txt"
    )


# Run
@task
def run_backend(c):
    c.run("cd backend/yatodowa_api; flask run")


@task
def run(c):
    run_backend(c)
