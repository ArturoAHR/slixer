from invoke import task


@task
def build(c):
    c.run("pyinstaller --onefile --name slixer.exe main.py")


@task
def test(c):
    c.run("pytest")


@task
def lint(c):
    c.run("flake8")
