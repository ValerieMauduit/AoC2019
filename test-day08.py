# For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following
# image layers:
# Layer 1: 123
#          456
# Layer 2: 789
#          012

from all_days.day08 import layers

def main():
    output_layers = layers('123456789012', 3, 2)
    expected_layers = [['123', '456'], ['789', '012']]
    if output_layers != expected_layers:
        raise Exception(f'Output layers {output_layers} are not expected layers {expected_layers}')

if __name__ == '__main__':
    main()