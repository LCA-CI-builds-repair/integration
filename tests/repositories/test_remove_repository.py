import os
import os
from pathlib import Path
from typing import Generator

from homeassistant.core import HomeAssistant
import pytest

from custom_components.hacs.enums import HacsCategory

from tests.common import (
    CategoryTestData,
    WSClient,
    category_test_data_parametrized,
    get_hacs,
)
from tests.conftest import SnapshotFixture

    await snapshots.assert_hacs_data(
        hacs, f"{category_test_data['repository']}/test_remove_repository_post.json"
    )
