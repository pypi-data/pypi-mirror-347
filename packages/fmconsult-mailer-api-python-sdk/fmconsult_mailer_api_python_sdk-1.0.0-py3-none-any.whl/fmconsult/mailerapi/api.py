import os
from fmconsult.http.api import ApiBase

class MailerApi(ApiBase):

  def __init__(self):
    try:
      self.api_token = os.environ['fmconsult.mailer.api.token']
      self.base_url = 'https://api-mailer.fmconsult.com.br'
      super().__init__()
    except:
      raise