import aiohttp.web
import pytest

from kopf._cogs.clients.creating import create_obj
from kopf._cogs.clients.errors import APIError


async def test_simple_body_with_arguments(
        resp_mocker, aresponses, hostname, settings, resource, namespace, logger, caplog):

    post_mock = resp_mocker(return_value=aiohttp.web.json_response({}))
    aresponses.add(hostname, resource.get_url(namespace=namespace), 'post', post_mock)

    body = {'x': 'y'}
    await create_obj(
        logger=logger,
        settings=settings,
        resource=resource,
        namespace=namespace,
        name='name1',
        body=body,
    )

    assert post_mock.called
    assert post_mock.call_count == 1

    data = post_mock.call_args_list[0][0][0].data  # [callidx][args/kwargs][argidx]
    if resource.namespaced:
        assert data == {'x': 'y', 'metadata': {'name': 'name1', 'namespace': 'ns'}}
    else:
        assert data == {'x': 'y', 'metadata': {'name': 'name1'}}


async def test_full_body_with_identifiers(
        resp_mocker, aresponses, hostname, settings, resource, namespace, caplog, logger):

    post_mock = resp_mocker(return_value=aiohttp.web.json_response({}))
    aresponses.add(hostname, resource.get_url(namespace=namespace), 'post', post_mock)

    body = {'x': 'y', 'metadata': {'name': 'name1', 'namespace': namespace}}
    await create_obj(
        logger=logger,
        settings=settings,
        resource=resource,
        body=body,
    )

    assert post_mock.called
    assert post_mock.call_count == 1

    data = post_mock.call_args_list[0][0][0].data  # [callidx][args/kwargs][argidx]
    assert data == {'x': 'y', 'metadata': {'name': 'name1', 'namespace': namespace}}


# Note: 401 is wrapped into a LoginError and is tested elsewhere.
@pytest.mark.parametrize('status', [400, 403, 404, 409, 500, 666])
async def test_raises_api_errors(
        resp_mocker, aresponses, hostname, settings, status, resource, namespace, logger,
        cluster_resource, namespaced_resource):

    post_mock = resp_mocker(return_value=aresponses.Response(status=status, reason='oops'))
    cluster_url = cluster_resource.get_url(namespace=None)
    namespaced_url = namespaced_resource.get_url(namespace='ns')
    aresponses.add(hostname, cluster_url, 'post', post_mock)
    aresponses.add(hostname, namespaced_url, 'post', post_mock)

    body = {'x': 'y'}
    with pytest.raises(APIError) as e:
        await create_obj(
            logger=logger,
            settings=settings,
            resource=resource,
            namespace=namespace,
            name='name1',
            body=body,
        )
    assert e.value.status == status
