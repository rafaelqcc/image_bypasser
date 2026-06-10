import argparse
from PIL import Image  # Pillow

def load_image(path, size):
    img = Image.open(path).convert('RGB')
    return img.resize(size)

def build_image_data(image):
    pixels = image.load()
    width, height = image.size

    lines = ["local image = {"]

    for y in range(height):
        row = [f"    [{y + 1}] = {{" ]

        for x in range(width):
            r, g, b = pixels[x, y]

            row.append(f"{{{r},{g},{b}}},")

        row.append("},")
        lines.append("".join(row))

    lines.append("}\n\nreturn image")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    # Args
    parser.add_argument("-o", "--output", default="output.rbxmx")
    parser.add_argument("-w", "--width", type=int, default=128)
    parser.add_argument("-H", "--height", type=int, default=96)

    args = parser.parse_args()
    # Read the xml
    base_xml = open("image.rbxmx", "r", encoding="utf-8").read()

    image = load_image(args.input, (args.width, args.height))
    image_data = build_image_data(image)

    result = base_xml.replace("___", image_data)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)

    print("Done:", args.output)

if __name__ == "__main__":
    main()
