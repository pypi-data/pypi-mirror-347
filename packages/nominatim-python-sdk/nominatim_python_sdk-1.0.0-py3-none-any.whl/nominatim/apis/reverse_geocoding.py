import jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from nominatim.api import NominatimApi
from nominatim.dtos.geocoder import ReverseGeocodingFilter

class ReverseGeocoding(NominatimApi):
    
    def reverse(self, options: ReverseGeocodingFilter):
        try:
            url = UrlUtil().make_url(self.base_url, ['reverse'])
            
            params = {}

            if options is not None:
                filter_params = {
                    field: value for field, 
                    value in vars(options).items() if value is not None
                }

                # Tratamento específico para o campo 'layer'
                if 'layer' in filter_params and isinstance(filter_params['layer'], list):
                    filter_params['layer'] = ",".join(filter_params['layer'])

                params = {**params, **filter_params}

            res = self.call_request(
                http_method=HTTPMethod.GET, 
                request_url=url, 
                params=params
            )

            return jsonpickle.decode(res)
        except:
            raise