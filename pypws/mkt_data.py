import datetime
import enum
import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from pypws.helpers import load_data


class CurveType(enum.Enum):
    DiscountCurve = "DiscountCurve"
    ForwardRatesCurve = "ForwardRatesCurve"
    SpotRatesCurve = "SpotRatesCurve"


@dataclass
class CurveNodes:
    tenor: str
    value: float


@dataclass
class Curve:
    currency: str
    curve_date: datetime
    nodes: typing.List[CurveNodes]
    curve_type: CurveType
    interpolation_type: str = None
    extrapolation_type: str = None


@dataclass
class DiscountCurve(Curve):
    curve_type = CurveType.DiscountCurve


@dataclass
class ForwardRatesCurve(Curve):
    curve_type = CurveType.ForwardRatesCurve


@dataclass
class SpotRatesCurve(Curve):
    curve_type = CurveType.SpotRatesCurve


@dataclass
class VolatilityPoint:
    maturity: str
    strike: float
    value: float


@dataclass
class SurfaceVolatilityPoint(VolatilityPoint):
    pass


@dataclass
class CubeVolatilityPoint(VolatilityPoint):
    tenor: str


@dataclass_json
@dataclass
class MarketData:
    market_date: datetime
    discount_curve: Curve
    forward_rates_curve: Curve
    spot_rates_curve: Curve
    volatility: typing.List[VolatilityPoint]


mkt_data = MarketData.from_dict(load_data('data/mkt_data.json'))

