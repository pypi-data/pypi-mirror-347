import os
from fmconsult.http.api import ApiBase

class NominatimApi(ApiBase):

  def __init__(self):
    try:
      self.app_name       = os.environ['nominatim.api.app.name']
      self.app_version    = os.environ['nominatim.api.app.version']
      self.email_address  = os.environ['nominatim.api.email.address']

      self.base_url = 'https://api-geocode.fmconsult.com.br'
      
      self.headers = {
        'User-Agent': f'{self.app_name}/{self.app_version} {self.email_address}'
      }
    except:
      raise