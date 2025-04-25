from pdf2image import convert_from_bytes
from PIL import Image
import subprocess
import base64
import io
import tempfile
import os


class GenImage():
    def __init__(self, bytes: bytes, file_format: str):
        self.buffer = io.BytesIO()
        converter = getattr(self, file_format.lower(), lambda bytes: self.not_support(file_format))
        converter(bytes)

    def not_support(self, file_format: str):
        raise Exception(f"Not support this file format {file_format}")

    def pptx(self, pptx_bytes):
        with tempfile.TemporaryDirectory() as tmpdir:
            pptx_path = os.path.join(tmpdir, "presentation.pptx")
            pdf_path = os.path.join(tmpdir, "presentation.pdf")

            with open(pptx_path, "wb") as f:
                f.write(pptx_bytes)

            subprocess.run([
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", tmpdir,
                pptx_path
            ], check=True)

            os.remove(pptx_path)

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            
            os.remove(pdf_path)

            self.pdf(pdf_bytes)

    def pdf(self, pdf_bytes: bytes):
        images = convert_from_bytes(pdf_bytes)
        sum_width = sum([img.width for img in images])
        max_height = max([img.height for img in images])
        self.img = Image.new("RGB", (sum_width, max_height), color=(255, 255, 255))
        x_offset = 0
        for img in images:
            self.img.paste(img, (x_offset, 0))
            x_offset += img.width
        self.img.save(self.buffer, "jpeg")

    def base64(self):
        return base64.b64encode(self.buffer.getvalue())
    

def convert_to_img(file: bytes, format: str) -> GenImage:
    return GenImage(file, format)