import asyncio

import pytest

from kopf._cogs.structs.bodies import RawBody, RawEvent
from kopf._cogs.structs.references import Insights
from kopf._core.reactor.observation import process_discovered_namespace_event


async def test_initial_listing_is_ignored():
    insights = Insights()
    e1 = RawEvent(type=None, object=RawBody(metadata={'name': 'ns1'}))

    async def delayed_injection(delay: float):
        await asyncio.sleep(delay)
        await process_discovered_namespace_event(
            insights=insights, raw_event=e1, namespaces=['ns*'])

    task = asyncio.create_task(delayed_injection(0))
    with pytest.raises(asyncio.TimeoutError):
        async with insights.revised:
            await asyncio.wait_for(insights.revised.wait(), timeout=0.1)
    await task
    assert not insights.namespaces


@pytest.mark.parametrize('etype', ['ADDED', 'MODIFIED'])
async def test_followups_for_addition(timer, etype):
    insights = Insights()
    e1 = RawEvent(type=etype, object=RawBody(metadata={'name': 'ns1'}))

    async def delayed_injection(delay: float):
        await asyncio.sleep(delay)
        await process_discovered_namespace_event(
            insights=insights, raw_event=e1, namespaces=['ns*'])

    task = asyncio.create_task(delayed_injection(0.1))
    with timer:
        async with insights.revised:
            await insights.revised.wait()
    await task
    assert 0.1 < timer.seconds < 0.11
    assert insights.namespaces == {'ns1'}


@pytest.mark.parametrize('etype', ['DELETED'])
async def test_followups_for_deletion(timer, etype):
    insights = Insights()
    insights.namespaces.add('ns1')
    e1 = RawEvent(type=etype, object=RawBody(metadata={'name': 'ns1'}))

    async def delayed_injection(delay: float):
        await asyncio.sleep(delay)
        await process_discovered_namespace_event(
            insights=insights, raw_event=e1, namespaces=['ns*'])

    task = asyncio.create_task(delayed_injection(0.1))
    with timer:
        async with insights.revised:
            await insights.revised.wait()
    await task
    assert 0.1 < timer.seconds < 0.11
    assert not insights.namespaces
