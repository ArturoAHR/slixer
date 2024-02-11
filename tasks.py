from invoke import task


@task
def build(c):
    c.run("pyinstaller --onefile --name slixer.exe main.py")


@task
def test(c):
    c.run("pytest")


@task(optional=["fix"])
def lint(c, fix=False):
    if fix:
        c.run("black .")
    else:
        c.run("flake8")
