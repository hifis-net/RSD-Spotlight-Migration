# HTML Parser from
# https://gitlab.hzdr.de/hub-terra/stakeholder-view/-/blob/dev/datahub/stakeholderview/migrations/0015_html_to_md.py

from html.parser import HTMLParser
from tkinter import Image
from typing import List


class MdContent:
    """Collect markdown snippets and allow to print the full document."""

    def __init__(self):
        self.content = []

    def __getitem__(self, key) -> any:
        return self.content[key]

    def append(self, data) -> None:
        self.content.append(data)

    def to_markdown(self) -> str:
        return "".join(map(str, self.content))


class MdLink:
    """Class for links"""

    def __init__(self, attrs: List) -> None:
        self.href = ""
        self.text = ""
        self.data_id = ""
        self.is_id_link = False
        for key, value in attrs:
            if key == "href":
                self.href = value
            if key == "id":
                self.is_id_link = True
                self.data_id = value

    def text(self, text: str) -> None:
        self.text = text.strip()

    def __str__(self) -> str:
        if self.is_id_link:
            return f"[{self.text}]{{{self.data_id}}}"
        return f"[{self.text}]({self.href})"


class ImageSrcProcessor:
    def __init__(self, src: str) -> None:
        replacement = r'https://hifis.net/assets/img/'
        match = r'{{ site.directory.images | relative_url}}'
        if src.startswith(match):
            self.src = src.replace(match, replacement)
        else:
            self.src = src

    def convert(self):
        return self.src


class MdImage:
    """Class for images"""
    def __init__(self, attrs: List) -> None:
        self.alt = ""
        self.src = ""
        for key, value in attrs:
            if key == "alt":
                self.alt = value
            if key == "src":
                self.src = ImageSrcProcessor(value).convert()

    def __str__(self) -> str:
        return f"![{self.alt}]({self.src})"


class SvHtmlParser(HTMLParser):
    """Parses HTML to Markdown"""

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.inside_a = False
        self.inside_div = False
        self.inside_span = False
        self.inside_tt = False
        self.inside_icon = False
        self.inside_italic = False
        self.output = MdContent()

    def close(self) -> MdContent:
        super().close()
        return self.output

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!-- {data.strip()} -->")

    def handle_data(self, data: str) -> None:
        if self.inside_a:
            self.output[-1].text = data
        elif self.inside_div and data.isspace():
            # Do not parse indentation
            return
        elif self.inside_icon:
            return
        else:
            self.output.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self.inside_a = False
        elif tag == "b":
            self.output.append(r"**")
        elif tag == "div":
            self.inside_div = False
        elif tag == "span":
            self.inside_span = False
        elif tag == "tt":
            self.output.append(r"`")
            self.inside_tt = False
        elif tag == "i":
            if self.inside_italic:
                self.output.append(r"*")
                self.inside_italic = False
            else:
                self.inside_icon = False

    def handle_starttag(self, tag: str, attrs: List) -> None:
        if tag == "a":
            self.inside_a = True
            self.output.append(MdLink(attrs))
        elif tag == "b":
            self.output.append(r"**")
        elif tag == "br":
            self.output.append("<br>")
        elif tag == "p":
            self.output.append("\n\n")
        elif tag == "div":
            self.inside_div = True
        elif tag == "img":
            self.output.append(MdImage(attrs))
        elif tag == "span":
            self.inside_span = True
        elif tag == "tt":
            self.inside_tt = True
            self.output.append(r"`")
        elif tag == "i":
            if len(attrs) > 0:
                # We are in an icon, skip this
                self.inside_icon = True
                return
            else:
                self.inside_italic = True
                self.output.append(r"*")
        elif tag == "iframe" or tag == "centered" or tag == "center" or tag == "video":
            return
        else:
            raise NotImplementedError(
                f"{tag} tags are not implemented.\n\n" f"Last output: {self.output[-1]}"
            )
