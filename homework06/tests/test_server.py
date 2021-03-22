from boddle import boddle
import pytest
from hackernews import server
from pathlib import Path


def test_display_main_page():
    with open(Path("../hackernews/templates/main_menu.tpl")) as f:
        html = f.read()
    # assert server.main_page() == html
    pass
