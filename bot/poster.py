import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

POSTER_TOKEN = os.getenv('POSTER_TOKEN')
POSTER_URL = os.getenv('POSTER_URL')
PRODUCT_ID = int(os.getenv('PRODUCT_ID'))


async def get_json_request(rpc_method: str, quantity='one', **kwargs) -> dict:
    async with aiohttp.ClientSession() as session:
        async with await session.get(f'{POSTER_URL}{rpc_method}?token={POSTER_TOKEN}', params=kwargs) as response:
            json_response = await response.json()
            if json_response['response']:
                if quantity == 'one':
                    return json_response['response'][0]
                if quantity == 'many':
                    return json_response['response']
                
                
async def post_json_request(rpc_method: str, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{POSTER_URL}{rpc_method}?token={POSTER_TOKEN}', json=kwargs) as response:
            json_response = await response.json()
            return json_response['response']


async def get_customer_by_id(poster_id) -> dict:
    return await get_json_request("clients.getClient", client_id=poster_id)


async def get_customer_by_phone(phone) -> dict:
    return await get_json_request("clients.getClients", phone=phone)


async def get_receipt(transaction_id) -> dict:
    return await get_json_request("dash.getTransaction", transaction_id=transaction_id)


async def get_product_in_receipt(transaction_id) -> list:
    receipt = await get_json_request("dash.getTransactionProducts", quantity='many', transaction_id=transaction_id)
    products = {}
    for product in receipt:
        products[product['product_name']] = product['num'].split('.')[0]
    return products


async def update_customer_info(**kwargs) -> str:
    return await post_json_request("clients.updateClient", **kwargs)


async def add_incoming_order(poster_id: int) -> None:
    kwargs = {'spot_id': 1,
              'client_id': poster_id,
              'products': [{
                  'product_id': PRODUCT_ID,
                  'count': 1
                  }]}
    return await post_json_request("incomingOrders.createIncomingOrder", **kwargs)
