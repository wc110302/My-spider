import re

import pytesseract
from PIL import Image


# 二值化处理
def two_value(filename):

    image = Image.open(filename)
    # 灰度图
    lim = image.convert('L')
    # 灰度阈值设为165，低于这个值的点全部填白色
    threshold = 165
    table = []

    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    bim = lim.point(table, '1')
    bim.save(filename)


def add(string):
    s1 = ''
    for i in string:
        if i.isdigit():
            s1 = s1 + i
        else:
            s1 = s1 + " "
    lt = s1.split(" ")
    m = 0
    for a in lt:
        if a.isdigit():
            m = m + int(a)
    return m


def sub(string):
    s1 = ''
    for i in string:
        if i.isdigit():
            s1 = s1 + i
        else:
            s1 = s1 + " "
    lt = s1.split(" ")
    m = 0
    for a in lt:
        if a.isdigit():
            if not m:
                m = int(a)
            else:
                m -= int(a)
    return m


def mul(string):
    s1 = ''
    for i in string:
        if i.isdigit():
            s1 = s1 + i
        else:
            s1 = s1 + " "
    lt = s1.split(" ")
    m = 1
    for a in lt:
        if a.isdigit():
            m *= int(a)
    return m


def get_num(filename):
    two_value(filename)
    image = Image.open(filename)
    vcode = pytesseract.image_to_string(image)
    print(vcode)
    if "+" in vcode:
        return add(vcode)
    elif "X" in vcode or "x" in vcode:
        return mul(vcode)
    elif "-" in vcode:
        return sub(vcode)


def join(png1, png2, png3, png4, count):
    """
    :param png1: path
    :param png2: path
    :param flag: horizontal or vertical
    :return:
    """
    img1, img2, img3, img4 = Image.open(png1), Image.open(png2), Image.open(png3), Image.open(png4)
    size1, size2, size3, size4 = img1.size, img2.size, img3.size, img4.size

    joint = Image.new('RGB', (size1[0]+size2[0], size1[1]))
    loc1, loc2 = (0, 0), (size1[0], 0)
    joint.paste(img1, loc1)
    joint.paste(img2, loc2)
    joint.save('./image_{0}/5.png'.format(str(count)))

    joint = Image.new('RGB', (size3[0]+size4[0], size3[1]))
    loc3, loc4 = (0, 0), (size1[0], 0)
    joint.paste(img3, loc3)
    joint.paste(img4, loc4)
    joint.save('./image_{0}/6.png'.format(str(count)))

    img1, img2 = Image.open("./image_{0}/5.png".format(str(count))), Image.open("./image_{0}/6.png".format(str(count)))
    size1, size2 = img1.size, img2.size

    joint = Image.new('RGB', (size1[0]+size2[0], size1[1]))
    loc1, loc2 = (0, 0), (size1[0], 0)
    joint.paste(img1, loc1)
    joint.paste(img2, loc2)
    joint.save('./image_{0}/7.png'.format(str(count)))


if __name__ == '__main__':
    # png = '1.jpg'
    # join('1.jpg', '2.jpg')

    a = get_num('./image_5/7.png')
    print(a)