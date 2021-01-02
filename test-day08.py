# For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following
# image layers:
# Layer 1: 123
#          456
# Layer 2: 789
#          012

# Given an image 2 pixels wide and 2 pixels tall, the image data 0222112222120000 corresponds to the following image
# layers:
# Layer 1: 02
#          22
# Layer 2: 11
#          22
# Layer 3: 22
#          12
# Layer 4: 00
#          00
# Then, the full image can be found by determining the top visible pixel in each position:
# 01
# 10

from all_days.day08 import layers, build_image


def test_star1():
    output_layers = layers('123456789012', 3, 2)
    expected_layers = [['123', '456'], ['789', '012']]
    if output_layers != expected_layers:
        raise Exception(f'Output layers {output_layers} are not expected layers {expected_layers}')


def test_star2():
    output_layers = layers('0222112222120000', 2, 2)
    expected_layers = [['02', '22'], ['11', '22'], ['22', '12'], ['00', '00']]
    output_image = build_image(output_layers)
    expected_image = ['01', '10']
    if output_layers != expected_layers:
        raise Exception(f'Output layers {output_layers} are not expected layers {expected_layers}')
    if output_image != expected_image:
        raise Exception(f'Output layers {output_image} are not expected layers {expected_image}')


def main():
    test_star1()
    test_star2()


if __name__ == '__main__':
    main()