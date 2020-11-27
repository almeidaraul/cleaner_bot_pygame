# 0 1 0 0
# 0 0 1 0
# 1 0 0 0
# 0 0 1 0
real_map = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]]

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
