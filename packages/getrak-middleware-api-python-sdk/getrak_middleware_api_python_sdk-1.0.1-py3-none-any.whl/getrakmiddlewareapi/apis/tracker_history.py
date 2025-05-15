import logging, jsonpickle
from fmconsult.utils.url import UrlUtil
from fmconsult.exceptions.not_found_exception import NotFoundException
from getrakmiddlewareapi.api import GetrakMiddlewareApi

class TrackerHistory(GetrakMiddlewareApi):

  def get_vehicle_tracker_history(self, getrak_ids:str=None, start_date:str=None, end_date:str=None):
    try:
      logging.info(f'get_vehicle_tracker_history tracker history records...')
      
      params = {}

      if start_date:
        params['start_date'] = start_date
        
      if end_date:
        params['end_date'] = end_date
        
      if getrak_ids:
        if isinstance(getrak_ids, list):
            params['getrak_ids'] = ','.join(map(str, getrak_ids))
        else:
            params['getrak_ids'] = getrak_ids
        
      url = UrlUtil().make_url(self.base_url, ['vehicle', 'tracker-history'])
      res = self.call_request('GET', url, params=params)
      return jsonpickle.decode(res)
    except NotFoundException as e:
      raise e
    except Exception as e:
      raise e