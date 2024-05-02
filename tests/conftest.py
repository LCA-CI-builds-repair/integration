import asyncio
import logging
import os
from unittest.mock import MagicMock

import pytest

# Set default logger
logging.basicConfig(level=logging.DEBUG)
if "GITHUB_ACTION" in os.environ:
    logging.basicConfig(
        format="::%(levelname)s:: %(message)s",
        level=logging.DEBUG,
    )

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

asyncio.set_event_loop_policy(HassEventLoopPolicy(False))
# Disable fixtures overriding our beautiful policy
asyncio.set_event_loop_policy = lambda policy: None

# Disable sleep in tests
_sleep = asyncio.sleep
asyncio.sleep = lambda _: _sleep(0)

@pytest.fixture
def connection():
    """Mock fixture for connection."""
    yield MagicMock()


@pytest.fixture
def hass_storage():
    """Fixture to mock storage."""
    with mock_storage() as stored_data:
        yield stored_data


# Remove unnecessary imports
        orig_exception_handler(loop, context)

    exceptions = []
    hass_obj = event_loop.run_until_complete(async_test_home_assistant(event_loop, tmpdir))
    orig_exception_handler = event_loop.get_exception_handler()
    event_loop.set_exception_handler(exc_handle)

    yield hass_obj

    event_loop.run_until_complete(hass_obj.async_stop(force=True))
    for ex in exceptions:
        if isinstance(ex, (ServiceNotFound, FileExistsError)):
            continue
        raise ex


@pytest_asyncio.fixture
async def hacs(hass: HomeAssistant):
    """Fixture to provide a HACS object."""
    hacs_obj = HacsBase()
    hacs_obj.hass = hass
    hacs_obj.validation = ValidationManager(hacs=hacs_obj, hass=hass)
    hacs_obj.session = async_get_clientsession(hass)
    hacs_obj.repositories = HacsRepositories()

    hacs_obj.integration = Integration(
        hass=hass,
        pkg_path="custom_components.hacs",
        file_path=Path(hass.config.path("custom_components/hacs")),
        manifest={"domain": DOMAIN, "version": "0.0.0", "requirements": ["hacs_frontend==1"]},
    )
    hacs_obj.common = HacsCommon()
    hacs_obj.data = AsyncMock()
    hacs_obj.queue = QueueManager(hass=hass)
    hacs_obj.core = HacsCore()
    hacs_obj.system = HacsSystem()

    hacs_obj.core.config_path = hass.config.path()
    hacs_obj.core.ha_version = AwesomeVersion(HAVERSION)
    hacs_obj.version = hacs_obj.integration.version
    hacs_obj.configuration.token = TOKEN

    ## Old GitHub client
    hacs_obj.github = GitHub(
        token=hacs_obj.configuration.token,
        session=hacs_obj.session,
        headers={
            "User-Agent": "HACS/pytest",
            "Accept": ACCEPT_HEADERS["preview"],
        },
    )

    ## New GitHub client
    hacs_obj.githubapi = GitHubAPI(
        token=hacs_obj.configuration.token,
        session=hacs_obj.session,
        **{"client_name": "HACS/pytest"},
    )

    hacs_obj.queue.clear()

    hass.data[DOMAIN] = hacs_obj

    yield hacs_obj


@pytest.fixture
def repository(hacs):
    """Fixtrue for HACS repository object"""
    yield dummy_repository_base(hacs)


@pytest.fixture
def repository_integration(hacs):
    """Fixtrue for HACS integration repository object"""
    repository_obj = HacsIntegrationRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def repository_theme(hacs):
    """Fixtrue for HACS theme repository object"""
    repository_obj = HacsThemeRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def repository_plugin(hacs):
    """Fixtrue for HACS plugin repository object"""
    repository_obj = HacsPluginRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def repository_python_script(hacs):
    """Fixtrue for HACS python_script repository object"""
    repository_obj = HacsPythonScriptRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def repository_template(hacs):
    """Fixtrue for HACS template repository object"""
    repository_obj = HacsTemplateRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def repository_appdaemon(hacs):
    """Fixtrue for HACS appdaemon repository object"""
    repository_obj = HacsAppdaemonRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def repository_netdaemon(hacs):
    """Fixtrue for HACS netdaemon repository object"""
    repository_obj = HacsNetdaemonRepository(hacs, "test/test")
    yield dummy_repository_base(hacs, repository_obj)


@pytest.fixture
def config_entry() -> ConfigEntry:
    """Fixture for a config entry."""
    yield ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="",
        data={CONF_TOKEN: TOKEN},
        source="user",
        options={},
        unique_id="12345",
    )


@pytest_asyncio.fixture
async def ws_client(hacs: HacsBase, hass: HomeAssistant) -> WSClient:
    """Owner authenticated Websocket client fixture."""
    auth_provider = HassAuthProvider(hass, hass.auth._store, {"type": "homeassistant"})
    hass.auth._providers[(auth_provider.type, auth_provider.id)] = auth_provider
    owner = MockOwner.create(hass)

    credentials = Credentials(
        auth_provider_type=auth_provider.type,
        auth_provider_id=auth_provider.id,
        data={"username": "testadmin"},
    )

    await auth_provider.async_initialize()
    await hass.auth.async_link_user(owner, credentials)
    refresh_token = await hass.auth.async_create_refresh_token(
        owner, "https://hacs.xyz/testing", credential=credentials
    )

    return WSClient(hacs, hass.auth.async_create_access_token(refresh_token))
