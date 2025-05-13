from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class TextContent(object):
  text: str
  type: Optional[str] = 'text'

@dataclass
class SMSMessage(object):
  from_number: str
  to_number: str
  contents: List[TextContent]

  def to_dict(self):
    data = asdict(self)
    data['from'] = self.from_number
    data['to'] = self.to_number
    return data