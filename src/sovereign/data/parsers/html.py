from __future__ import annotations

from bs4 import BeautifulSoup

from sovereign.data.core.parsed_content import ParsedContent
from sovereign.data.core.resource import RawResource

from .base import BaseParser


class HTMLParser(BaseParser):

    def parse(
        self,
        resource: RawResource,
    ) -> ParsedContent:

        soup = BeautifulSoup(
            resource.content,
            "lxml",
        )

        title = None

        if soup.title:
            title = soup.title.text.strip()

        headings = []

        for tag in soup.find_all(
            ["h1", "h2", "h3", "h4"]
        ):
            headings.append(tag.get_text(strip=True))

        links = []

        for tag in soup.find_all("a", href=True):
            links.append(tag["href"])

        images = []

        for img in soup.find_all("img", src=True):
            images.append(img["src"])

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        return ParsedContent(
            text=text,
            title=title,
            headings=headings,
            images=images,
            links=links,
            parser_name="HTMLParser",
        )