# API Reference

## Image Processing Module

### `process_image(image_path: str) -> dict`
Processes an image and returns metadata.

**Parameters:**
- `image_path` (str): Path to the image file

**Returns:**
```json
{
    "dimensions": {"width": int, "height": int},
    "format": str,
    "size_kb": float
}
```

## Caption Generation

### `generate_caption(image_metadata: dict) -> str`
Generates a caption for the given image metadata.

**Parameters:**
- `image_metadata` (dict): Metadata from process_image()

**Returns:**
- str: Generated caption

---
*Note: This is a template. Update with your actual API details.*
