import os
import sys
from pyvenDF.server import start_server

def create_project(name):
    os.makedirs(f"{name}/pyven_app", exist_ok=True)
    os.makedirs(f"{name}/static", exist_ok=True)
    os.makedirs(f"{name}/templates", exist_ok=True)

    with open(f"{name}/pyven_app/views.py", "w") as f:
        f.write("# Define your views here\n")

    with open(f"{name}/pyven_app/routes.py", "w") as f:
        f.write("# Define your routes here\n")

    with open(f"{name}/main.py", "w") as f:
        f.write("from pyven import run_server\nrun_server()\n")

    print(f"✅ Project '{name}' created.")

def main():
    if len(sys.argv) < 2:
        print("Usage: pyven [create|runserver]")
        return

    cmd = sys.argv[1]
    if cmd == "create":
        if len(sys.argv) < 3:
            print("Usage: pyven create <project_name>")
        else:
            create_project(sys.argv[2])
    elif cmd == "runserver":
        start_server()
