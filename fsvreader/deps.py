import karp_api_client
from fastapi import Request


def get_karp_client(request: Request) -> karp_api_client.Client:
    return request.app.state._karp_client
