from dataclasses import dataclass

from dataclasses_json import dataclass_json

from pypws.helpers import load_data


@dataclass
class Env:
    token_url: str
    client_id: str
    client_secret: str
    grant_type: str
    scope: str
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


config = Config.from_dict(load_data('config.json'))

print(config)
