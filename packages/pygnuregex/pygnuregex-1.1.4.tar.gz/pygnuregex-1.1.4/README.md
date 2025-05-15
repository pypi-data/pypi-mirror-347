# Pygnuregex, GNU regex for Python

Pygnuregex is a Python package for the GNU interface of regex functions in `<regex.h>`. The GNU interface provides a wide range of different syntaxes for the regex compiler. This package **requires** GNU libc to work properly; prefer the sdist if you're worried about ABI compatibility.

## Example

```python
import pygnuregex

# Search for the first match
p = pygnuregex.compile(b"f\\(oo\\)[0-9]+")
result = p.search(b"hello foo123!") # ==> 6
p.span() # ==> [(6, 12), (7, 9)]

# All matches
p = pygnuregex.compile(b"\\(foo\\|bar\\)[0-9]+")
list(p.finditer(b"hello foo123 and bar456!"))
# ==> [[(6, 12), (6, 9)],[(17, 23), (17, 20)]]
```

The `SyntaxFlag` enum contains all the available syntax options that may be set in `pygnuregex.compile()`.
