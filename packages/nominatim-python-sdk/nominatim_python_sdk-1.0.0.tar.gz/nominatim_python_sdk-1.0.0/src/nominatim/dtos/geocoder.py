from dataclasses import dataclass
from typing import Optional, Literal, List

@dataclass
class ReverseGeocodingFilter(object):
    lat: float
    lon: float
    format: Literal['xml', 'json', 'jsonv2', 'geojson', 'geocodejson'] = 'xml'
    addressdetails: int = 1
    extratags: int = 0
    namedetails: int = 1
    zoom: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] = 18
    polygon_geojson: int = 0
    polygon_kml: int = 0
    polygon_svg: int = 0
    polygon_text: int = 0
    polygon_threshold: float = 0.0
    layer: Optional[List[Literal['address', 'poi', 'railway', 'natural', 'manmade']]] = None