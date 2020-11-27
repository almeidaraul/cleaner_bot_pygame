# 0 1 0 0
# 0 0 1 0
# 1 0 0 0
# 0 0 1 0
real_map = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]]

def sensor(s):
    """
    s: array
    return: n, given that nth element of s is first to be non-zero
        obs: n is -1 if s is only composed of zeros
    """
    for i in range(len(s)):
        if s[i]:
            return i
    return -1

class Robot():
    def __init__(self, map_size):
        self.pos = [0, 0] //row, column
        self.map_size = map_size
        self.map = [[0]*map_size for m in range(map_size)]
        self.map[self.pos[0]][self.pos[1]] = 1
        print(self.map)

    def sense(self):
        top = [self.map[x][self.pos[1]] for x in range(self.pos[0])]
        sensor_value = sensor(top)
        top = [sensor_value, self.pos[1]] if sensor_value != -1 else None

        bottom = [self.map[x][self.pos[1]] for x in range(self.pos[0]+1, self.map_size)]
        sensor_value = sensor(bottom)
        bottom = [sensor_value+self.pos[0]+1, self.pos[1]] if sensor_value != -1 else None

        left = [self.map[self.pos[0]][x] for x in range(self.pos[1])]
        sensor_value = sensor(left)
        left = [self.pos[0], sensor_value] if sensor_value != -1 else None

        right = [self.map[self.pos[0]][x] for x in range(self.pos[1]+1, self.map_size)]
        sensor_value = sensor(right)
        right = [self.pos[0], snesor_value+self.pos[1]+1] if sensor_value != -1 else None
        return {'top': top, 'right': right, 'bottom': bottom, 'left': left]

    def move(self, new_pos):
        if self.map[new_pos]:
            return 1 # can't move there
        elif self.pos != new_pos:
            self.map[self.pos[0]][self.pos[1]] = 0
            self.map[new_pos[0]][new_pos[1]] = 1
            self.pos = new_pos
            sensor_results = self.sense()
            for t in sensor_results:
                v = sensor_results[t]
                if v:
                    self.map[v[0]][v[1]] = 1
        return 0
