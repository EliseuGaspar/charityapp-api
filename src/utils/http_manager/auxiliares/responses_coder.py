from enum import Enum



class ResponseCodes(Enum):

	''' Retorna o c]odigo correspondente a mensagem http '''

	CONTINUE = 100 # CONTINUAR
	PROCESSING = 102 # PROCESSANDO
	OK = 200 # TUDO OK
	CREATED = 201 # SOLICITACAO CRIADA
	ACEPTED = 202 # SOLICITACAO ACEITE MAS SEM RESPOSTA DE RETORNO
	NO_CONTENT = 204 # SEM CONTEUDO PARA RETORNO
	MOVED_PERMANENTLY = 301 # ENDPOINT MOVIDO PERMANENTEMENTE
	SEE_OTHER = 303 # TENTE OUTRO ENDPOINT
	PERMANENT_REDIRECT = 308 # REDIRECIONAMENTOS PERMANENTE PARA ESTE ENDPOINT
	BAD_REQUEST = 400 # SOLICITACAO MAL FEITA, ALGO ERRADO NO PEDIDO
	UNAUTHORIZED = 401 # ACESSO REQUERIDO, LOGIN OU SIGUP
	FORBIDDEN = 403 # ACAO RECUSADA DEVIDO A ALGUMA COISA ERRADA COM A PERMISSAO
	NOT_FOUND = 404 # ENDPOINT ERRADO, NAO EXISTE ESTE ENDPOINT NO SISTEMA
	METHOD_NOT_ALLOWED = 405 # METODOD ERRADO PARA ESTE ENDPOINT
	REQUEST_TIMEOUT = 408 # TEMPO DE ESPERA EXPIRADO, O SERVIDOR ESPEROU MAS NAO RECEBEU
	CONFLICT = 409 # CONFLITO ENTRE OS DADOS ENVIADOS NA SOLICITACAO
	GONE = 410 # RECEURSO SOLICITADO NAO MAIS DISPONIVEL
	LENGTH_REQUIRED = 411 # EXTENSAO DE ARQUIVO ESPERADA MAS NAO PASSADA
	PRECONDITION_FALEID = 412 # FALTANDO OU PASSADO ALGO A MAIS NO CABECALHO DA SOLICITACAO
	PAYLOAD_TOO_LARGE = 413 # SOLICITACAO MUITO EXTENSA, DADOS GRANDES DE MAIS PARA O SERVIDOR
	UNSSUPORTED_MEDIA_TYPE = 415 # TIPO DE MIDIA NAO SUPORTADA
	MISDIRECTED_REQUEST = 421 # IMPOSSIVEL FORNECER UMA RESPOSTA PARA A SOLICITACAO
	UNPROCESSABLE_CONTENT = 422 # CONTEUDO INCAPAZ DE SER PROCESSADO
	BLOCKED = 423 # RECURSO SOLICITADO BLOQUEADO POR ENQUANTO
	TO_MANY_REQUEST = 429 # SOLICITACAO INCAPAZ DE SER LIDA
	INTERNAL_SERVER_ERROR = 500 # ERRO INTERNO NO SERVIDOR
	NOT_IMPLEMENTED = 501 # SEM UMA RESPOSTA PROPRIA PARA A SOLICITACAO
	SERVICE_UNAVAILABLE = 503 # SERVICO INDISPONIVEL NESTE SERVIDOR
	INSUFFICIENT_STORAGE = 507 # ESPACO INSUFICIENTE
	NETWORK_AUTENTICATION_REQUIRED = 511 # AUTORIZACAO REQUERIDA
	INVALID_TOKEN = 498 # TOKEN INVALIDO
	
