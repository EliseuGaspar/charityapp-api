from .auxiliares import CodesResponse, ResponseCodes



class HttpCodesResponses:
	''''''

	def __init__(self, ) -> None:
		''''''
		self._codes_response = CodesResponse
		self._response_codes = ResponseCodes

	@property
	def response_codes(self) -> ResponseCodes:
		return self._response_codes

	@property
	def codes_response(self) -> CodesResponse:
		return self._codes_response
