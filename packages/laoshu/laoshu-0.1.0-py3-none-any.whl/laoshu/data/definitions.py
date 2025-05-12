from typing import List
from pydantic import BaseModel


class PromptCluster(BaseModel):
    cluster_id: int
    description: str
    session_ids: List[str]
