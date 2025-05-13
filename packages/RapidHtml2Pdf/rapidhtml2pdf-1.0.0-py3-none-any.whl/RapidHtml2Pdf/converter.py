from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import asyncio

@dataclass
class PDFOptions:
    page_size: str = "A4"
    orientation: str = "portrait"
    margins: Dict[str, float] = field(default_factory=lambda: {"top": 10, "bottom": 10, "left": 10, "right": 10})
    header_template: Optional[str] = None
    footer_template: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=lambda: {"title": "", "author": "", "keywords": ""})
    password: Optional[str] = None
    fit_to_one_page: bool = False

async def html_to_pdf_async(
html: str,
output_path: str,
options: Optional[PDFOptions] = None,
timeout: int = 30
) -> None:
    """
    Render HTML (with CSS/SCSS, assets, fonts) to PDF asynchronously.

    :param html: The HTML content or file path.
    :param output_path: Where to save the PDF.
    :param options: PDFOptions instance for page settings.
    :param timeout: Max seconds to wait for loading assets.
    """
    from h2p.renderer import Renderer

    opts = options or PDFOptions()
    renderer = Renderer(options=opts, timeout=timeout)
    await renderer.render(html, output_path)


def html_to_pdf(
    html: str,
    output_path: str,
    options: Optional[PDFOptions] = None,
    timeout: int = 30
) -> None:
    """
    Synchronous wrapper around html_to_pdf_async.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(html_to_pdf_async(html, output_path, options, timeout))

# Public API
__all__ = [
    "PDFOptions",
    "html_to_pdf",
    "html_to_pdf_async",
]
async def html_to_pdf_async(
    html: str,
    output_path: str,
    options: Optional[PDFOptions] = None,
    timeout: int = 30
) -> None:
    """
    Render HTML (with CSS/SCSS, assets, fonts) to PDF asynchronously.

    :param html: The HTML content or file path.
    :param output_path: Where to save the PDF.
    :param options: PDFOptions instance for page settings.
    :param timeout: Max seconds to wait for loading assets.
    """
    from RapidHtml2Pdf.renderer import Renderer

    opts = options or PDFOptions()
    renderer = Renderer(options=opts, timeout=timeout)
    await renderer.render(html, output_path)


def html_to_pdf(
    html: str,
    output_path: str,
    options: Optional[PDFOptions] = None,
    timeout: int = 30
) -> None:
    """
    Synchronous wrapper around html_to_pdf_async.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(html_to_pdf_async(html, output_path, options, timeout))

# Public API
__all__ = [
    "PDFOptions",
    "html_to_pdf",
    "html_to_pdf_async",
]