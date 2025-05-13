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
"""Escape reserved characters."""

import os
import re

__TEX_CONV = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\^{}",
    "\\": r"\textbackslash{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
    "®": r"\textsuperscript{\textregistered}",
    "©": r"\textcopyright{}",
    "™": r"\textsuperscript{\texttrademark}",
}
__TEX_REGEX = re.compile("|".join(re.escape(key) for key in sorted(__TEX_CONV.keys(), key=lambda item: -len(item))))


def tex(text: str | None):
    r"""
    Escape (La)Tex.

    Args:
        text: tex
    Returns:
        escaped string.

        >>> tex("Foo & Bar")
        'Foo \\& Bar'
        >>> tex(None)
    """
    if text is None:
        return None
    result = __TEX_REGEX.sub(lambda match: __TEX_CONV[match.group()], str(text))
    if os.linesep != "\n":
        return result.replace("\n", os.linesep)
    return result
