import datetime as dt
import logging
import logging.config
import pathlib
from typing import Any, Callable, Optional, TypeVar, Union, overload

import yaml

__all__ = [
    "setup_logging",
]


_Callable = Callable[..., Any]
_C = TypeVar("_C", bound=_Callable)


@overload
def setup_logging(
    name: Optional[str] = None,
    *,
    logs: str = r"./logs/",
    logging_yaml: str = r"./logging.yaml",
) -> Callable[[_C], _C]: ...


@overload
def setup_logging(
    func: _C,
) -> _C: ...


def setup_logging(
    name_or_func: Union[Optional[str], _Callable] = None,
    *,
    logs: str = r"./logs/",
    logging_yaml: str = r"./logging.yaml",
) -> Union[Callable[[_Callable], _Callable], _Callable]:
    if callable(name_or_func):
        func = name_or_func
        return setup_logging()(func)
    name = (
        dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        if name_or_func is None
        else name_or_func
    )
    log_dir = pathlib.Path(logs) / name
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(logging_yaml, mode="rb") as f:
        logging_config = yaml.safe_load(f)
    for handler in (
        x for x in logging_config.get("handlers", {}).values() if "filename" in x
    ):
        handler["filename"] = str(log_dir / handler["filename"])
    logging.config.dictConfig(logging_config)

    def decorator(
        func: _C,
    ) -> _C:
        return func

    return decorator
