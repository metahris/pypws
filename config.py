import typing
from dataclasses import dataclass
from os.path import dirname, abspath, join

from dataclasses_json import dataclass_json

from pypws.helpers import load_data

file_path = dirname(abspath(__file__))


@dataclass
class Env:
    token_url: str
    client_id: str
    client_secret: str
    grant_type: str
    scope: typing.List[str]
    token: str


@dataclass
class PricingService:
    base_url: str
    authentication: str
    uat: Env
    prod: Env


@dataclass_json
@dataclass
class Config:
    pricing_service: PricingService


config_json_path = join(file_path, 'config.json')
config = Config.from_dict(load_data(config_json_path))
