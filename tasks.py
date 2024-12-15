from invoke import task

@task
def start(ctx):
    ctx.run("python __init__.py")

# @task
# def test(ctx):
#     ctx.run("pytest tests/")
#
# @task
# def lint(ctx):
#     ctx.run("flake8 app/")
