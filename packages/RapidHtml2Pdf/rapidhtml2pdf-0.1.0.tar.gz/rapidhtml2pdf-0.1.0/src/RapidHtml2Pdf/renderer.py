import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from dataclasses import asdict
from typing import Optional
from .converter import PDFOptions
from .assets import AssetManager
from .exceptions import RenderError

class Renderer:
    def __init__(self, options: PDFOptions, timeout: int = 30):
        self.options = options
        self.timeout = timeout * 1000  # milliseconds

    async def render(self, html: str, output_path: str) -> None:
        if not isinstance(html, str):
            raise RenderError("HTML content must be a string.")

        async with AssetManager() as asset_manager:
            html_content = await asset_manager.prepare(html)

        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch()
                context = await browser.new_context()
                page = await context.new_page()

                await page.set_content(html_content, timeout=self.timeout)
                await page.wait_for_load_state("networkidle", timeout=self.timeout)

                if self.options.fit_to_one_page:
                    # Measure content height (in pixels)
                    content_height = await page.evaluate("document.body.scrollHeight")

                    # A4 height at 96 DPI = ~1122px
                    a4_height_px = 1122
                    a4_width_in = 8.27

                    if content_height <= a4_height_px:
                        # Dynamically fit to content height to avoid blank pages
                        await page.pdf(
                            path=output_path,
                            width=f"{a4_width_in}in",
                            height=f"{content_height}px",
                            print_background=True,
                            margin={"top": "0in", "bottom": "0in", "left": "0in", "right": "0in"},
                        )
                    else:
                        # Generate multi-page PDF normally
                        pdf_opts = self._build_pdf_options()
                        await page.pdf(path=output_path, **pdf_opts)
                else:
                    pdf_opts = self._build_pdf_options()
                    await page.pdf(path=output_path, **pdf_opts)

                await browser.close()
        except PlaywrightTimeoutError as e:
            raise RenderError(f"Timeout rendering page: {e}")
        except Exception as e:
            raise RenderError(f"Error during render: {e}")

    def _build_pdf_options(self) -> dict:
        opts = asdict(self.options)

        # Convert margins to strings like '10mm'
        margin_values = opts.pop("margins", {})
        margin_dict = {k: f"{v}mm" for k, v in margin_values.items()}

        pdf_opts = {
            "print_background": True,
            "margin": margin_dict,
            "format": opts.pop("page_size", "A4"),
        }

        if opts.pop("orientation", "portrait") == "landscape":
            pdf_opts["landscape"] = True

        if opts.get("header_template") or opts.get("footer_template"):
            pdf_opts["display_header_footer"] = True
            if opts["header_template"]:
                pdf_opts["header_template"] = opts["header_template"]
            if opts["footer_template"]:
                pdf_opts["footer_template"] = opts["footer_template"]

        return pdf_opts