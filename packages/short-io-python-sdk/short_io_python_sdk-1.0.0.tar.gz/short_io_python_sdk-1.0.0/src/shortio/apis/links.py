import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from shortio.api import ShorIOApi
from shortio.dtos.link import Link

class Links(ShorIOApi):

  def create(self, data: Link):
    logging.info(f'generating short link...')
    try:
      url = UrlUtil().make_url(self.base_url, ['links'])
      res = self.call_request(
        http_method=HTTPMethod.POST, 
        request_url=url, 
        payload=data.__dict__
      )
      return jsonpickle.decode(res)
    except:
      raise