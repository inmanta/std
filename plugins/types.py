"""
    Copyright 2023 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import re
import typing

import pydantic


def regex_string(regex: typing.Union[str, re.Pattern]) -> type:
    """Build a regex constrained string that is both supported by pydantic v1 and v2

    :param regex: A regex string or compiler regex pattern
    :return: A type that the current pydantic can use for validation
    """
    try:
        # v2
        return typing.Annotated[
            str,
            pydantic.AfterValidator(
                pydantic.TypeAdapter(
                    pydantic.constr(pattern=regex),
                    config=pydantic.ConfigDict(regex_engine="python-re"),
                ).validate_python
            ),
        ]
    except AttributeError:
        # v1
        return pydantic.constr(regex=regex)
