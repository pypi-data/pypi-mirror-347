import json, logging, jsonpickle
from enum import Enum
from http import HTTPMethod
from fmconsult.utils.cast import JSONCastUtil
from fmconsult.utils.url import UrlUtil
from fmconsult.mailerapi.api import MailerApi
from fmconsult.mailerapi.dtos.email import EmailTemplate

class EmailChannel(MailerApi):

  def send_mail(self, data: EmailTemplate):
    try:
      logging.info(f'serializing data to JSON to get Enum values...')
      data = json.dumps(data.to_dict(), default=JSONCastUtil().serialize_enum)
      
      logging.info(f'deserializing data from JSON...')
      data = json.loads(data)

      logging.info(f'sending e-mail...')
      url = UrlUtil().make_url(self.base_url, ['email', 'send'])
      res = self.call_request(
        http_method=HTTPMethod.POST, 
        request_url=url, 
        payload=data
      )
      return jsonpickle.decode(res)
    except:
      raise