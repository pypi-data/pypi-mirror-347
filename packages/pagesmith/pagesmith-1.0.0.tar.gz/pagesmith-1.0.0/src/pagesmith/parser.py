import io
import re
from typing import Optional

from lxml import etree, html
from lxml.html import tostring


def parse_partial_html(input_html: str) -> Optional[etree.Element]:  # noqa
    """Parse string with HTML fragment into an lxml tree.

    Supports partial HTML content.
    Removes comments.
    """
    # Simple heuristic to detect unclosed comments
    open_count = input_html.count("<!--")
    close_count = input_html.count("-->")

    # If counts don't match, escape all opening comment tags
    if open_count != close_count:
        input_html = input_html.replace("<!--", "&lt;!--")

    # Normalize new lines to spaces for consistent handling
    input_html = re.sub(r"[\n\r]+", " ", input_html)

    # Remove CDATA sections
    input_html = re.sub(r"<!\[CDATA\[.*?]]>", "", input_html, flags=re.DOTALL)

    parser = etree.HTMLParser(recover=True, remove_comments=True, remove_pis=True)
    tree = html.parse(io.StringIO(input_html), parser=parser)
    return tree.getroot()


def etree_to_str(root: etree.Element) -> str:
    if root.tag in ["root", "html", "body"]:
        # If it's our artificial root, only return its contents
        result = root.text if root.text else ""
        for child in root:
            result += tostring(child, encoding="unicode", method="html")
        return result
    return tostring(root, encoding="unicode", method="html")  # type: ignore[no-any-return]
