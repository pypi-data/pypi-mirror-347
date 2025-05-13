from __future__ import annotations

import pytest

# from mkconvert.html_to_md.htmd_converter import HtmdConverter
from mkconvert.html_to_md.markdownify_converter import MarkdownifyConverter


TEST = """
<table>
<tr>
<th></th>
<th>Lorem ipsum</th>
<th>Lorem ipsum</th>
<th>Lorem ipsum</th>
</tr>
<tr>
<td>1</td>
<td>In eleifend velit vitae libero sollicitudin euismod.</td>
<td>Lorem</td>
<td></td>
</tr>
<tr>
<td>2</td>
<td>Cras fringilla ipsum magna, in fringilla dui commodo a.</td>
<td>Ipsum</td>
<td></td>
</tr>
<tr>
<td>3</td>
<td>Aliquam erat volutpat.</td>
<td>Lorem</td>
<td></td>
</tr>
<tr>
<td>4</td>
<td>Fusce vitae vestibulum velit.</td>
<td>Lorem</td>
<td></td>
</tr>
<tr>
<td>5</td>
<td>Etiam vehicula luctus fermentum.</td>
<td>Ipsum</td>
<td></td>
</tr>
</table>
"""


# def test_htmd():
#     converter = HtmdConverter()
#     result = converter.convert(TEST)
#     print(result)


def test_markdownify():
    converter = MarkdownifyConverter()
    result = converter.convert(TEST)
    assert "|" in result
    # print(result)


if __name__ == "__main__":
    pytest.main([__file__, "-vv", "-s"])
