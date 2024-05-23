from enum import Enum



class CodesResponse(Enum):

	''' Retorna uma mensagem contendo o motivo do erro '''

	CONTINUE = 'the header has been received, waiting for the rest of the data.'
	PROCESSING = 'request received, processing the data, continue!'
	OK = 'request made'
	CREATED = 'requested resource created successfully'
	ACEPTED = 'request received but not completed'
	NO_CONTENT = 'request executed! No return'
	MOVED_PERMANENTLY = 'dead endpoint, perform the operation on this endpoint'
	SEE_OTHER = 'request executed successfully! Get the answer in'
	PERMANENT_REDIRECT = 'redirect this and similar requests to this endpoint'
	BAD_REQUEST = 'processing impossible, check the content of your request'
	UNAUTHORIZED = 'unauthorized access, make sure you have an access token'
	FORBIDDEN = 'action refused, check your permissions'
	NOT_FOUND = 'the requested resource was not found'
	METHOD_NOT_ALLOWED = 'incompatible request method'
	REQUEST_TIMEOUT = 'expired waiting time'
	CONFLICT = 'the resource sent has conflicts in its data'
	GONE = 'this feature is no longer available'
	LENGTH_REQUIRED = 'error reading content, extension not specified'
	PRECONDITION_FALEID = 'failed to load the order, there is an error in the content sent, missing data or more'
	PAYLOAD_TOO_LARGE = 'make sure this request is for this endpoint. Content too long, impossible to load'
	UNSSUPORTED_MEDIA_TYPE = 'This type of media is not supported by the system'
	MISDIRECTED_REQUEST = 'It is not possible to provide an answer'
	UNPROCESSABLE_CONTENT = 'Unable to read your request'
	BLOCKED = 'this feature is blocked for now'
	TO_MANY_REQUEST = 'your attempts to access this resource have expired'
	INTERNAL_SERVER_ERROR = 'An internal error occurred before completing your order'
	NOT_IMPLEMENTED = 'request without a response of its own'
	SERVICE_UNAVAILABLE = 'service unavailable, the server was unable to handle your request'
	INSUFFICIENT_STORAGE = 'the server no longer has the capacity to store data'
	NETWORK_AUTENTICATION_REQUIRED = 'You need access to perform this operation'
