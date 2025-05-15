import logging, jsonpickle
from typing import List
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from fmconsult.http.api import ContentType
from here.api import HereApi
from here.dtos.geocoder import ReverseGeocoderFilter, Point

class ReverseGeocoder(HereApi):

  def get_multi_reverse_geocode(self, filters:ReverseGeocoderFilter, points:List[Point]):
    try:
      url = UrlUtil().make_url(self.base_url, ['6.2', 'multi-reversegeocode.json'])
    
      params = {
        'app_id': self.app_id,
        'app_code': self.app_code
      }
      
      if filters is not None:
        filter_params = {field: value for field, value in vars(filters).items() if value is not None}
        params = {**params, **filter_params}

      payload = "\n".join([f'id={point.id}&prox={point.latitude},{point.longitude},80' for point in points])

      res = self.call_request(
        http_method=HTTPMethod.POST, 
        request_url=url, 
        params=params, 
        payload=payload,
        content_type=ContentType.TEXT_PLAIN
      )
      return jsonpickle.decode(res)
    except:
      raise