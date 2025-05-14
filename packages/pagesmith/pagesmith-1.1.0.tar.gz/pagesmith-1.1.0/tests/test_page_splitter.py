import re

import allure
import pytest
from pagesmith.page_splitter import PageSplitter


@pytest.fixture
def mock_page_splitter():
    yield from mock_book_plain_text(30)


@pytest.fixture
def mock_page100_splitter():
    yield from mock_book_plain_text(100)


@pytest.fixture(
    scope="function",
    params=[
        "\n\nCHAPTER VII.\nA Mad Tea-Party\n\n",
        "\n\nCHAPTER I\n\n",
        "\n\nCHAPTER Two\n\n",
        "\n\nCHAPTER Third\n\n",
        "\n\nCHAPTER four. FALL\n\n",
        "\n\nCHAPTER twenty two. WINTER\n\n",
        "\n\nCHAPTER last inline\nunderline\n\n",
        "\n\nI. A SCANDAL IN BOHEMIA\n \n",
        "\n\nV.\nПет наранчиних сjеменки\n\n",
    ],
)
def chapter_pattern(request):
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        "\ncorrespondent could be.\n\n",
    ],
)
def wrong_chapter_pattern(request):
    return request.param


def normalize(text: str) -> str:
    """Make later processing more simple."""
    # if self.escape_html:
    #     text = escape(text)
    text = re.sub(r"(\r?\n|\u2028|\u2029)", " <br/> ", text)
    text = re.sub(r"\r", "", text)
    return re.sub(r"[ \t]+", " ", text)


def mock_book_plain_text(page_length: int):
    original_target = PageSplitter.PAGE_LENGTH_TARGET
    set_book_page_length(page_length)
    yield
    set_book_page_length(original_target)


def set_book_page_length(page_length):
    PageSplitter.PAGE_LENGTH_TARGET = page_length  # Mocked target length for testing
    PageSplitter.PAGE_LENGTH_ERROR_TOLERANCE = 0.5
    PageSplitter.PAGE_MIN_LENGTH = int(
        PageSplitter.PAGE_LENGTH_TARGET * (1 - PageSplitter.PAGE_LENGTH_ERROR_TOLERANCE)
    )
    PageSplitter.PAGE_MAX_LENGTH = int(
        PageSplitter.PAGE_LENGTH_TARGET * (1 + PageSplitter.PAGE_LENGTH_ERROR_TOLERANCE)
    )


@allure.epic("Page splitter")
def test_paragraph_end_priority(mock_page_splitter):
    # Paragraph end is within 25% error margin but farther than sentence end
    text = (
        "a" * 25 + ".  " + "b" * 5 + "\n\n" + "a" * 22 + "\r\n\t\r\n" + "b" * 3 + ". \r" + "a" * 10
    )
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 3
    assert "a" * 25 + ".  " + "b" * 5 == pages[0]
    assert "\n\n" + "a" * 22 == pages[1]
    assert "\r\n\t\r\n" + "b" * 3 + ". \r" + "a" * 10 == pages[2]


@allure.epic("Page splitter")
def test_sentence_end_priority(mock_page_splitter):
    # Sentence end near farther than word end
    text = "a" * 29 + " aaa" + ". " + "b" * 5 + " next  sentence.\n"
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2
    assert "a" * 29 + " aaa" + ". " == pages[0]

    # now no sentence - will split nearer to target by words
    text = "a" * 29 + " aaa" + "  " + "b" * 5 + " next  sentence.\n"
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2
    assert "a" * 29 == pages[0]


@allure.epic("Page splitter")
def test_word_end_priority(mock_page_splitter):
    # No paragraph or sentence end, splitting by word
    text = "A long text without special ends here"
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2


@allure.epic("Page splitter")
def test_no_special_end(mock_page_splitter):
    # A long string without any special end
    text = "a" * 60
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2
    len(pages[0]) == 30


# @allure.epic("Page splitter")
# def test_chapter_pattern(mock_page100_splitter, chapter_pattern):
#     splitter = PageSplitter(f"aa{chapter_pattern}34")
#     pages = list(splitter.pages())
#     assert len(splitter.toc) == 1, f"chapter_pattern: {chapter_pattern}"
#     assert splitter.toc[0] == (chapter_pattern.replace("\n", "   ").strip(), 1, 2)


@allure.epic("Page splitter")
def test_wrong_chapter_pattern(mock_page_splitter, wrong_chapter_pattern):
    splitter = PageSplitter(f"aa{wrong_chapter_pattern}34")
    list(splitter.pages())
    assert len(splitter.toc) == 0, f"chapter_pattern: {wrong_chapter_pattern}"


@allure.epic("Page splitter")
def test_pages_shift_if_heading(mock_page_splitter):
    chapter_pattern = "\n\nCHAPTER VII.\n\n"
    splitter = PageSplitter("a" * 16 + chapter_pattern + " " + "aaa")
    pages = list(splitter.pages())
    assert len(pages) == 3
    assert pages[0] == "a" * 16

    splitter = PageSplitter("a" * 16 + "\n123 aaaaaaaa\n" + "aaa")
    pages = list(splitter.pages())
    assert len(pages) == 2
    assert pages[0] == "a" * 16 + "\n"
    assert pages[1] == "123 aaaaaaaa\naaa"

    splitter = PageSplitter("a" * 20 + "aa\n\n" + "d" * 21 + "\n\n34")
    pages = list(splitter.pages())
    assert len(pages) == 3
    assert pages[0] == "a" * 20 + "aa"


# @allure.epic("Page splitter")
# def test_split_inside_p_tag(mock_page_splitter):
#     # Text contains a long paragraph that should be split inside the <p> tag
#     text = "<p>" + "a" * 60 + "</p>" + "b" * 30
#     splitter = PageSplitter(text)
#     pages = list(splitter.pages())
#
#     # Assert that the split is inside the <p> tag
#     print(pages)
#     assert len(pages) == 3
#     assert pages[0].endswith("&lt;/p&gt;")  # we escape tags when import plain text
#     assert pages[1].startswith("&lt;p&gt;")
