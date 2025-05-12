# Splitter Client FDS

A pip-installable package to launch a modern federated/split learning lab portal with a Next.js frontend and FastAPI backend. Designed for non-technical users, with a clean dashboard UI and easy setup.

## Features
- Modern dashboard UI (Next.js, Tailwind CSS, shadcn/ui)
- Upload CSV or zip of images for split learning simulation
- FastAPI backend for ML simulation
- One-line install and launch
- Clear instructions and notifications

## Requirements
- Python 3.8+
- Node.js and npm (https://nodejs.org/)

## Installation
```bash
pip install splitter-client-fds
```

## Usage
### 1. Initialize project in your working directory
```bash
splitter-fds init
```
- This copies the backend and frontend folders to your current directory and installs all dependencies.
- Use `--force` to overwrite existing backend/frontend folders without prompting.

### 2. Start the backend server
```bash
splitter-fds start-backend
```
- Runs FastAPI backend from ./backend (http://localhost:8000)

### 3. Start the frontend server
```bash
splitter-fds start-frontend
```
- Runs Next.js frontend from ./frontend (http://localhost:3000)

## Troubleshooting
- If you see errors about missing Node.js/npm, install them from https://nodejs.org/
- If you see Python version errors, use Python 3.8 or higher.
- For other issues, try re-running `splitter-fds init --force`.

## Project Structure
- `backend/`: FastAPI backend
- `frontend/`: Next.js frontend
- `splitter_client_fds/cli.py`: CLI entry point

## About
Splitter is a modern, user-friendly portal for split/federated learning labs.
