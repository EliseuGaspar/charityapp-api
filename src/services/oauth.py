""""""
import os, requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from flask import session
import google.auth.transport.requests
import requests_oauthlib



class GOAuth:

    flow: Flow
    
    def __init__(self) -> None:
        """"""
        pass

    def __setInfos(self, redirect_link : str):
        """"""
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secrets_file = os.path.join("src","files","client_secret.json")
        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=self.client_secrets_file,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid"
            ],
            redirect_uri=redirect_link
        )
    
    def get_link(self, redirect_link : str) -> str:
        """"""
        self.__setInfos(redirect_link)
        self.authorization_url, self.state = self.flow.authorization_url()
        session["state"] = self.state
        return self.authorization_url
    
    def get_flow_var(self) -> object:
        """"""
        return self.flow


GoogleAuth = GOAuth()
