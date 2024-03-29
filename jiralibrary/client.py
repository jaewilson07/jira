# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/client.ipynb.

# %% ../nbs/client.ipynb 3
from __future__ import annotations

from dataclasses import dataclass, field
from pprint import pprint
import httpx

# %% auto 0
__all__ = ['ResponseGetData', 'get_data']

# %% ../nbs/client.ipynb 4
@dataclass
class ResponseGetData:
    """class for returning data from any jiralibrary route"""

    status: int
    response: str
    auth: any = field(repr=False, default=None)
    is_success: bool = False

    def __post_init__(self):
        self.is_success = True if self.status >= 200 and self.status <= 399 else False

    @classmethod
    def _from_httpx_response(cls, res: httpx.Response, auth=None):
        rgd = cls(status=res.status_code, response=res.json(), auth=auth)

        return rgd

# %% ../nbs/client.ipynb 7
async def get_data(
    url: str,
    method: str,
    auth: any,
    headers: dict = None,
    params: dict = None,
    debug_api: bool = False,
    body=None,
    session: httpx.AsyncClient = None,
) -> ResponseGetData:
    """wrapper for httpx Request library, always use with jiralibrary class"""

    is_close_session = False
    method = method.lower()

    if not headers:
        headers = {"Accept": "application/json"}

    if auth:
        headers = {**headers, **auth.generate_auth_header()}

    if not session:
        session = httpx.AsyncClient()
        is_close_session = True

    if debug_api:
        pprint({"url": url, "headers": headers, "params": params, "body": body})

    if method == "get":
        res = await getattr(session, method)(url=url, headers=headers, params=params)
    else:
        res = await getattr(session, method)(
            url=url, headers=headers, params=params, data=body
        )

    if is_close_session:
        await session.aclose()

    return ResponseGetData._from_httpx_response(res)
