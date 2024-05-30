import requests
import os
from dotenv import load_dotenv

load_dotenv()

POSTER_TOKEN = os.getenv('POSTER_TOKEN')
POSTER_URL = os.getenv('POSTER_URL')
PROMOTION_ID = int(os.getenv('PROMOTION_ID'))

def to_present(poster_id):

    count = 0
    present_info = {
        'to_cup': 0,
        'cups': 0
    }

    client = get_customer_by_id(poster_id)
    accumulation_products = client['accumulation_products']
    prize_products = client['prize_products']

    present_info['cups'] = len(prize_products)

    if accumulation_products:
        for group in accumulation_products.values():
            if group['promotion_id'] == PROMOTION_ID:
                for cup in group['products']:
                    count += cup['count']

    present_info['to_cup'] = 4 - count

    return present_info


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
