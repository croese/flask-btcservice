import requests

class Wallet:
    def __init__(self, address, num_tx, received, sent, balance, sub_wallets=None):
        self.address = address
        self.num_tx = num_tx
        self.total_received = received
        self.total_sent = sent
        self.final_balance = balance
        self.sub_wallets = sub_wallets

    def __str__(self):
        return self.address

class RequestsHttpClient:
    def get(self, address, params=None):
        return requests.get(address, params=params)

class MockHttpClient:
    def __init__(self, response):
        self.response = response

    def get(self, address, params=None):
        return self.response

class BadResponse:
    def __init__(self, ex):
        self.ex = ex

    def raise_for_status(self):
        raise ex

class BlockchainInfoClient:
    def __init__(self, http_client):
        self.http_client = http_client

    def get_single_address(self, address):
        url = 'https://blockchain.info/rawaddr/' + address
        resp = self.http_client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return Wallet(data['address'], data['n_tx'],
            data['total_received'], data['total_sent'],
            data['final_balance'])

    def get_multi_address(self, addresses, wallet_name='wallet'):
        resp = self.http_client.get('https://blockchain.info/multiaddr',
            params={'active': "|".join(addresses)})
        resp.raise_for_status()
        data = resp.json()
        wallet = data['wallet']
        sub_wallets = list(map(lambda a: Wallet(a['address'], a['n_tx'],
            a['total_received'], a['total_sent'],
            a['final_balance']), data['addresses']))
        return Wallet(wallet_name, wallet['n_tx'],
            wallet['total_received'], wallet['total_sent'],
            wallet['final_balance'], sub_wallets)

    def get_exchange_rate(self, currency_code='USD'):
        resp = self.http_client.get('https://blockchain.info/ticker')
        resp.raise_for_status()
        data = resp.json()
        return data[currency_code]['last']

if __name__ == '__main__':
    wallets = [
        "115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn",
        "12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw",
        "13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94"
    ]

    c = BlockchainInfoClient(RequestsHttpClient())
    print(c.get_single_address(wallets[0]))
    print(c.get_multi_address(wallets))
    print(c.get_exchange_rate())



# single response
# {
# 	"response_type": "in_channel",
#     "text": "Address: `115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn`",
#     "attachments": [
#         {
# 			"fields": [
# 				{
# 					"title": "Transaction Count",
# 					"value": 86,
# 					"short": true
# 				},
# 				{
# 					"title": "Total Received",
# 					"value": "116.16871770 BTC",
# 					"short": true
# 				},
# 				{
# 					"title": "Total Sent",
# 					"value": "116.16871770 BTC",
# 					"short": true
# 				},
# 				{
# 					"title": "Balance",
# 					"value": "0 BTC",
# 					"short": true
# 				}
# 			]
#         }
#     ]
# }


# multi response
# {
#     "response_type": "in_channel",
#     "text": "Wallet: `WannaCry`\nTransactions: 292\nReceived: 48.42961826 BTC\nSent: 116.16871770 BTC\nBalance: 0 BTC\nUSD: $1.00",
#     "attachments": [
#         {
# 			"text": "Address: 13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94",
# 			"fallback": "Address: 13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94",
#             "fields": [
#                 {
#                     "title": "Transaction Count",
#                     "value": 86,
#                     "short": true
#                 },
#                 {
#                     "title": "Total Received",
#                     "value": "116.16871770 BTC",
#                     "short": true
#                 },
#                 {
#                     "title": "Total Sent",
#                     "value": "116.16871770 BTC",
#                     "short": true
#                 },
#                 {
#                     "title": "Balance",
#                     "value": "0 BTC",
#                     "short": true
#                 },
# 				{
# 					"title": "USD Value",
# 					"value": "$1.00",
# 					"short": true
# 				}
#             ]
#         },
# 		{
# 			"text": "Address: 12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw",
# 			"fallback": "Address: 12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw",
#             "fields": [
#                 {
#                     "title": "Transaction Count",
#                     "value": 86,
#                     "short": true
#                 },
#                 {
#                     "title": "Total Received",
#                     "value": "116.16871770 BTC",
#                     "short": true
#                 },
#                 {
#                     "title": "Total Sent",
#                     "value": "116.16871770 BTC",
#                     "short": true
#                 },
#                 {
#                     "title": "Balance",
#                     "value": "0 BTC",
#                     "short": true
#                 },
# 				{
# 					"title": "USD Value",
# 					"value": "$1.00",
# 					"short": true
# 				}
#             ]
#         }
#     ]
# }
