import os
from datetime import date
from typing import Any, Union, Dict
from urllib.parse import urlencode

from jinja2 import pass_context
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fastapi_admin2 import VERSION
from fastapi_admin2.constants import BASE_DIR

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals["VERSION"] = VERSION
templates.env.globals["NOW_YEAR"] = date.today().year
templates.env.add_extension("jinja2.ext.i18n")
templates.env.add_extension("jinja2.ext.autoescape")


@pass_context
def current_page_with_params(context: Dict[str, Any], params: Dict[str, Any]) -> str:
    request = context["request"]  # type: Request
    full_path = request.scope["raw_path"].decode()
    query_params = dict(request.query_params)
    for k, v in params.items():
        query_params[k] = v
    return full_path + "?" + urlencode(query_params)


templates.env.filters["current_page_with_params"] = current_page_with_params


def set_global_env(name: str, value: Any):
    templates.env.globals[name] = value


def add_template_folder(*folders: Union[str, os.PathLike]):
    for folder in folders:
        templates.env.loader.searchpath.insert(0, folder)  # type: ignore
