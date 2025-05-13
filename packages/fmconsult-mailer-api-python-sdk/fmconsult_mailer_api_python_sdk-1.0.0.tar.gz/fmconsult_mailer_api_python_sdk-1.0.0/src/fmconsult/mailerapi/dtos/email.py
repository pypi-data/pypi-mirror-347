from dataclasses import dataclass, asdict
from typing import Dict, List, Union, Optional
from fmconsult.utils.enum import CustomEnum

class DataType(CustomEnum):
  STRING = "string"
  DOUBLE = "double"
  INT = "integer"
  PHONE_NUMBER = "phone-number"

@dataclass
class DataField(object):
  field: str
  type: DataType
  value: Union[str, int, float]

class AttachmentType(CustomEnum):
  URL = "url"
  BASE64 = "base64"

@dataclass
class Attachment(object):
  type: AttachmentType
  value: str
  filename: Optional[str] = None

@dataclass
class EmailTemplate(object):
  template: str
  emails: List[str]
  subject: str
  data: List[DataField]
  attachments: Optional[List[Attachment]] = None

  def to_dict(self):
    data = asdict(self)
    data['emails'] = ','.join(self.emails)
    return data