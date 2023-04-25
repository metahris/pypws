import asyncio
import copy

from option import Priceable
from pricing_service import pricing_service


async def compute_delta(priceable: Priceable, batches=1, step_size=0.0001):
    # deep copying options objects
    options_copy_up = [copy.deepcopy(option) for option in priceable.options]
    options_copy_down = [copy.deepcopy(option) for option in priceable.options]
    # shift underlying price up/down
    for option in options_copy_up:
        option.underlying.price += option.underlying.price * step_size
    for option in options_copy_down:
        option.underlying.price -= option.underlying.price * step_size
    # create shifted up/down priceables
    priceable_up = copy.deepcopy(priceable)
    priceable_down = copy.deepcopy(priceable)
    priceable_up.options = options_copy_up
    priceable_down.options = options_copy_down
    # set batch size
    batch_size = int(len(priceable.options) / batches)
    print(batch_size)
    # price shifted up/down options
    results_up, results_down = await asyncio.gather(
        pricing_service.price(priceable=priceable_up, batch_size=batch_size),
        pricing_service.price(priceable=priceable_down, batch_size=batch_size))
    # calculate delta for each option
    for option, option_up, option_down in zip(priceable.options, results_up, results_down):
        option.delta = (option_up.price - option_down.price) / (2 * option.underlying.price * step_size)
    return priceable.options
