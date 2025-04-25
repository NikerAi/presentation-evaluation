import pytest
from io import BytesIO
from backend.converter import GenImage
from PIL import Image
import base64
from pptx import Presentation
from pptx.util import Inches
import tempfile
import os

def create_simple_presentation(output_path):
    '''
    Create simple presentation for tests
    '''
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = "Тестовая презентация"
    slide.placeholders[1].text = "Создано для теста GenImage"
    prs.save(output_path)

@pytest.fixture
def sample_pptx_bytes():
    '''
    Get bytes from simple pptx 
    '''
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=True) as tmp:
        create_simple_presentation(tmp.name)
        tmp.seek(0)
        data = tmp.read()
    return data

def test_pptx_conversion(sample_pptx_bytes):
    '''
    Checking that the buffer contains an image
    '''
    gi = GenImage(sample_pptx_bytes, "pptx")
    img = Image.open(gi.buffer)
    assert img.format == "JPEG"
    assert img.size[0] > 0 and img.size[1] > 0


def test_base64_output(sample_pptx_bytes):
    '''
    Checking that the base64 bytes contain a picture
    '''
    gi = GenImage(sample_pptx_bytes, "pptx")
    b64 = gi.base64()
    assert isinstance(b64, bytes)
    decoded = base64.b64decode(b64)
    # Check JPEG magic bytes
    assert decoded[:2] == b'\xff\xd8'

def test_unsupported_format():
    '''
    Checking the reaction to an unsupported format
    '''
    with pytest.raises(Exception) as exc:
        GenImage(BytesIO(b"dummy").getvalue(), "txt")
    assert "Not support this file format txt" in str(exc.value)
