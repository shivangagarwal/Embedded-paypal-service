#Service Layer API for the Paypal Adaptive payments
import urllib, urllib2
import logging
import simplejson as json
log = logging.getLogger(__name__)
class PaypalAdaptivePayment(Document):
    """
    Paypal Object to initialize and conducting the payments
    """
    def __init__(self, paypal_sandbox_enabled):
    '''Constructor for the Paypal Api Sets the headers and api credentials which are required for the initialization of the payments
    '''
	assert paypal_sandbox_enabled, "missing arguments..."
	self.request_data_format = 'JSON'
	self.response_data_format = 'JSON'
	self.paypal_sandbox_enabled = paypal_sandbox_enabled
	if paypal_sandbox_enabled:
	    self.paypal_secure_user_id = "your sandbox API user id"
	    self.paypal_secure_password = "Your sandbox API password"
	    self.paypal_api_signature = "Your sandbox API signature"
	    self.receiver_email = "Your sandbox receiver email"
	    self.request_url =  "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay"
	else:
	    self.paypal_secure_user_id = "your live paypal secure user id"
	    self.paypal_secure_password = "your live secure password"
	    self.paypal_api_signature = "Your live ApI signature"
	    self.receiver_email = "Your Live Receiver Email"
	    self.request_url =  "https://paypal.com/AdaptivePayments/Pay"

    def initialize_payment(self,amount,cancel_url,return_url):
    try:
	header_data = {}
	header_data["X-PAYPAL-SECURITY-USERID"] = self.paypal_secure_user_id
	header_data["X-PAYPAL-SECURITY-PASSWORD"] = self.paypal_secure_password
	header_data["X-PAYPAL-SECURITY-SIGNATURE"] = self.paypal_api_signature
	header_data["X-PAYPAL-REQUEST-DATA-FORMAT"] = self.request_data_format
	header_data["X-PAYPAL-RESPONSE-DATA-FORMAT"] = self.response_data_format
	if self.paypal_sandbox_enabled:
	    header_data["X-PAYPAL-APPLICATION-ID"] = "APP-80W284485P519543T"
	else:
	    header_data["X-PAYPAL-APPLICATION-ID"] = "Your Live Paypal Application ID"
	params = {'actionType':'PAY', 'receiverList':{'receiver':[{'email':self.receiver_email,'amount':amount}]}, 'cancelUrl':cancel_url, 'requestEnvelope':\   'errorLanguage':'en_US'}, 'currencyCode':'USD', 'returnUrl':return_url}
	paypal_request_data = json.dumps(params)
	req = urllib2.Request(self.request_url,paypal_request_data,header_data)
	response = urllib2.urlopen(req)
	return json.loads(response.read())
    except:
    log.exception("Unable to initialize the payment flow...")
