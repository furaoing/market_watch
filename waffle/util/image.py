# -*- coding: utf-8 -*-

import base64

"""
python3.4+ only
"""


def b64File_to_imgFile(b64_str_pth, dst_pth):
    with open(b64_str_pth, "r") as f:
        MIME_b64_str = f.read()
        # read b64 str from file ("file" to "str")

        MIME_b64_byte = bytes(MIME_b64_str, encoding="utf-8")
        # convert a b64 str into a b64 byte ("str" to "byte")

        raw_byte = base64.decodebytes(MIME_b64_byte)
        # convert a b64 byte into a raw byte ("byte" to "byte), per RFC 2045 / MIME

        with open(dst_pth, "wb") as g:
            g.write(raw_byte)


def b64Str_to_imgFile(MIME_b64_str, dst_pth):

    MIME_b64_byte = bytes(MIME_b64_str, encoding="utf-8")
    # convert a b64 str into a b64 byte ("str" to "byte")

    raw_byte = base64.decodebytes(MIME_b64_byte)
    # convert a b64 byte into a raw byte ("byte" to "byte), per RFC 2045 / MIME

    with open(dst_pth, "wb") as g:
        g.write(raw_byte)


def imgFile_to_b64File(src_pth, b64_str_pth):
    with open(src_pth, "rb") as f:
        raw_byte = f.read()
        # read raw byte from src, "file" to "byte"

        MIME_b64_byte = base64.encodebytes(raw_byte)
        # convert raw byte into b64 byte , "byte" to "byte", per RFC 2045 / MIME

        MIME_b64_str = MIME_b64_byte.decode(encoding="utf-8")
        # decode b64 byte into str, "byte" to "str"

        with open(b64_str_pth, "w") as g:
            g.write(MIME_b64_str)


def imgByte_to_b64File(raw_byte, b64_str_pth):

    MIME_b64_byte = base64.encodebytes(raw_byte)
    # convert raw byte into b64 byte , "byte" to "byte", per RFC 2045 / MIME

    MIME_b64_str = MIME_b64_byte.decode(encoding="utf-8")
    # decode b64 byte into str, "byte" to "str"

    with open(b64_str_pth, "w") as g:
        g.write(MIME_b64_str)


def imgByte_to_b64Str(raw_byte):

    MIME_b64_byte = base64.encodebytes(raw_byte)
    # convert raw byte into b64 byte , "byte" to "byte", per RFC 2045 / MIME

    MIME_b64_str = MIME_b64_byte.decode(encoding="utf-8")
    # decode b64 byte into str, "byte" to "str"

    return MIME_b64_str


def b64Str_to_imgByte(MIME_b64_str):

    MIME_b64_byte = bytes(MIME_b64_str, encoding="utf-8")
    # convert a b64 str into a b64 byte ("str" to "byte")

    raw_byte = base64.decodebytes(MIME_b64_byte)
    # convert a b64 byte into a raw byte ("byte" to "byte), per RFC 2045 / MIME

    return raw_byte



if __name__ == "__main__":
    img_pth = "2.jpeg"

    b64_str_pth = "new_b65"
    dst_img_pth = "dst_img111.jpeg"



    src_img_pth = "dst_img.jpeg"
    new_b64_str_pth = "new_b65"

    #img_to_b64(src_img_pth, new_b64_str_pth)