# Code generated. DO NOT EDIT.

import dataclasses
from typing import Any, Dict


@dataclasses.dataclass
class BuiltinEmailConnection:
    """
    The builtin email specific connection data.
    """

    def __json_encode__(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        return data

    @staticmethod
    def __json_decode__(data: Dict[str, Any]) -> "BuiltinEmailConnection":
        if data is None:
            data = {}

        kwargs: Dict[str, Any] = {}

        return BuiltinEmailConnection(**kwargs)
