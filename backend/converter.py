from pdf2image import convert_from_bytes
from PIL import Image
import subprocess
import base64
import io
import tempfile
import os


class GenImage():
    '''
    Class for working with a presentation in the form of an image

    Attributes
    ----------
    buffer: io.BytesIO
        buffer into which the image is loaded upon successful conversion
    
    Methods
    -------
    pptx(pptx_bytes:bytes):
        Convert pptx to jpeg
    pdf(pdf_bytes: bytes):
        Convert pdf to jpeg
    base64() -> bytes:
        Get base64 bytes from buffer

    '''
    def __init__(self, bytes: bytes, file_format: str):
        '''
        Creates an image from the resulting byte array 
        '''
        self.buffer = io.BytesIO()
        # Automatically calling the converter, if the type is not supported, we throw an exception
        converter = getattr(self, file_format.lower(), lambda bytes: self.not_support(file_format))
        converter(bytes)

    def not_support(self, file_format: str):
        raise Exception(f"Not support this file format {file_format}")

    # It is automatically invoked if necessary
    def pptx(self, pptx_bytes):
        '''
        Convert pptx to jpeg

        Parameters
        ----------
            pptx_bytes: bytes
                An array of bytes that may contain a pptx
        '''
        with tempfile.TemporaryDirectory() as tmpdir:
            pptx_path = os.path.join(tmpdir, "presentation.pptx")
            pdf_path = os.path.join(tmpdir, "presentation.pdf")

            with open(pptx_path, "wb") as f:
                f.write(pptx_bytes)

            # Run libreoffice for convert pptx to pdf
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

            # Run converter pdf to img
            self.pdf(pdf_bytes)

    # It is automatically invoked if necessary
    def pdf(self, pdf_bytes: bytes):
        '''
        Convert pdf to jpeg

        Parameters
        ----------
            pdf_bytes: bytes
                An array of bytes that may contain a pdf
        '''
        images = convert_from_bytes(pdf_bytes)
        sum_width = sum([img.width for img in images])
        max_height = max([img.height for img in images])
        # Create empty image for pasting
        self.img = Image.new("RGB", (sum_width, max_height), color=(255, 255, 255))
        x_offset = 0
        # Construction all the slides into one picture
        for img in images:
            self.img.paste(img, (x_offset, 0))
            x_offset += img.width
        self.img.save(self.buffer, "jpeg")

    def base64(self):
        '''
        Get base64 bytes from buffer
        '''
        return base64.b64encode(self.buffer.getvalue())
    
# For future changes towards safe conversion
def convert_to_img(file: bytes, format: str) -> GenImage:
    '''
    Function of converting a presentation into an image

    Parameters
    ----------
        file: bytes
            file to be converted, in bytes
        format: str
            format/type of file that needs to be converted
    '''
    return GenImage(file, format)