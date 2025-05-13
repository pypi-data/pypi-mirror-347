import os
from fmconsult.http.api import ApiBase

class ShorIOApi(ApiBase):

  def __init__(self):
    try:
      self.api_key = os.environ['short.io.api.key']
      self.base_url = 'https://api.short.io'
      self.headers = {
        'Authorization': self.api_key
      }
    except:
      raise