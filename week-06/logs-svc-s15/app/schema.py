import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import strawberry
from typing import List, Optional

@strawberry.type
class Log:
    id: int
    name: str
    level: str
    created_at: str

@strawberry.type
class Query:
    @strawberry.field
    def logs(self) -> List[Log]:
        from resolvers import get_logs
        return get_logs()
    
    @strawberry.field
    def log(self, id: int) -> Optional[Log]:
        from resolvers import get_log
        return get_log(id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_log(self, name: str, level: str) -> Log:
        from resolvers import create_log
        return create_log(name, level)