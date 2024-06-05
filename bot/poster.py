import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

POSTER_TOKEN = os.getenv('POSTER_TOKEN')
POSTER_URL = os.getenv('POSTER_URL')
PRODUCT_ID = int(os.getenv('PRODUCT_ID'))


async def get_customer_by_id(poster_id) -> dict:
    async with aiohttp.ClientSession() as session:
        async with await session.get(f'{POSTER_URL}/clients.getClient?format=json&token={POSTER_TOKEN}&client_id={poster_id}') as response:
            json_response = await response.json()
            return json_response['response'][0]


async def get_customer_by_phone(phone) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{POSTER_URL}/clients.getClients?format=json&token={POSTER_TOKEN}&phone={phone}') as response:
            json_response = await response.json()
            if json_response['response']:
                return json_response['response'][0]

        

async def get_receipt(transaction_id) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{POSTER_URL}/dash.getTransaction?format=json&token={POSTER_TOKEN}&transaction_id={transaction_id}') as response:
            json_response = await response.json()
            if json_response['response']:
                return json_response['response'][0]



async def get_product_in_receipt(transaction_id) -> list:
    products = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{POSTER_URL}/dash.getTransactionProducts?format=json&token={POSTER_TOKEN}&transaction_id={transaction_id}') as response:
            json_response = await response.json()
            receipt = json_response['response']
            for product in receipt:
                products[product['product_name']] = int(float(product['num']))
            return products


async def update_customer_info(**kwargs) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{POSTER_URL}/clients.updateClient?token={POSTER_TOKEN}', data=kwargs) as response:
            json_response = await response.json()
            return json_response['response']


async def add_incoming_order(poster_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{POSTER_URL}/incomingOrders.createIncomingOrder?token={POSTER_TOKEN}', json={
                'spot_id': 1,
                'client_id': poster_id,
                'products': [
                    {
                        'product_id': PRODUCT_ID,
                        'count': 1
                    }]
            }) as response:
            pass
