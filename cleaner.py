import sys
import pygame
# 0 1 0 0 0 0 1 0 1 0
# 0 0 1 0 0 1 0 0 0 0
# 1 0 0 0 0 0 0 1 0 1
# 0 0 1 0 0 1 0 0 1 1
real_map = [[0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 1]]

# real_map = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]]

def sensor(s):
    """
    s: array of coordinates (row, column)
    return: n, given that nth element of s is first to be non-zero
        obs: n is -1 if s is only composed of zeros
    """
    for i in range(len(s)):
        if real_map[s[i][0]][s[i][1]]:
            return i
    return -1

class Robot():
    def __init__(self, map_size):
        self.pos = [0, 0] #row, column
        self.map_size = map_size
        self.map = [[0]*map_size for m in range(map_size)]

        # positioning our bot
        self.map[self.pos[0]][self.pos[1]] = 2
        sensor_results = self.sense()
        for t in sensor_results:
            v = sensor_results[t]
            if v:
                self.map[v[0]][v[1]] = 1

    def print_map(self):
        for row in self.map:
            print(row)
    
    def seen_coords(self):
        seen = []
        for r in range(len(self.map)):
            for k in range(len(self.map[0])):
                if self.map[r][k] and (r != self.pos[0] or k != self.pos[1]):
                    seen.append((r, k))
        return seen

    def sense(self):
        top = [[x, self.pos[1]] for x in range(self.pos[0])]
        sensor_value = sensor(top)
        top = top[sensor_value] if sensor_value != -1 else None

        bottom = [[x, self.pos[1]] for x in range(self.pos[0]+1, self.map_size)]
        sensor_value = sensor(bottom)
        bottom = bottom[sensor_value] if sensor_value != -1 else None

        left = [[self.pos[0], x] for x in range(self.pos[1])]
        sensor_value = sensor(left)
        left = left[sensor_value] if sensor_value != -1 else None


        right = [[self.pos[0], x] for x in range(self.pos[1]+1, self.map_size)]
        sensor_value = sensor(right)
        right = right[sensor_value] if sensor_value != -1 else None
        return {'top': top, 'right': right, 'bottom': bottom, 'left': left}

    def move(self, new_pos):
        if new_pos[0] < 0 or new_pos[0] >= self.map_size or new_pos[1] < 0 or new_pos[1] >= self.map_size:
            return 1
        if self.map[new_pos[0]][new_pos[1]]:
            return 1 # can't move there
        if self.pos[0] != new_pos[0] or self.pos[1] != new_pos[1]:
            self.map[self.pos[0]][self.pos[1]] = 0
            self.map[new_pos[0]][new_pos[1]] = 2
            self.pos = new_pos
            sensor_results = self.sense()
            for t in sensor_results:
                v = sensor_results[t]
                if v:
                    self.map[v[0]][v[1]] = 1
        return 0

if sys.argv[1] == 'm':
    print("Real map:")
    for r in real_map:
        print(r)

    r = Robot(4)
    print("Robot vision:")
    r.print_map()
    entra = input()
    while entra in ['w', 'a', 's', 'd']:
        new_pos = [r.pos[0], r.pos[1]]
        if entra == 'w':
            new_pos[0] -= 1
        elif entra == 's':
            new_pos[0] += 1
        elif entra == 'a':
            new_pos[1] -= 1
        elif entra == 'd':
            new_pos[1] += 1
        r.move(new_pos)
        r.print_map()
        entra = input()
    sys.exit()

class GameObject():
    def __init__(self, x, y, w, h, s, robot=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.s = s # speed
        self.robot = robot

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def update_from_bot(self):
        modifier = 50
        self.x = self.robot.pos[1]*modifier
        self.y = self.robot.pos[0]*modifier


pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Cleaner robot example")
bot = Robot(10)
robot_obj = GameObject(50, 50, 50, 50, 5, bot)

img = pygame.image.load('bot.png')
img.convert()

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    new_pos = [bot.pos[0], bot.pos[1]]
    if keys[pygame.K_LEFT]:
        new_pos[1] -= 1
    if keys[pygame.K_RIGHT]:
        new_pos[1] += 1
    if keys[pygame.K_UP]:
        new_pos[0] -= 1
    if keys[pygame.K_DOWN]:
        new_pos[0] += 1
    if keys[pygame.K_q]:
        run = False
    bot.move(new_pos)
    robot_obj.update_from_bot()

    win.fill((255, 255, 255))
    win.blit(img, (robot_obj.get_rect()))
    #pygame.draw.rect(win, (255, 0, 0), (robot_obj.get_rect()))
    for c in bot.seen_coords():
        pygame.draw.rect(win, (0, 155, 155), (c[1]*50, c[0]*50, 50, 50))

    pygame.display.update()

pygame.quit()
