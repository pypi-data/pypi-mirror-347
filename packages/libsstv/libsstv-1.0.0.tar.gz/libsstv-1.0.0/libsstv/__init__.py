from pysstv.color import ScottieS2 # pysstv[pil]
from PIL import Image # pillow
import sstv_decoder # file

encoding_engine = ScottieS2

def encode(image_file: str, output_file: str):
    image = Image.open(image_file).convert("RGB")
    image = image.resize((320, 256))
    encoder = encoding_engine(image, 44110, 16)
    with open(output_file, "wb") as output:
        encoder.write_wav(output)

def decode(input_file: str, output_image: str):
    with open(input_file, "rb") as inp:
        decoder = sstv_decoder.SSTVDecoder(inp)
        out = decoder.decode()
        out.save(output_image)