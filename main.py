import argparse
from PIL import Image # Pillow

def load_image(path, size):
    img = Image.open(path).convert('RGB')
    return img.resize(size)

def build_image_data(image):
    pixels = image.load()
    width, height = image.size

    lines = ["local image = {"]

    for y in range(height):
        row = [f'    [{y}] = "']

        for x in range(width):
            r, g, b = pixels[x, y]
            color = f'rgb({r},{g},{b})'

            row.append(
                f'<font color="{color}">□</font>'
            )

        row.append('",')
        lines.append(''.join(row))

    lines.append("}\n\nreturn image")
    return '\n'.join(lines)

# now CLI
def main(): # main function
    parser = argparse.ArgumentParser(description="Image to Roblox RichText converter")
    
    parser.add_argument("input", help="Input image file")
    parser.add_argument("-o", "--output", default="output.rbxmx", help="Output file")
    parser.add_argument("-w", "--width", type=int, default=128)
    parser.add_argument("-H", "--height", type=int, default=96)
    args = parser.parse_args()

    image = load_image(args.input, (args.width, args.height))
    result = build_image_data(image)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Done: {args.output}")

if __name__ == "__main__":
    main()
