import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import List, Optional
from datetime import datetime
from schema import Message

messages_db: List[Message] = []
id_counter = 1

def get_messages() -> List[Message]:
    return messages_db

def get_message(id: int) -> Optional[Message]:
    return next((m for m in messages_db if m.id == id), None)

def create_message(name: str, topic: str) -> Message:
    global id_counter
    new_message = Message(
        id=id_counter,
        name=name,
        topic=topic,
        created_at=datetime.now().isoformat()
    )
    messages_db.append(new_message)
    id_counter += 1
    return new_message