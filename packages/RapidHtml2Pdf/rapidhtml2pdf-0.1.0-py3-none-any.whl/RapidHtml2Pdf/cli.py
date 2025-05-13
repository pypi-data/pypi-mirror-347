import sys
import asyncio
import typer
from .converter import html_to_pdf_async, html_to_pdf, PDFOptions
from .exceptions import ConfigurationError

def main(
    input: str = typer.Argument(..., help="Input HTML file or string."),
    output: str = typer.Argument(..., help="Output PDF file path."),
    page_size: str = typer.Option("A4", help="Page size (e.g., A4, Letter)."),
    orientation: str = typer.Option("portrait", help="Orientation: portrait or landscape."),
    margin_top: float = typer.Option(10.0, help="Top margin in mm."),
    margin_bottom: float = typer.Option(10.0, help="Bottom margin in mm."),
    margin_left: float = typer.Option(10.0, help="Left margin in mm."),
    margin_right: float = typer.Option(10.0, help="Right margin in mm."),
    header: str = typer.Option(None, help="HTML template for header."),
    footer: str = typer.Option(None, help="HTML template for footer."),
    title: str = typer.Option(None, help="PDF metadata title."),
    author: str = typer.Option(None, help="PDF metadata author."),
    keywords: str = typer.Option(None, help="PDF metadata keywords."),
    password: str = typer.Option(None, help="Password to encrypt the PDF."),
    async_mode: bool = typer.Option(False, help="Use asynchronous rendering."),
):
    """Convert HTML to PDF with h2p."""
    # Validate orientation
    if orientation not in ("portrait", "landscape"):
        raise ConfigurationError(f"Invalid orientation: {orientation}")

    options = PDFOptions(
        page_size=page_size,
        orientation=orientation,
        margins={
            "top": margin_top,
            "bottom": margin_bottom,
            "left": margin_left,
            "right": margin_right,
        },
        header_template=header,
        footer_template=footer,
        metadata={
            "title": title or "",
            "author": author or "",
            "keywords": keywords or "",
        },
        password=password,
    )

    try:
        if async_mode:
            asyncio.run(html_to_pdf_async(input, output, options))
        else:
            html_to_pdf(input, output, options)
        typer.secho(f"Successfully generated PDF: {output}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        sys.exit(1)

if __name__ == "__main__":
    typer.run(main)
