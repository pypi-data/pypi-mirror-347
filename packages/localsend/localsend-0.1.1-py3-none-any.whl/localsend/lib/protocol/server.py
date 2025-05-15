import functools
import typing
import urllib.parse

import pydantic
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from localsend.lib import util

from . import endpoints


def define[Q: pydantic.BaseModel, ReqB: pydantic.BaseModel, ResB: pydantic.BaseModel, S](
    spec: endpoints.Endpoint[Q, ReqB, ResB], routes: list[Route]
):
    def inner(f: typing.Callable[[Q, ReqB, S, Request], typing.Awaitable[ResB | Response]]):
        @functools.wraps(f)
        async def _wrapper(request: Request):
            try:
                querry = spec.querry.model_validate(dict(urllib.parse.parse_qsl(request.url.query)))
            except pydantic.ValidationError as exc:
                util.LOGGER.info(f'Querry validation error {exc}, validating {request.url.query}')
                return Response('Invalid querry', status_code=400)

            if issubclass(spec.request_body, endpoints.Empty):
                request_body = spec.request_body.model_validate({})
            else:
                try:
                    request_body = spec.request_body.model_validate_json(await request.body())
                except pydantic.ValidationError as exc:
                    util.LOGGER.info(
                        f'Body validation error {exc}, validating {await request.body()}'
                    )
                    return Response('Invalid body', status_code=400)

            response = await f(querry, request_body, request.state.state, request)
            if isinstance(response, Response):
                return response
            return Response(
                content=response.model_dump_json(), headers={'Content-Type': 'application/json'}
            )

        routes.append(Route(spec.path, _wrapper, methods=[spec.method]))

        return _wrapper

    return inner
