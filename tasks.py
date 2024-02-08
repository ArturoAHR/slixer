from invoke import task

@task
def compile(c):
  c.run("pyinstaller --onefile main.py")
  
@task
def install(c):
  c.run("pipenv install --dev")