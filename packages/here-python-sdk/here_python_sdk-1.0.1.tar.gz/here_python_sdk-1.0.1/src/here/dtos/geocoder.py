from dataclasses import dataclass
from typing import Optional

@dataclass
class ReverseGeocoderFilter(object):
  mode: str
  maxresults: int
  intersectionsnaptolerance: int
  addressattributes: str
  responseattributes: str
  locationattributes: str
  pageinformation: str
  addressrangesqueezefactor: int
  gen: int
  language: str
  app_id: Optional[str] = None
  app_code: Optional[str] = None

@dataclass
class Point(object):
  id: str
  latitude: str
  longitude: str