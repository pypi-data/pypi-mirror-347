import os
from fmconsult.http.api import ApiBase

class GetrakMiddlewareApi(ApiBase):

  def __init__(self):
    try:
      self.api_token = os.environ['getrak.middleware.api.token']
      self.api_client_id = os.environ['getrak.middleware.api.client_id']
      self.base_url = 'https://api-getrak-middleware.fmconsult.com.br'
      super().__init__({'x-client-id': self.api_client_id})
    except:
      raise