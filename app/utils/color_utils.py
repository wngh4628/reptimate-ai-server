import math

#hex로 변환
def rgb_to_hex(r, g, b):
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)


#두 개의 RGB 색상 값 사이의 유사성을 측정하는 함수
def rgb_similarity(color1:int, color2:int):
    # Calculate the Euclidean distance between two RGB colors
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    distance = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return distance

#특정 색상과 비교하여 유사한 색상을 찾는 함수
def find_similar_colors(target_color:[], search_list:[], threshold:int):
    total = []
    similar_colors = []
    similar_idxs = []
    i = 0
    for color in search_list[0]:
        if rgb_similarity(target_color, color) <= threshold:
            similar_colors.append(color)
            # print("몇번째 개체야?")
            # print(i)
            similar_idxs.append(search_list[1][i])
        i = i + 1

    # print("similar_idxs")
    # print(similar_idxs)
    # print("similar_idxs")
    total.append(similar_colors)
    total.append(similar_idxs)
    return total


#RGB -> CIELAB : XYZ로 변환 후 LAB으로 변환 진행
def rgb2lab(inputColor:[]):

    num = 0
    RGB = [0, 0, 0]

    for value in inputColor:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    # Observer= 2°, Illuminant= D65
    XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab