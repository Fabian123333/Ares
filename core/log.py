from typing import Optional
from datetime import datetime

buffer = ""

def write(text: str, level: Optional[str] = "INFO"):
	line = "["+str(datetime.now())+"] " + text
	buffer = line
	print(line)

def clearBuffer():
	buffer = ""

def getBuffer():
	return buffer