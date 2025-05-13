import os
from fmconsult.http.api import ApiBase

class ZenviaApi(ApiBase):

  def __init__(self):
    try:
      self.api_token = os.environ['zenvia.api.token']
      self.base_url = 'https://api.zenvia.com/v2'
      super().__init__()
    except:
      raise