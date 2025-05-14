from typing import Any, Optional

from jinja2 import (
    Environment,
    StrictUndefined,
    Template,
    TemplateSyntaxError,
    meta,
)

JINJA2_FILE_STANDARD_REGEX = r".*\.jinja2$"


def render_template(
    template_str: Optional[str], *args: Any, **kwargs: Any
) -> str:
    if template_str is None:
        return ""
    return Template(template_str).render(*args, **kwargs).strip()


def render_template_with_none_return_allowed(
    template_str: Optional[str], *args: Any, **kwargs: Any
) -> Optional[str]:
    if template_str is None:
        return None
    render_result = Template(template_str).render(*args, **kwargs).strip()
    return render_result if render_result else None


def get_template_variables(template_str: str) -> set[str]:
    """
    Extracts the set of variables that are expected (not defined in the template).
    """
    env = Environment(undefined=StrictUndefined)
    try:
        parsed_template = env.parse(template_str)
    except TemplateSyntaxError as e:
        raise ValueError(f"Invalid Jinja2 syntax: {e}") from e
    return meta.find_undeclared_variables(parsed_template)
