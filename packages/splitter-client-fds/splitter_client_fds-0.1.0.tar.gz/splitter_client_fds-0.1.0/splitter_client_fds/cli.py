import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_command(cmd, name, install_url=None):
    try:
        subprocess.run([cmd, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        print(f"{name} is required. Please install it." + (f" See: {install_url}" if install_url else ""))
        return False

def copytree(src, dst, symlinks=False, ignore=None):
    # Recursively copy a directory tree
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def install_backend_deps(backend_dir):
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=backend_dir, check=True)

def install_frontend_deps(frontend_dir):
    subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)

def start_backend(backend_dir):
    subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"], cwd=backend_dir)

def start_frontend(frontend_dir):
    subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Splitter Client FDS CLI")
    parser.add_argument('--force', action='store_true', help='Overwrite existing backend/frontend folders during init')
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Copy backend and frontend to current directory and install dependencies")
    subparsers.add_parser("start-backend", help="Start backend server from ./backend")
    subparsers.add_parser("start-frontend", help="Start frontend server from ./frontend")

    args = parser.parse_args()
    cwd = os.getcwd()
    backend_dst = os.path.join(cwd, "backend")
    frontend_dst = os.path.join(cwd, "frontend")
    package_dir = Path(__file__).parent
    backend_src = package_dir / "backend"
    frontend_src = package_dir / "frontend"

    # Dependency checks
    if not check_command('python3', 'Python 3.8+'):
        sys.exit(1)
    if not check_command('pip', 'pip'):
        sys.exit(1)
    if not check_command('node', 'Node.js', 'https://nodejs.org/'):
        sys.exit(1)
    if not check_command('npm', 'npm', 'https://nodejs.org/'):
        sys.exit(1)

    if args.command == "init":
        # Backend
        if os.path.exists(backend_dst):
            if args.force:
                shutil.rmtree(backend_dst)
            else:
                resp = input("./backend already exists. Overwrite? [y/N]: ").strip().lower()
                if resp != 'y':
                    print("Skipping backend copy.")
                else:
                    shutil.rmtree(backend_dst)
        if not os.path.exists(backend_dst):
            print("Copying backend to ./backend ...")
            copytree(str(backend_src), backend_dst)
        # Frontend
        if os.path.exists(frontend_dst):
            if args.force:
                shutil.rmtree(frontend_dst)
            else:
                resp = input("./frontend already exists. Overwrite? [y/N]: ").strip().lower()
                if resp != 'y':
                    print("Skipping frontend copy.")
                else:
                    shutil.rmtree(frontend_dst)
        if not os.path.exists(frontend_dst):
            print("Copying frontend to ./frontend ...")
            copytree(str(frontend_src), frontend_dst)
        print("Installing backend dependencies ...")
        install_backend_deps(backend_dst)
        print("Installing frontend dependencies ...")
        install_frontend_deps(frontend_dst)
        print("Initialization complete. You can now use 'splitter-fds start-backend' and 'splitter-fds start-frontend'.")
    elif args.command == "start-backend":
        if not os.path.exists(backend_dst):
            print("./backend not found. Please run 'splitter-fds init' first.")
            sys.exit(1)
        print("Starting backend server from ./backend ... (Press Ctrl+C to stop)")
        start_backend(backend_dst)
        print("Backend server running at http://localhost:8000")
    elif args.command == "start-frontend":
        if not os.path.exists(frontend_dst):
            print("./frontend not found. Please run 'splitter-fds init' first.")
            sys.exit(1)
        print("Starting frontend server from ./frontend ... (Press Ctrl+C to stop)")
        start_frontend(frontend_dst)
        print("Frontend server running at http://localhost:3000")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()