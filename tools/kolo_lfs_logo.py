from pathlib import Path

WIDTH, HEIGHT = 288, 80
SCALE = 4
BACKGROUND = (10, 12, 28)
EDGE = (107, 42, 99)
PINK = (255, 117, 177)
CYAN = (114, 235, 229)
WHITE = (249, 227, 236)
SHADOW = (61, 29, 72)
GLYPHS = {
    "k": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "o": ("00000", "01110", "10001", "10001", "10001", "01110", "00000"),
    "l": ("01100", "00100", "00100", "00100", "00100", "01110", "00000"),
    "s": ("00000", "01111", "10000", "01110", "00001", "11110", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "f": ("00110", "01001", "01000", "11100", "01000", "01000", "01000"),
    " ": ("00000",) * 7,
}
pixels = [[BACKGROUND for _ in range(WIDTH)] for _ in range(HEIGHT)]


def rect(x, y, width, height, color):
    for row in range(max(0, y), min(HEIGHT, y + height)):
        for col in range(max(0, x), min(WIDTH, x + width)):
            pixels[row][col] = color


for x in range(0, WIDTH, 8):
    rect(x, 0, 4, 2, EDGE)
    rect(x + 4, HEIGHT - 2, 4, 2, EDGE)
for y in range(0, HEIGHT, 8):
    rect(0, y, 2, 4, EDGE)
    rect(WIDTH - 2, y + 4, 2, 4, EDGE)

for x, y, color in ((11, 15, CYAN), (269, 12, PINK), (13, 59, PINK), (272, 58, CYAN)):
    rect(x + 3, y, 3, 12, color)
    rect(x, y + 4, 9, 3, color)

text = "kolo's lfs"
x0 = (WIDTH - ((len(text) * 6 - 1) * SCALE)) // 2
y0 = 25
for index, char in enumerate(text):
    for row, line in enumerate(GLYPHS[char]):
        for col, bit in enumerate(line):
            if bit == "1":
                x = x0 + (index * 6 + col) * SCALE
                y = y0 + row * SCALE
                rect(x + 2, y + 3, SCALE, SCALE, SHADOW)
                rect(x, y, SCALE, SCALE, CYAN if row < 2 else PINK if row > 4 else WHITE)

output = Path("kolo-lfs-kernel-logo.ppm")
with output.open("w", encoding="ascii") as file:
    file.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")
    for row in pixels:
        file.write(" ".join(f"{red} {green} {blue}" for red, green, blue in row))
        file.write("\n")
print(output)
