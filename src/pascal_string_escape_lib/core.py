from __future__ import annotations


def decode(literal: str) -> str:
    """Decode a Pascal/Delphi string literal body into a Python string.

    ``literal`` is the *interior* of the Pascal string — i.e. the
    characters that would appear between the surrounding single quotes.
    Feeding the quotes themselves is incorrect; they are the container,
    not the contents, and keeping them out of the parser lets callers
    extract the interior however they like (regex, slicing, hand-parsing)
    without this function second-guessing them.

    Returns the decoded ``str``.  Raises ``ValueError`` for malformed
    escapes (a ``#`` not followed by a digit or ``$``+hex-digit, or a
    dangling lone ``#`` at end of input).  Empty input returns ``""``.
    """
    out: list[str] = []
    i = 0
    n = len(literal)
    while i < n:
        ch = literal[i]
        if ch == "#":
            i += 1
            if i >= n:
                raise ValueError("dangling '#' at end of literal")
            if literal[i] == "$":
                i += 1
                start = i
                while i < n and literal[i] in "0123456789abcdefABCDEF":
                    i += 1
                hex_digits = literal[start:i]
                if len(hex_digits) == 0:
                    raise ValueError("'#$' not followed by hex digits")
                code = int(hex_digits, 16)
            else:
                start = i
                while i < n and literal[i] in "0123456789":
                    i += 1
                digits = literal[start:i]
                if len(digits) == 0:
                    raise ValueError("'#' not followed by a decimal or '$'")
                code = int(digits, 10)
            out.append(chr(code))
        elif ch == "'":
            # Pascal doubles a single quote to represent a literal quote
            # inside a string.  Because this function receives the
            # *interior*, an isolated quote here must be the doubled form.
            if i + 1 >= n or literal[i + 1] != "'":
                raise ValueError("lone single quote in literal interior")
            out.append("'")
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)
