from pydantic import HttpUrl

from openremote.api.asset import Asset
from openremote.authenticator import Authenticator
from openremote.http import HttpClient
from openremote.schemas.asset_object import AssetObject
from openremote.url_builder import UrlBuilder


class OpenRemoteClient:
    authenticator: Authenticator
    url_builder: UrlBuilder
    http_client: HttpClient

    asset: Asset

    def __init__(self, openremote_host: HttpUrl | str, client_id: str, client_secret: str):
        self.url_builder = UrlBuilder(openremote_host)
        self.authenticator = Authenticator(self.url_builder, client_id, client_secret)
        self.http_client = HttpClient(self.url_builder, self.authenticator)

        self.asset = Asset(self.http_client)
