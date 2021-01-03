#--- Day 11: Space Police ---

# First star:
# You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of
# square panels on the side of your ship, detect the color of its current panel, and paint its current panel black or
# white. (All of the panels are currently black.)
# The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's
# camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will
# output two values:
# - First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel
# black, and 1 means to paint the panel white.
# - Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90
# degrees, and 1 means it should turn right 90 degrees.
# After the robot turns, it should always move forward exactly one panel. The robot starts facing up.
# The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the Intcode
# computer inside the robot during this process.
# Build a new emergency hull painting robot and run the Intcode program on it. How many panels does it paint at least
# once?

# Second star:

from all_days.intcode import Opcoder

class Robot():
    def __init__(self):
        self.direction = 'N'
        self.position = (0, 0)
        self._nesw = 'NESW'

    def camera(self, panel):
        return panel.color(self.position)  # 0 means black - 1 means white

    def move(self, turn):
        self.direction = self._nesw[(self._nesw.index(self.direction) + (2 * turn - 1)) % 4]
        if self.direction == 'N':
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == 'S':
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == 'E':
            self.position = (self.position[0] +1, self.position[1])
        elif self.direction == 'W':
            self.position = (self.position[0] - 1, self.position[1])
        else:
            raise Exception('Direction unknown - must be E, W, S or N')


class Panel():
    def __init__(self):
        self.positions = []
        self.colors = []

    def color(self, position):  # 0 means black - 1 means white
        if position in self.positions:
            return self.colors[self.positions.index(position)]
        else:
            return 0

    def paint(self, position, color):  # 0 means black - 1 means white
        if position in self.positions:
            self.colors[self.positions.index(position)] = color
        else:
            self.positions += [position]
            self.colors += [color]


def run(data_dir, star):
    with open(f'{data_dir}/input-day11.txt', 'r') as fic:
        opcodes = [int(x) for x in fic.read().split(',')]
    if star == 1:
        robot = Robot()
        panel = Panel()
        brain = Opcoder(opcodes)
        while not brain.exit:
            brain.inputs(robot.camera(panel))
            brain.run_until_next_output()
            panel.paint(robot.position, brain.output_values[-1])
            brain.run_until_next_output()
            robot.move(brain.output_values[-1])
        npanels = len(panel.positions)
        print(f'Star {star} - There are {npanels} panels painted at least once')
        return npanels
    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
