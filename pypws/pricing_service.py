import asyncio

from base_api import BaseAPI
from config import config
from option import Priceable


class OptionPricingService(BaseAPI):
    def __init__(self, env='prod'):
        super().__init__(config=config.pricing_service, env=env)
        self._set_resource_url('pricing')

    async def price(self, priceable: Priceable, batches_nbr: int = 1, endpoint=''):
        '''
        :param priceable: Priceable object
        :param batches_nbr: number of batches containing all priceable options
        :param endpoint: the pricing endpoint for the specified option
        :return: list of priced options
        '''
        if not priceable.options:
            return []
        if not batches_nbr >= 1:
            raise Exception('number of batches must be at least 1')
        batch_size = int(len(priceable.options) / batches_nbr)
        batches = [priceable.options[i:i + batch_size] for i in range(0, len(priceable.options), batch_size)]
        async with self._client_session() as session:
            tasks = []
            for batch in batches:
                task = asyncio.create_task(self._post_async(session=session, endpoint=endpoint, json={
                    'options': batch,
                    'data': priceable.market_data.to_dict()
                }))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            return results


pricing_service = OptionPricingService()
