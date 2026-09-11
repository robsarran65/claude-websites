"""Generate print and screen QR assets for the permanent Connect URL."""

from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.barcode.qrencoder import QRErrorCorrectLevel


URL = "https://www.sarranai.com/connect"
QUIET_ZONE = 4
MODULE_SIZE = 40
INK = "#05101F"
PAPER = "#FFFFFF"


def matrix_for(value: str) -> list[list[bool]]:
    widget = QrCodeWidget(value)
    widget.qr.errorCorrectLevel = QRErrorCorrectLevel.H
    widget.qr.make()
    return [[bool(cell) for cell in row] for row in widget.qr.modules]


def write_png(matrix: list[list[bool]], destination: Path) -> None:
    modules = len(matrix)
    size = (modules + QUIET_ZONE * 2) * MODULE_SIZE
    image = Image.new("RGB", (size, size), PAPER)
    draw = ImageDraw.Draw(image)
    for row, values in enumerate(matrix):
        for column, filled in enumerate(values):
            if not filled:
                continue
            left = (column + QUIET_ZONE) * MODULE_SIZE
            top = (row + QUIET_ZONE) * MODULE_SIZE
            draw.rectangle(
                (left, top, left + MODULE_SIZE - 1, top + MODULE_SIZE - 1),
                fill=INK,
            )
    image.save(destination, format="PNG", optimize=True)


def write_svg(matrix: list[list[bool]], destination: Path) -> None:
    modules = len(matrix)
    size = modules + QUIET_ZONE * 2
    squares = []
    for row, values in enumerate(matrix):
        for column, filled in enumerate(values):
            if filled:
                squares.append(
                    f'<rect x="{column + QUIET_ZONE}" y="{row + QUIET_ZONE}" width="1" height="1"/>'
                )
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        'shape-rendering="crispEdges" role="img" aria-labelledby="title desc">\n'
        '  <title id="title">Sarran AI Connect QR code</title>\n'
        f'  <desc id="desc">Open {URL}</desc>\n'
        f'  <rect width="{size}" height="{size}" fill="{PAPER}"/>\n'
        f'  <g fill="{INK}">{"".join(squares)}</g>\n'
        '</svg>\n'
    )
    destination.write_text(svg, encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    assets = project_root / "assets"
    matrix = matrix_for(URL)
    write_png(matrix, assets / "sarran-ai-connect-qr.png")
    write_svg(matrix, assets / "sarran-ai-connect-qr.svg")
    print(f"Generated {len(matrix)}x{len(matrix)} QR matrix for {URL}")


if __name__ == "__main__":
    main()
