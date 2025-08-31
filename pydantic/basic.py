from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    tags: List[str] = []

# Valid input
user = User(id="1", name="Alice", age="30", tags=["admin", "tester"])
print(user)
# -> id=1 name='Alice' age=30 tags=['admin', 'tester']

# Invalid input
try:
    User(id="abc", name=123)
except Exception as e:
    print(e)
