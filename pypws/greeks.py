import asyncio
import copy

from option import Priceable
from pricing_service import pricing_service


def _shift_underlying_price(priceable: Priceable, direction='up', step_size=0.0001):
    """

    :param priceable: object of type Priceable
    :param direction: up or down
    :param step_size: small step
    :return:
    """
    # deep copy priceable object
    priceable_shift = copy.deepcopy(priceable)
    # shift underlying price up/down
    if direction == 'up':
        for option in priceable_shift.options:
            option.underlying.price += option.underlying.price * step_size
    elif direction == 'down':
        for option in priceable_shift.options:
            option.underlying.price -= option.underlying.price * step_size
    else:
        raise Exception('direction must be up or down')
    return priceable_shift


async def compute_delta(priceable: Priceable, batches_nbr=1, step_size=0.0001):
    priceable_up = _shift_underlying_price(priceable=priceable, direction='up', step_size=step_size)
    priceable_down = _shift_underlying_price(priceable=priceable, direction='down', step_size=step_size)
    # price shifted up/down options
    results_up, results_down = await asyncio.gather(
        pricing_service.price(priceable=priceable_up, batches_nbr=batches_nbr),
        pricing_service.price(priceable=priceable_down, batches_nbr=batches_nbr))
    # calculate delta for each option
    for option, option_up, option_down in zip(priceable.options, results_up, results_down):
        option.delta = (option_up.price - option_down.price) / (2 * option.underlying.price * step_size)
    return priceable.options


async def compute_gamma(priceable: Priceable, batches_nbr=1, step_size=0.0001):
    priceable_up = _shift_underlying_price(priceable=priceable, direction='up', step_size=step_size)
    priceable_down = _shift_underlying_price(priceable=priceable, direction='down', step_size=step_size)
    # price shifted up/down options
    result, results_up, results_down = await asyncio.gather(
        pricing_service.price(priceable=priceable, batches_nbr=batches_nbr),
        pricing_service.price(priceable=priceable_up, batches_nbr=batches_nbr),
        pricing_service.price(priceable=priceable_down, batches_nbr=batches_nbr))
    # calculate gamma for each option
    for option, option_up, option_down in zip(result, results_up, results_down):
        option.delta = (option_up.price - 2 * option.price + option_down.price) / (
                2 * option.price * step_size)
    return result
