#
# MIT License
#
# Copyright (c) 2023-2025 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Configuration Handling."""

from collections.abc import Callable
from pathlib import Path

from attrs import define
from outputfile import Existing

COMMENT_MAP_DEFAULT = {
    ".c": "//",
    ".c++": "//",
    ".cpp": "//",
    ".ini": "#",
    ".py": "#",
    ".sv": "//",
    ".svh": "//",
    ".tex": "%",
    ".txt": "//",
    ".v": "//",
    ".vh": "//",
}


@define
class Config:
    """
    Configuration.

    Container For All Customization Options.

    The following file extensions are known:

        >>> for suffix, comment in Config().comment_map.items():
        ...     print(f"{suffix}: {comment}")
        .c: //
        .c++: //
        .cpp: //
        .ini: #
        .py: #
        .sv: //
        .svh: //
        .tex: %
        .txt: //
        .v: //
        .vh: //
    """

    template_paths: list[Path] = []  # noqa: RUF008
    """Default Search Paths for Templates."""

    existing: Existing = Existing.KEEP_TIMESTAMP
    """Behaviour in case of existing files."""

    diffout: Callable[[str], None] | None = None
    """``print`` function to handle differential output on changed files."""

    verbose: bool = False
    """Enable Verbose Output."""

    create: bool = False
    """Create Missing Inplace Files."""

    template_marker: str = "MAKO TEMPLATE"
    """Search marker for template code within output file."""

    inplace_marker: str = "GENERATE INPLACE"
    """Search marker for output code within output file."""

    static_marker: str = "STATIC"
    """Marker for Static Code."""

    marker_fill: str = "="
    """Marker Filling."""

    marker_linelength: int = 0
    """Marker Line Length for Filling."""

    cache_path: Path | None = None
    """
    Cache Directory.

    Used to store converted templates. Use if you have many and/or large templates.
    Speeds up rendering. Share it between runs.
    """

    comment_map: dict[str, str] = COMMENT_MAP_DEFAULT
    """
    Line Comment Symbols.

    File Suffix dependent comment starter.
    """

    inplace_eol_comment: str | None = None
    """End-Of-Line Comment Added On Every Inplace Generated Line """

    track: bool = False
    """Track Changes."""

    tag_lines: int = 50
    """Number Of Lines Within A Files to look for Tags."""
