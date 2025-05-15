import os
from fmconsult.http.api import ApiBase

class HereApi(ApiBase):

  def __init__(self):
    try:
      self.app_id = os.environ['here.api.app.id']
      self.app_code = os.environ['here.api.app.code']
      self.base_url = 'https://reverse.geocoder.api.here.com'
      self.headers = {}
    except:
      raise