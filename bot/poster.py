import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

POSTER_TOKEN = os.getenv('POSTER_TOKEN')
POSTER_URL = os.getenv('POSTER_URL')
PRODUCT_ID = int(os.getenv('PRODUCT_ID'))


class API():

    def __init__(self, token=POSTER_TOKEN, base_url=POSTER_URL) -> None:
        self._token = token
        self._base_url = base_url

    def get_url(self, rpc_method) -> str:
        return f'{self._base_url}{rpc_method}?token={self._token}'

    async def get_json_request(self, rpc_method: str, quantity='one', **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with await session.get(self.get_url(rpc_method), params=kwargs) as response:
                json_response = await response.json()
                if json_response['response']:
                    if quantity == 'one':
                        return json_response['response'][0]
                    if quantity == 'many':
                        return json_response['response']

    async def post_json_request(self, rpc_method: str, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.get_url(rpc_method), json=kwargs) as response:
                json_response = await response.json()
                return json_response['response']

    async def get_customer_by_id(self, poster_id: int) -> dict:
        return await self.get_json_request("clients.getClient", client_id=poster_id)

    async def get_customer_by_phone(self, phone: str) -> dict:
        return await self.get_json_request("clients.getClients", phone=phone)

    async def get_receipt(self, transaction_id: str) -> dict:
        return await self.get_json_request("dash.getTransaction", transaction_id=transaction_id)

    async def get_products_in_receipt(self, transaction_id: str) -> list:
        receipt = await self.get_json_request("dash.getTransactionProducts", quantity='many', transaction_id=transaction_id)
        products = {}
        for product in receipt:
            products[product['product_name']] = product['num'].split('.')[0]
        return products

    async def update_customer_info(self, **kwargs) -> str:
        return await self.post_json_request("clients.updateClient", **kwargs)

    async def add_incoming_order(self, poster_id: int) -> None:
        kwargs = {'spot_id': 1,
                  'client_id': poster_id,
                  'products': [{
                      'product_id': PRODUCT_ID,
                      'count': 1
                  }]}
        return await self.post_json_request("incomingOrders.createIncomingOrder", **kwargs)
