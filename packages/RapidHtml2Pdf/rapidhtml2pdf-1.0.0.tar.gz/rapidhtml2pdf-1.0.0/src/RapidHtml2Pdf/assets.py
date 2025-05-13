import aiohttp
import aiofiles
import os
import base64
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Optional
from .exceptions import AssetError

class AssetManager:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _fetch(self, url: str) -> bytes:
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with AssetManager()'.")
        try:
            async with self.session.get(url) as resp:
                resp.raise_for_status()
                return await resp.read()
        except Exception as e:
            raise AssetError(f"Failed to fetch asset {url}: {e}")

    async def _fetch_text(self, url: str) -> str:
        data = await self._fetch(url)
        return data.decode('utf-8')

    async def _load_html(self, html: str) -> str:
        if html is None:
            raise ValueError("HTML content cannot be None.")
        if os.path.exists(html):
            async with aiofiles.open(html, mode='r', encoding='utf-8') as f:
                return await f.read()
        return html

    async def _embed_base64(self, url: str, default_mime: str = "application/octet-stream") -> str:
        data = await self._fetch(url)
        ext = os.path.splitext(url)[1].lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".woff2": "font/woff2",
            ".woff": "font/woff",
            ".ttf": "font/ttf",
            ".eot": "application/vnd.ms-fontobject",
            ".svg": "image/svg+xml"
        }.get(ext, default_mime)
        encoded = base64.b64encode(data).decode('utf-8')
        return f"data:{mime};base64,{encoded}"

    async def _replace_css_urls(self, css: str, base_url: Optional[str] = None) -> str:
        async def replacer(match):
            raw_url = match.group(1).strip('\'"')
            if not raw_url.startswith("http"):
                if base_url:
                    raw_url = urljoin(base_url, raw_url)
                else:
                    return match.group(0)  # leave unchanged if no base URL
            try:
                embedded = await self._embed_base64(raw_url)
                return f"url('{embedded}')"
            except AssetError:
                return match.group(0)

        # Use an actual async loop since re.sub isn't awaitable
        pattern = re.compile(r"url\(([^)]+)\)")
        matches = list(pattern.finditer(css))
        new_css_parts = []
        last_index = 0
        for match in matches:
            new_css_parts.append(css[last_index:match.start()])
            new_css_parts.append(await replacer(match))
            last_index = match.end()
        new_css_parts.append(css[last_index:])
        return ''.join(new_css_parts)

    async def prepare(self, html: str) -> str:
        html_content = await self._load_html(html)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Inline external stylesheets
        for link_tag in soup.find_all("link", rel="stylesheet"):
            href = link_tag.get("href")
            if href and href.startswith("http"):
                try:
                    css_text = await self._fetch_text(href)
                    css_text = await self._replace_css_urls(css_text, href)
                    style_tag = soup.new_tag("style")
                    style_tag.string = css_text
                    link_tag.insert_after(style_tag)
                    link_tag.decompose()
                except AssetError:
                    continue  # skip broken CSS links

        # Replace images
        for img in soup.find_all("img"):
            src = img.get("src")
            if src and src.startswith("http"):
                try:
                    img["src"] = await self._embed_base64(src, "image/png")
                except AssetError:
                    continue

        # Replace inline style urls
        for style_tag in soup.find_all("style"):
            css = style_tag.string
            if css:
                new_css = await self._replace_css_urls(css)
                style_tag.string.replace_with(new_css)

        return str(soup)
