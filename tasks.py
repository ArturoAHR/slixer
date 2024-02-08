from invoke import task

@task
def compile(c):
  c.run("pyinstaller --onefile main.py")