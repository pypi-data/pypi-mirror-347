import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from zenvia.api import ZenviaApi
from zenvia.dtos.sms import SMSMessage

class SMSChannel(ZenviaApi):

  def send_text_message(self, data: SMSMessage):
    logging.info(f'sending SMS text message...')
    try:
      url = UrlUtil().make_url(self.base_url, ['channels', 'sms', 'messages'])
      res = self.call_request(
        http_method=HTTPMethod.POST, 
        request_url=url, 
        payload=data.to_dict()
      )
      res = jsonpickle.decode(res)
      if 'id' in res:
          return res
      else:
          raise Exception(res['message'])
    except:
      raise