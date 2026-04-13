import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import strawberry
from typing import List, Optional
from datetime import datetime

@strawberry.type
class Message:
    id: int
    name: str
    topic: str
    created_at: str

@strawberry.type
class Query:
    @strawberry.field
    def messages(self) -> List[Message]:
        from resolvers import get_messages
        return get_messages()
    
    @strawberry.field
    def message(self, id: int) -> Optional[Message]:
        from resolvers import get_message
        return get_message(id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_message(self, name: str, topic: str) -> Message:
        from resolvers import create_message
        return create_message(name, topic)