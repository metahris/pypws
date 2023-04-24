import datetime
import enum
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from option import Option, Underlying


class SwaptionType(enum.Enum):
    Payer = 'Payer'
    Receiver = 'Receiver'


class SettlementType(enum.Enum):
    Cash = 'Cash'
    Physical = 'Physical'


@dataclass
class IRSwap(Underlying):
    fixed_rate: float
    floating_rate_reference: str
    floating_rate_spread: float
    payment_frequency_months: int
    currency: str
    day_count_convention: str
    start_date: datetime
    end_date: datetime
    notional: float
    valuation_date: datetime


@dataclass_json
@dataclass
class Swaption(Option):
    option_type: SwaptionType
    settlement_type: SettlementType
    underlying: IRSwap
