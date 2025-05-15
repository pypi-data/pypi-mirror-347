import json,logging,requests,hmac
from .error import ClientError, ServerError
from .utils import cleanNoneValue,get_timestamp

from hashlib import sha256





class ApiClient(object):
    

    def __init__(self,api_key=None,secret_key=None,base_url=None,timeout=None,proxies=None):
        
        
        self._api_key = api_key
        self._secret_key = secret_key
        self._base_url = base_url 
        self._timeout = timeout
        headers={}
        headers["User-Agent"]      = "Bingx Python Sdk"
        headers["Content-Type"]    = "*/*"
        
        if api_key:  
            headers["X-BX-APIKEY"] = api_key
        
        
        if not isinstance(proxies, dict): proxies = None

        
        
        self._session = requests.Session()

        self._session.headers.update(headers)

        self._session.proxies=proxies
        
        
        

        self._logger = logging.getLogger(__name__)
       


   

    def send_request(self,http_method:str, url_path:str, payload:dict=None):
        if not payload:payload = {}
        
        payload=cleanNoneValue(payload)

        sorted_params = sorted(payload)
        
        params_str = "&".join(["%s=%s" % (x, payload[x]) for x in sorted_params]) 
        
        params_str =f"{params_str}&timestamp={get_timestamp()}" if params_str  else f"timestamp={get_timestamp()}"
        
        signature   = hmac.new(self._secret_key.encode("utf-8"), params_str.encode("utf-8"), digestmod=sha256).hexdigest() if self._secret_key else ""
        
        url = "%s%s?%s&signature=%s" % (self._base_url, url_path, params_str,signature ) if signature else "%s%s?%s" % (self._base_url, url_path, params_str)
        
        self._logger.debug("url: " + url)

        
        response = self._session.request(method=http_method,url=url,timeout=self._timeout)
        self._logger.debug("raw response from server:" + response.text)
        self._handle_exception(response)

        
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            result=response.content
        

        return result

    
    
        
    
    def _handle_exception(self, response:requests.Response):
        status_code = response.status_code
        
        
        
        try:
            result_json = json.loads(response.text)
        except json.JSONDecodeError:
            result_json=None
        
        
        
        
        if status_code == 200:
            if result_json: 
                if "code" in result_json and result_json["code"] != 0:
                    raise ClientError(status_code, result_json["code"], result_json["msg"], response.headers, result_json)
            

        
        else:
            
            
            raise ServerError(status_code, response.text)  
            
