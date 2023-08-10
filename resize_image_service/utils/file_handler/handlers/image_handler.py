from PIL import Image

import io


def image_handler(file_bytes: io.BytesIO) -> io.BytesIO:
    img = Image.open(file_bytes)

    img.thumbnail((320, 320))

    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)

    new_byte_img = io.BytesIO()
    img.save(new_byte_img, format="PNG")

    new_byte_img.seek(0)

    return new_byte_img
