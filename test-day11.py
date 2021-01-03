from all_days.day11 import Robot, Panel

def test_example1():
    robot = Robot()
    panel = Panel()

    print('Step 0 - Initialization')
    if robot.direction != 'N':
        raise Exception('Robot must face north')
    if panel.color(robot.position) != 0:
        raise Exception('Start position must be black (0)')
    if robot.camera(panel) != 0:
        raise Exception('Robot should send a 0')

    print('Step 1')
    panel.paint(robot.position, 1)
    robot.move(0)
    if panel.color((0, 0)) != 1:
        raise Exception('Position (0, 0) should be painted in white')
    if robot.position != (-1, 0):
        raise Exception('Robot position should be (-1, 0)')
    if robot.direction != 'W':
        raise Exception('Robot should face West')
    if robot.camera(panel) != 0:
        raise Exception('Robot should send a 0')

    print('Step 2')
    panel.paint(robot.position, 0)
    robot.move(0)
    if panel.color((-1, 0)) != 0:
        raise Exception('Position (-1, 0) should be painted in black')
    if robot.position != (-1, 1):
        raise Exception('Robot position should be (-1, 1)')
    if robot.direction != 'S':
        raise Exception('Robot should face South')
    if robot.camera(panel) != 0:
        raise Exception('Robot should send a 0')

    print('Steps 3 and 4')
    panel.paint(robot.position, 1)
    robot.move(0)
    panel.paint(robot.position, 1)
    robot.move(0)
    if panel.color((-1, 1)) != 1:
        raise Exception('Position (-1, 1) should be painted in white')
    if panel.color((0, 1)) != 1:
        raise Exception('Position (0, 1) should be painted in white')
    if robot.position != (0, 0):
        raise Exception('Robot position should be (0, 0)')
    if robot.direction != 'N':
        raise Exception('Robot should face North')
    if robot.camera(panel) != 1:
        raise Exception('Robot should send a 1')

    print('Steps 5, 6, 7')
    panel.paint(robot.position, 0)
    robot.move(1)
    panel.paint(robot.position, 1)
    robot.move(0)
    panel.paint(robot.position, 1)
    robot.move(0)
    if panel.color((0, 0)) != 0:
        raise Exception('Position (0, 0) should be painted in black')
    if panel.color((1, 0)) != 1:
        raise Exception('Position (1, 0) should be painted in white')
    if panel.color((1, -1)) != 1:
        raise Exception('Position (1, -1) should be painted in white')
    if robot.position != (0, -1):
        raise Exception('Robot position should be (0, -1)')
    if robot.direction != 'W':
        raise Exception('Robot should face West')
    if robot.camera(panel) != 0:
        raise Exception('Robot should send a 0')

    print('Summary stage')
    if len(panel.positions) != 6:
        raise Exception('Exactly 6 panels should have been painted at least once')

    print('-- Test example 1 OK')


def main():
    test_example1()


if __name__ == '__main__':
    main()
