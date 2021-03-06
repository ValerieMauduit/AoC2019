# --- Day 8: Space Image Format ---

# First star:
# Images are sent as a series of digits that each represent the color of a single pixel. The digits fill each row of the
# image left-to-right, then move downward to the next row, filling rows top-to-bottom until every pixel of the image is
# filled.
# Each image actually consists of a series of identically-sized layers that are filled in this way. So, the first digit
# corresponds to the top-left pixel of the first layer, the second digit corresponds to the pixel to the right of that
# on the same layer, and so on until the last digit, which corresponds to the bottom-right pixel of the last layer.
# The image you received is 25 pixels wide and 6 pixels tall.
# To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains
# the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?

# Second star:
# Now you're ready to decode the image. The image is rendered by stacking the layers and aligning the pixels with the
# same positions in each layer. The digits indicate the color of the corresponding pixel:
# 0 is black, 1 is white, and 2 is transparent.
# The layers are rendered with the first layer in front and the last layer in back. So, if a given position has a
# transparent pixel in the first and second layers, a black pixel in the third layer, and a white pixel in the fourth
# layer, the final image would have a black pixel at that position.
# What message is produced after decoding your image?

def layers(image_input, width, height):
    raws = []
    for n in range(0, len(image_input), width):
        raws += [image_input[n:(n + width)]]
    layers = []
    for p in range(0, len(raws), height):
        layers +=  [raws[p:(p + height)]]
    return layers


def count_digit(image, digit):
    return sum([raw.count(str(digit)) for raw in image])


def build_image(layers):
    output_list = [n for raw in layers[0] for n in raw]
    width = len(layers[0][0])
    l = 1
    while count_digit(output_list, 2) > 0:
        next_image = [n for raw in layers[l] for n in raw]
        output_list = [output_list[n] if output_list[n] != '2' else next_image[n] for n in range(len(output_list))]
        l += 1
    output_image = []
    for n in range(0, len(output_list), width):
        output_image += [''.join(output_list[n:(n + width)])]
    return output_image


def print_image(image):
    printable = [''.join(['*' if x == '1' else ' ' for x in raw]) for raw in image]
    for raw in printable:
        print(raw)


def run(data_dir, star):
    with open(f'{data_dir}/input-day08.txt', 'r') as fic:
        tempo = fic.read().strip('\n')
    output_layers = layers(tempo, 25, 6)

    if star == 1:
        count_zeros = [count_digit(layer, 0) for layer in output_layers]
        min_zeros_layer = output_layers[count_zeros.index(min(count_zeros))]
        check_value = count_digit(min_zeros_layer, 1) * count_digit(min_zeros_layer, 2)
        print(f'Star {star} - The check value is {check_value}')
        return check_value

    elif star == 2:
        output_image = build_image(output_layers)
        print(f'Star {star}:')
        print_image(output_image)
        return

    else:
        raise Exception('Star number must be either 1 or 2.')
