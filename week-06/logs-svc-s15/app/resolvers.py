import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import List, Optional
from datetime import datetime
from schema import Log

logs_db: List[Log] = []
id_counter = 1

def get_logs() -> List[Log]:
    return logs_db

def get_log(id: int) -> Optional[Log]:
    return next((l for l in logs_db if l.id == id), None)

def create_log(name: str, level: str) -> Log:
    global id_counter
    new_log = Log(
        id=id_counter,
        name=name,
        level=level,
        created_at=datetime.now().isoformat()
    )
    logs_db.append(new_log)
    id_counter += 1
    return new_log