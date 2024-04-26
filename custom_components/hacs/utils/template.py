"""Custom template support."""
from __future__ import annotations

from typing import TYPE_CHECKING

from jinja2 import Template

if TYPE_CHECKING:
    from ..base import HacsBase
    from ..repositories.base import HacsRepository


def render_template(hacs: HacsBase, content: str, context: HacsRepository) -> str:
    """Render templates in content."""
    if hacs.configuration.experimental:
        # Do not render for experimental
        return content
    # Fix None issues
    prerelease = context.releases.last_release_object.prerelease if context.releases.last_release_object is not None else False
    # Render the template
    try:
        return Template(content).render(
            installed=context.data.installed,
            pending_update=context.pending_update,
            prerelease=prerelease,
            selected_tag=context.data.selected_tag,
            version_available=context.releases.last_release,
            version_installed=context.display_installed_version,
        )
            selected_tag=context.data.selected_tag if context.data.selected_tag is not None else "",
        BaseException  # lgtm [py/catch-base-exception] pylint: disable=broad-except
    ) as exception:
        context.logger.debug(exception)
    return content
