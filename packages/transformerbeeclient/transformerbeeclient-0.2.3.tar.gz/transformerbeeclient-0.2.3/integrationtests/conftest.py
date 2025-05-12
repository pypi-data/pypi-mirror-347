import os
from typing import AsyncGenerator, Generator

import pytest
from docker.errors import DockerException
from testcontainers.core.container import DockerContainer  # type:ignore[import-untyped]
from testcontainers.core.network import Network  # type:ignore[import-untyped]
from testcontainers.core.waiting_utils import (  # type:ignore[import-untyped]
    wait_container_is_ready,
    wait_for_logs,
)
from yarl import URL

from transformerbeeclient import (
    AuthenticatedTransformerBeeClient,
    TransformerBeeClient,
    UnauthenticatedTransformerBeeClient,
)

_TRANSFORMER_BEE_HTTP_GRPC_PORT = 5000
_TRANSFORMER_BEE_HTTP_REST_PORT = 5001


@pytest.fixture(scope="session")
def docker_network() -> Network:
    """Creates a shared Docker network for inter-container communication."""
    try:
        network = Network()
    except DockerException as docker_exception:
        if "Error while fetching server API version" in str(docker_exception):
            raise OSError(
                # pylint:disable=line-too-long
                "For the tests that involve the actual transformer.bee, you need to have a transformer.bee container running in docker. But it seems like Docker Desktop is not running."
            ) from docker_exception
        raise
    network.create()
    yield network
    network.remove()


@pytest.fixture(scope="session")
def start_transformer_bee_on_localhost(docker_network: Network) -> Generator[int, None, None]:
    """
    Starts transformer.bee.
    Yields the exposed http (REST) port.
    """
    transformer_bee_container = DockerContainer("ghcr.io/enercity/edifact-bo4e-converter/edifactbo4econverter:v1.4.1")
    transformer_bee_container.with_network(docker_network)
    transformer_bee_container.with_exposed_ports(_TRANSFORMER_BEE_HTTP_REST_PORT)
    transformer_bee_container.with_env("StorageProvider", "Directory")
    transformer_bee_container.start()
    wait_container_is_ready(transformer_bee_container)
    wait_for_logs(transformer_bee_container, r".*Application started\. Press Ctrl\+C to shut down\..*", timeout=30)
    port_on_localhost = transformer_bee_container.get_exposed_port(_TRANSFORMER_BEE_HTTP_REST_PORT)
    yield int(port_on_localhost)
    transformer_bee_container.stop()


@pytest.fixture(scope="function")
async def unauthenticated_client(start_transformer_bee_on_localhost: int) -> AsyncGenerator[TransformerBeeClient, None]:
    """
    A fixture that yields an unauthenticated client for the transformer.bee API running in a docker container
    on localhost.
    """
    client = UnauthenticatedTransformerBeeClient(
        base_url=URL(f"http://localhost:{start_transformer_bee_on_localhost}/")
    )
    yield client
    await client.close_session()


_test_system_url = URL("https://transformer.utilibee.io")


@pytest.fixture
async def oauthenticated_client() -> AsyncGenerator[TransformerBeeClient, None]:
    """
    A fixture that yields an OAuth client ID / client secret authenticated client for the transformer.bee API
    running in our online test system
    """
    # Those env variables shall be set by the Integration Test GitHub Action
    client_id = os.environ.get("AUTH0_TEST_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_TEST_CLIENT_SECRET")
    assert client_id is not None
    assert client_secret is not None  # <-- use pytest.skip instead of assert for local tests
    client = AuthenticatedTransformerBeeClient(
        _test_system_url, oauth_client_id=client_id, oauth_client_secret=client_secret
    )
    yield client
    await client.close_session()
