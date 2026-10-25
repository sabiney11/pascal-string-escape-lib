# pascal-string_escape_lib

Decodes Pascal and Delphi string literals containing decimal (`#65`), hex (`#$41`), and quote-doubling (`''`) escape sequences into Python `str` values.

## Usage

```python
from pascal_string_escape_lib import decode

assert decode("Hello") == "Hello"
assert decode("#65#66#67") == "ABC"
assert decode("#$41#$42") == "AB"
assert decode("it''s") == "it's"
assert decode("#8364") == "€"
```

## Why this exists

Classic Pascal (and Delphi) spell string-internal characters with `#<decimal>`, `#$<hex>`, and doubled single quotes for a literal quote. When ingesting old Pascal source into a Python toolchain, you need a decoder that understands exactly those rules. Supporting Unicode surrogate pairs (Delphi's `#$D800#$DC00`) was deliberately left out; it doubles the parser surface and the same job is done cleanly by decoding each `#$XXXX` escape and letting Python's `chr` handle scalar values. One interpretation, tested.

## Edge case you will hit

`decode` expects the *interior* of the literal — the bytes between the surrounding single quotes — not the quotes themselves. A lone `'` inside the input is an error, because in Pascal's own grammar a single `'` only appears as the first of a doubled pair. If your extractor gives you the full quoted literal, strip the outermost quotes before calling this.
