"""pascal_string_escape_lib — decode Pascal/Delphi string literals.

This package exposes a single function, ``decode``, which converts a
Pascal or Delphi string literal (without the surrounding single quotes)
into a Python ``str``.  Only the package-level ``decode`` name is part of
the supported API; everything else inside the submodules is internal and
may change between releases.

Supported escape syntax (this is the subset that real-world Pascal and
Delphi source code actually relies on):

* ``#<digits>`` — a decimal character code, e.g. ``#65`` -> ``"A"``.
* ``#$<hex>`` — a hexadecimal character code, e.g. ``#$41`` -> ``"A"``.
* ``#<multi>`` — consecutive ``#`` escapes may be chained *without* any
  separator, e.g. ``#65#66`` -> ``"AB"``.
* ``'<char>''<char>'`` — two single quotes inside a quoted segment are a
  literal single quote (Pascal's own quoting rule).

Delphi's newer named escapes (``#1234`` as a surrogate pair, ``\u0041``)
are intentionally NOT supported; they were never part of classic Pascal
and supporting them would require a separate parser.  If the input
contains an unsupported or malformed escape, ``ValueError`` is raised so
callers can distinguish a genuinely bad literal from an empty string.
"""

from __future__ import annotations

from .core import decode

__all__ = ["decode"]
