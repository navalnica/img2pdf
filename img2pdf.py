from pathlib import Path
from datetime import datetime
import argparse
import sys
from PIL import Image
import pillow_heif

# Enable HEIC support
pillow_heif.register_heif_opener()


SUPPORTED_EXTS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".heif",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
}


def images_to_pdf(image_paths: list[str], output_path: Path):
    images = []

    for p in image_paths:
        path = Path(p)

        if not path.exists():
            print(f"Skipping missing file: {path}")
            continue

        if path.suffix.lower() not in SUPPORTED_EXTS:
            print(f"Skipping unsupported format: {path}")
            continue

        img = Image.open(path)

        # Convert to RGB for PDF compatibility
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        images.append(img)

    if not images:
        raise ValueError("No valid images to convert.")

    # Use first image size as canonical page size (pixels)
    base_width, base_height = images[0].size

    # Normalize images so that pdf pages have same width
    normalized = []
    for img in images:
        if img.size != (base_width, base_height):
            img = img.resize((base_width, base_height), Image.Resampling.LANCZOS)
        normalized.append(img)

    normalized[0].save(
        output_path,
        save_all=True,
        append_images=normalized[1:],
        resolution=300.0,  # enforce consistent DPI
    )


def resolve_output_path(output_arg: str | None) -> Path:
    now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = Path(output_arg) if output_arg else Path(f"{now_str}.pdf")

    if path.suffix.lower() != ".pdf":
        path = path.with_suffix(".pdf")

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        path = path.with_stem(f"{path.stem}_{now_str}")

    return path


def main():
    parser = argparse.ArgumentParser(
        description="Convert multiple images (JPG, PNG, HEIC, etc.) to a single PDF."
    )

    parser.add_argument("images", nargs="+")
    parser.add_argument("-o", "--output", default=None)

    args = parser.parse_args()

    out_path = resolve_output_path(args.output)

    print(f"saving to {out_path}")

    try:
        images_to_pdf(args.images, out_path)
        print("done")
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
