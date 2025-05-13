from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Link(object):
  domain: str
  originalURL: str
  title: Optional[str] = None
  expiresAt: Optional[int] = None
  expiredURL: Optional[str] = None
  tags: Optional[List[str]] = None
  password: Optional[str] = None
  ttl: Optional[int] = None
  utmSource: Optional[str] = None
  utmMedium: Optional[str] = None
  utmCampaign: Optional[str] = None
  utmTerm: Optional[str] = None
  utmContent: Optional[str] = None