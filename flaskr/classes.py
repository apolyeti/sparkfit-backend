from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SparkFitImage:
    predicted_classes: List[str]
    file_name: str
    data: str
    fabric: Optional[str]
    color: Optional[str]
    fit: Optional[str]
