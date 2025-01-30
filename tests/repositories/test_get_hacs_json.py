import pytest  # noqa: F401
from custom_components.hacs.base import HacsBase
from custom_components.hacs.repositories.base import HacsRepository

from tests.common import client_session_proxy



@pytest.mark.parametrize("version,expected_name", [
    ("1.0.0", "Proxy integration"),
    ("99.99.99", None),
])
@pytest.mark.asyncio
async def test_validate_repository(
    hacs: HacsBase, version: str, expected_name: str | None
):
    repository = HacsRepository(hacs=hacs)
    repository.data.full_name = "octocat/integration"

    hacs.session = await client_session_proxy(hacs.hass)
    manifest = await repository.get_hacs_json(version=version)

    if expected_name:
        assert manifest.name == expected_name
    else:
        assert manifest is None
