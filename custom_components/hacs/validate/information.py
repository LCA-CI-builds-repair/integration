from __future__ import annotations

from ..repositories.base import HacsRepository
from .base import ActionValidationBase, ValidationException


async def async_setup_validator(repository: HacsRepository) -> Validator:
    """Set up this validator."""
    return Validator(repository=repository)


class Validator(ActionValidationBase):
    """Validate the repository."""

    more_info = "https://hacs.xyz/docs/publish/include#check-info"

    async def async_validate(self):
        """Validate the repository."""
        filenames = [x.filename.lower() for x in self.repository.tree]
        if "readme" not in filenames and "readme.md" not in filenames and "info" not in filenames and "info.md" not in filenames:
            raise ValidationException("The repository has no information file")
