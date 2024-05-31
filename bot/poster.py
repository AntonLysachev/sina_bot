import requests
import os
from dotenv import load_dotenv

load_dotenv()

POSTER_TOKEN = os.getenv('POSTER_TOKEN')
POSTER_URL = os.getenv('POSTER_URL')
PRODUCT_ID = int(os.getenv('PRODUCT_ID'))

def get_customer_by_id(poster_id) -> dict:
    response = requests.get(f'{POSTER_URL}/clients.getClient?format=json&token={POSTER_TOKEN}&client_id={poster_id}')
    return response.json()['response'][0]


def get_customer_by_phone(phone) -> dict:
    response = requests.get(f'{POSTER_URL}/clients.getClients?format=json&token={POSTER_TOKEN}&phone={phone}')
    if response.json()['response']:
        return response.json()['response'][0]
    else:
        response.json()['response']


def get_receipt(transaction_id) -> dict:

    response = requests.get(f'{POSTER_URL}/dash.getTransaction?format=json&token={POSTER_TOKEN}&transaction_id={transaction_id}')
    if response.json()['response']:
        return response.json()['response'][0]
    else:
        response.json()['response']


def get_product_in_receipt(transaction_id) -> dict:

    products = {}

    response = requests.get(f'{POSTER_URL}/dash.getTransactionProducts?format=json&token={POSTER_TOKEN}&transaction_id={transaction_id}')
    receipt = response.json()['response']

    for product in receipt:
        products[product['product_name']] = int(float(product['num']))

    return products


def update_customer_info(**kwargs) -> str:
    response = requests.post(f'{POSTER_URL}/clients.updateClient?token={POSTER_TOKEN}', data=kwargs)
    return response.json()['response']


def add_incoming_order(poster_id: int) -> None:
    requests.post(f'{POSTER_URL}/incomingOrders.createIncomingOrder?token={POSTER_TOKEN}', json={
        'spot_id': 1,
        'client_id': poster_id,
        'products': [
            {
                'product_id': PRODUCT_ID,
                'count': 1
            }]
    })
