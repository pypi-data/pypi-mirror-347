from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.geoteknisk_borehull import GeotekniskBorehull
from ...models.validated_geoteknisk_borehull import ValidatedGeotekniskBorehull
from ...types import Response


def _get_kwargs(
    geoteknisk_unders_id: str,
    geoteknisk_borehull_id: str,
    *,
    body: GeotekniskBorehull,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/GeotekniskUnders/{geoteknisk_unders_id}/GeotekniskBorehull/{geoteknisk_borehull_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ValidatedGeotekniskBorehull]:
    if response.status_code == 200:
        response_200 = ValidatedGeotekniskBorehull.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ValidatedGeotekniskBorehull]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    geoteknisk_unders_id: str,
    geoteknisk_borehull_id: str,
    *,
    client: AuthenticatedClient,
    body: GeotekniskBorehull,
) -> Response[ValidatedGeotekniskBorehull]:
    """Updates a GeotekniskBorehull.

     Updates a GeotekniskBorehull.

    Args:
        geoteknisk_unders_id (str):
        geoteknisk_borehull_id (str):
        body (GeotekniskBorehull): geografisk område representert ved et punkt som er den logiske
            enhet for tolking av laginndeling og egenskaper til de forskjellige jordlag
            <engelsk>geographical area represented by a location which is the logical unit for
            interpretation of stratification and properties for the different strata </engelsk>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValidatedGeotekniskBorehull]
    """

    kwargs = _get_kwargs(
        geoteknisk_unders_id=geoteknisk_unders_id,
        geoteknisk_borehull_id=geoteknisk_borehull_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    geoteknisk_unders_id: str,
    geoteknisk_borehull_id: str,
    *,
    client: AuthenticatedClient,
    body: GeotekniskBorehull,
) -> Optional[ValidatedGeotekniskBorehull]:
    """Updates a GeotekniskBorehull.

     Updates a GeotekniskBorehull.

    Args:
        geoteknisk_unders_id (str):
        geoteknisk_borehull_id (str):
        body (GeotekniskBorehull): geografisk område representert ved et punkt som er den logiske
            enhet for tolking av laginndeling og egenskaper til de forskjellige jordlag
            <engelsk>geographical area represented by a location which is the logical unit for
            interpretation of stratification and properties for the different strata </engelsk>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ValidatedGeotekniskBorehull
    """

    return sync_detailed(
        geoteknisk_unders_id=geoteknisk_unders_id,
        geoteknisk_borehull_id=geoteknisk_borehull_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    geoteknisk_unders_id: str,
    geoteknisk_borehull_id: str,
    *,
    client: AuthenticatedClient,
    body: GeotekniskBorehull,
) -> Response[ValidatedGeotekniskBorehull]:
    """Updates a GeotekniskBorehull.

     Updates a GeotekniskBorehull.

    Args:
        geoteknisk_unders_id (str):
        geoteknisk_borehull_id (str):
        body (GeotekniskBorehull): geografisk område representert ved et punkt som er den logiske
            enhet for tolking av laginndeling og egenskaper til de forskjellige jordlag
            <engelsk>geographical area represented by a location which is the logical unit for
            interpretation of stratification and properties for the different strata </engelsk>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValidatedGeotekniskBorehull]
    """

    kwargs = _get_kwargs(
        geoteknisk_unders_id=geoteknisk_unders_id,
        geoteknisk_borehull_id=geoteknisk_borehull_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    geoteknisk_unders_id: str,
    geoteknisk_borehull_id: str,
    *,
    client: AuthenticatedClient,
    body: GeotekniskBorehull,
) -> Optional[ValidatedGeotekniskBorehull]:
    """Updates a GeotekniskBorehull.

     Updates a GeotekniskBorehull.

    Args:
        geoteknisk_unders_id (str):
        geoteknisk_borehull_id (str):
        body (GeotekniskBorehull): geografisk område representert ved et punkt som er den logiske
            enhet for tolking av laginndeling og egenskaper til de forskjellige jordlag
            <engelsk>geographical area represented by a location which is the logical unit for
            interpretation of stratification and properties for the different strata </engelsk>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ValidatedGeotekniskBorehull
    """

    return (
        await asyncio_detailed(
            geoteknisk_unders_id=geoteknisk_unders_id,
            geoteknisk_borehull_id=geoteknisk_borehull_id,
            client=client,
            body=body,
        )
    ).parsed
