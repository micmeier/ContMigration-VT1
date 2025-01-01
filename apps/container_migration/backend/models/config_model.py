from pydantic import BaseModel
from typing import List, Optional

class RuleConfig(BaseModel):
    rule: str
    cluster: str
    action: str
    targetCluster: Optional[str] = None
    forensic_analysis: Optional[bool] = False
    AI_suggestion: Optional[bool] = False

class Config(BaseModel):
    config: List[RuleConfig]