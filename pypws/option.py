import datetime
import enum
import typing
from abc import ABCMeta
from dataclasses import dataclass

from pypws.mkt_data import MarketData


class PricingModel(enum.Enum):
    BS = 'BlackScholes'
    BSM = 'BlackScholesMerton'
    Sabr = 'Sabr'
    Hjm = 'Hjm'
    Heston = 'Heston'


class OptionType(enum.Enum):
    Call = "Call"
    Put = 'Put'


class ExerciseStyle(enum.Enum):
    American = "American"
    European = "European"
    Bermudan = "Bermudan"


@dataclass
class Underlying(metaclass=ABCMeta):
    pass


@dataclass
class Option(metaclass=ABCMeta):
    option_type: OptionType
    exercise_style: ExerciseStyle
    pricing_model: PricingModel
    valuation_date: datetime
    effective_date: datetime
    expiration_date: datetime
    underlying: Underlying
    price: typing.Optional[float]
    delta: typing.Optional[float]
    gamma: typing.Optional[float]
    vega: typing.Optional[float]
    theta: typing.Optional[float]
    rho: typing.Optional[float]


@dataclass
class Priceable:
    options: typing.List[Option]
    market_data: MarketData



