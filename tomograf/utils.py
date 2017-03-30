def bresenham(x1, y1, x2, y2):

    line = []
    kx = 1 if x1 <= x2 else -1
    ky = 1 if y1 <= y2 else -1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x = x1
    y = y1
    line.append([x, y])
    if dx >= dy:
        e = dx / 2
        for i in range(0, int(dx)):
            x += kx
            e = e - dy
            if e < 0:
                y += ky
                e = e + dx
            line.append([x, y])
    else:
        e = dy / 2
        for i in range(0, int(dy)):
            y += ky
            e = e - dx
            if e < 0:
                x += kx
                e = e + dy
            line.append([x, y])
    return line
