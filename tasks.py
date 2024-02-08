from invoke import task

@task
def build(c):
  c.run("pyinstaller --onefile --name slixer.exe main.py")
  
@task
def install(c):
  c.run("pipenv install --dev")
  
@task
def test(c):
  c.run("pytest")