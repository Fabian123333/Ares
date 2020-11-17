# Ares
Ares Backup Utility

Ares is a scalable backup solution for containers, linux hosts and files, offering a large API for automated deployment.

# Installation

## Prerequirments:
 MongoDB Server

 The following packages (for Debian):
 
 `apt install python3-pip rustc libffi-dev`

For the Ares-Controller:
 `pip3 install fastapi uvicorn pymongo`
 
For the Ares-Worker(s):
 `pip3 install pymongo fs.smbfs paramiko`
 

Afterwards enter the connection string of your mongoDB server to the config.py

# Start

Controller:
 `uvicorn api:app --host 0.0.0.0 --workers 8`

You can access the API afterwards at http://localhost:8000/docs
 
Worker:
 `python3 main.py`

The worker and controller nodes need access to the mongodb database
