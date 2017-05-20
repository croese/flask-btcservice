from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def index():
    result = {
    	"response_type": "in_channel",
        "text": "Address: `115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn`",
        "attachments": [
            {
    			"fields": [
    				{
    					"title": "Transaction Count",
    					"value": 86,
    					"short": True
    				},
    				{
    					"title": "Total Received",
    					"value": "116.16871770 BTC",
    					"short": True
    				},
    				{
    					"title": "Total Sent",
    					"value": "116.16871770 BTC",
    					"short": True
    				},
    				{
    					"title": "Balance",
    					"value": "0 BTC",
    					"short": True
    				}
    			]
            }
        ]
    }
    return jsonify(result)
