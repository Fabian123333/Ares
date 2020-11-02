from typing import Optional
from datetime import datetime

def write(text: str, level: Optional[str] = "INFO"):
	print("["+str(datetime.now())+"] " + text)