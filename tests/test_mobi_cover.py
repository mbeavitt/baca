import os
import tempfile
import shutil
from baca.tools.KindleUnpack.mobi_cover import get_image_type, get_image_size


def test_mobi_file_cover_extraction():
    """Test that we can extract and identify cover image from a real mobi file"""
    # Use test fixture from repo
    test_dir = os.path.dirname(os.path.abspath(__file__))
    mobi_file = os.path.join(test_dir, "fixtures", "room-with-a-view-gutenberg.mobi")

    # Skip test if the mobi file doesn't exist
    if not os.path.exists(mobi_file):
        import pytest
        pytest.skip(f"Test mobi file not found: {mobi_file}")

    # Extract the mobi file to a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Use kindleunpack to extract the mobi
        from baca.tools.KindleUnpack.kindleunpack import unpackBook

        # Extract the mobi file
        unpackBook(mobi_file, temp_dir)

        # Look for image files in the extracted directory
        image_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    image_files.append(os.path.join(root, file))

        # Verify that we found at least one image
        assert len(image_files) > 0, "No images found in extracted mobi file"

        # Test get_image_type on each image found
        for img_path in image_files:
            img_type = get_image_type(img_path)
            assert img_type is not None, f"Could not determine type for {img_path}"
            assert img_type in ['jpg', 'jpeg', 'png', 'gif'], f"Unexpected image type: {img_type}"

            # Test get_image_size on each image
            size = get_image_size(img_path)
            if size is not None:
                width, height = size
                assert width > 0, f"Invalid width for {img_path}"
                assert height > 0, f"Invalid height for {img_path}"

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
