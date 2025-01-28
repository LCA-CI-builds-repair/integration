from typing import Any
import pytest
from custom_components.hacs.base import HacsBase  # pylint: disable=unused-import
from custom_components.hacs.repositories.base import HacsRepository  # pylint: disable=unused-import

from tests.common import client_session_proxy

# pylint: disable=unused-argument

@pytest.mark.parametrize("data,result", [
    ({"installed": True, "installed_version": "1.0.0"}, "Example readme file"),
    ({"installed": False, "last_version": "2.0.0"}, "Example readme file")
])
@pytest.mark.asyncio
async def test_validate_repository(hacs: HacsBase, data: dict[str, Any], result: str):
    repository = HacsRepository(hacs=hacs)
    repository.data.full_name = "octocat/integration"
    repository.data.__dict__.update(data)

    hacs.session = await client_session_proxy(hacs.hass)
    docs = await repository.get_documentation(filename="README.md")

    assert result in docs
