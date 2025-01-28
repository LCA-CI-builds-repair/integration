from __future__ import annotations
import pytest
from custom_components.hacs.base import HacsBase
from custom_components.hacs.repositories.base import HacsRepository

from tests.common import client_session_proxy


@pytest.mark.parametrize(
    "data,result",
    [
        ({"installed": True, "installed_version": "1.0.0"}, "Example readme file"),
        ({"installed": False, "last_version": "2.0.0"}, "Example readme file"),
    ],
)
@pytest.mark.asyncio
async def test_validate_repository(hacs: HacsBase, data: dict, result: str):
    repository = HacsRepository(hacs=hacs)
    repository.data.full_name = "octocat/integration"
    for key, value in data.items():
        setattr(repository.data, key, value)

    hacs.session = await client_session_proxy(hacs.hass)
    docs = await repository.get_documentation(filename="README.md")

    assert result in docs
