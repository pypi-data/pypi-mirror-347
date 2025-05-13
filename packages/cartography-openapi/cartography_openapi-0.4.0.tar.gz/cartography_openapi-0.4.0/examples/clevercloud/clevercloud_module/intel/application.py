import logging
from typing import Any
from typing import Dict
from typing import List
import requests

import neo4j
from dateutil import parser as dt_parse
from requests import Session

from cartography.client.core.tx import load
from cartography.graph.job import GraphJob
from cartography.models.clevercloud.application import CleverCloudApplicationSchema
from cartography.util import timeit


logger = logging.getLogger(__name__)
# Connect and read timeouts of 60 seconds each; see https://requests.readthedocs.io/en/master/user/advanced/#timeouts
_TIMEOUT = (60, 60)


@timeit
def sync(
    neo4j_session: neo4j.Session,
    api_session: requests.Session,
    common_job_parameters: Dict[str, Any],
    id,
) -> List[Dict]:
    applications = get(
        api_session,
        common_job_parameters['BASE_URL'],
        id,
    )
    # CHANGEME: You can configure here a transform operation
    # formated_applications = transform(applications)
    load_applications(
        neo4j_session,
        applications,  # CHANGEME: replace with `formated_applications` if your added a transform step
        id,
        common_job_parameters['UPDATE_TAG'])
    cleanup(neo4j_session, common_job_parameters)


@timeit
def get(
    api_session: requests.Session,
    base_url: str,
    id,
) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    # CHANGEME: You have to handle pagination if needed
    req = api_session.get(
        "{base_url}".format(
            base_url=base_url,
            id=id,
        ),
        timeout=_TIMEOUT
    )
    req.raise_for_status()
    results = req.json()
    return results


def load_applications(
    neo4j_session: neo4j.Session,
    data: List[Dict[str, Any]],
    id,
    update_tag: int,
) -> None:
    load(
        neo4j_session,
        CleverCloudApplicationSchema(),
        data,
        lastupdated=update_tag,
        id=id,
    )


def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict[str, Any]) -> None:
    GraphJob.from_node_schema(
        CleverCloudApplicationSchema(),
        common_job_parameters
    ).run(neo4j_session)