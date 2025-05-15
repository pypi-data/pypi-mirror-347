import logging, jsonpickle
from fmconsult.utils.url import UrlUtil
from getrakmiddlewareapi.api import GetrakMiddlewareApi

class Vehicles(GetrakMiddlewareApi):

  def get_all(self, getrak_ids:str=None):
    try:
      logging.info(f'get all vehicles records...')
      
      params = {}

      if getrak_ids:
        params['getrak_ids'] = getrak_ids
        
      url = UrlUtil().make_url(self.base_url, ['vehicles'])
      res = self.call_request('GET', url, params=params)
      return jsonpickle.decode(res)
    except Exception as e:
      error = jsonpickle.decode(str(e))
      raise error['message']

  def get_by_id(self, id_veiculo):
    try:
      logging.info(f'get vehicle record from id {id_veiculo}...')
      url = UrlUtil().make_url(self.base_url, ['vehicle', id_veiculo])
      res = self.call_request('GET', url)
      return jsonpickle.decode(res)
    except Exception as e:
      error = jsonpickle.decode(str(e))
      raise error['message']