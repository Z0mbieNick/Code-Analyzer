

# Code Analyzer

This is the Repository where i develope the code analyzer for detecting Zero Division Errors and other Security Holes

# Installation Guide

1. Clone the repository using git.
2. Install the required packages using [command].
3. Create a DB-File called `src/wbgym,.db`.
4. Run the script `main.py` to start the server.

# Deployment Guide locally

- Pull the latest commits from the repository.
- Make the following changes to `main.py`:
  - Set debug to False
  - Set host to '0.0.0.0'

And run the `main.py`-file!


# Server deployment Guide

  - create the virtual enviorment
    - python -m venv /path/to/new/virtual/environment

  - Create a file
    - sudo nano /etc/systemd/system/Code-Analyzer.service

  - paste this and if necessary, adjust the paths accordingly:
  
  [Unit]
  Description=Flask App: Code-Analyzer
  After=network.target

  [Service]
  User=Code-Analyzer
  Group=Code-Analyzer
  WorkingDirectory=/home/Code-Analyzer/Code-Analyzer/Code-Analyzer/src
  ExecStart=/home/Code-Analyzer/Code-Analyzer/venv/bin/python3 main.py
  Restart=always
  Environment="FLASK_ENV=production"
  Environment="PYTHONUNBUFFERED=1"

  [Install]
  WantedBy=multi-user.target

  - Reload systemd and enable the service
    - sudo systemctl daemon-reexec
    - sudo systemctl daemon-reload
    - sudo systemctl enable Code-Analyzer.service

  - start the service
    - sudo systemctl start Code-Analyzer.service

  - Check logs
    - journalctl -u Code-Analyzer.service -e
  
