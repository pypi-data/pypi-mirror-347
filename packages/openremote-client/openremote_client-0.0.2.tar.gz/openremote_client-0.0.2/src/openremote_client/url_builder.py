from pydantic import HttpUrl


class UrlBuilder:
    __base_url: HttpUrl

    def __init__(self, base_url: HttpUrl | str):
        self.__base_url = HttpUrl(base_url)

    def build(self, path: str) -> str:
        path = path.lstrip("/")

        return HttpUrl.build(
            scheme=self.__base_url.scheme,
            host=self.__base_url.host,
            port=self.__base_url.port,
            path=path
        ).encoded_string()
