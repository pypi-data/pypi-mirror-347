# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
"""Internal helper functions for working with temporary files."""

from __future__ import annotations

import json
import tempfile
import time
import warnings
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any
import platform

from airbyte.constants import TEMP_DIR_OVERRIDE


if TYPE_CHECKING:
    from collections.abc import Generator


@contextmanager
def as_temp_files(files_contents: list[dict | str]) -> Generator[list[str], Any, None]:
    temp_files: list[Any] = []
    try:
        for content in files_contents:
            use_json = isinstance(content, dict)
            temp_file = tempfile.NamedTemporaryFile(
                mode="w+t",
                delete=False,
                encoding="utf-8",
                dir=TEMP_DIR_OVERRIDE or None,
                suffix=".json" if use_json else ".txt",
            )
            temp_file.write(
                json.dumps(content) if isinstance(content, dict) else content,
            )
            temp_file.flush()

            if platform.system() == "Windows":
                docker_path = f"/tmp/{Path(temp_file.name).name}"
                temp_files.append((temp_file, docker_path))
            else:
                temp_files.append(temp_file)

        if platform.system() == "Windows":
            yield [docker_path for _, docker_path in temp_files]
        else:
            yield [file.name for file in temp_files]

    finally:
        if platform.system() == "Windows":
            for temp_file, _ in temp_files:
                _cleanup_temp_file(temp_file)
        else:
            for temp_file in temp_files:
                _cleanup_temp_file(temp_file)


def _cleanup_temp_file(temp_file):
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            with suppress(Exception):
                temp_file.close()
            Path(temp_file.name).unlink(missing_ok=True)
            break
        except Exception as ex:
            if attempt < max_attempts - 1:
                time.sleep(1)
            else:
                warnings.warn(
                    f"Failed to remove temporary file: '{temp_file.name}'. {ex}",
                    stacklevel=2,
                )
