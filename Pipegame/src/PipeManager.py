import math, random
from src.constant import DIRECTIONS

directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
tileSize = 32


class PipeManager:
    def __init__(self):
        self.states = None
        self.pieces = None

    def generate(self, hsize, vsize):
        self.hsize = hsize
        self.vsize = vsize
        size = hsize * vsize

        addList = [0 for _ in range(size)]  # Some kind of queue?
        added = [[False for _ in range(vsize)] for _ in range(hsize)]
        self.pieces = [[0 for _ in range(vsize)] for _ in range(hsize)]
        self.states = [[0 for _ in range(vsize)] for _ in range(hsize)]

        cx = math.floor((random.random() * 0.3 + 0.4) * hsize)
        cy = math.floor((random.random() * 0.3 + 0.4) * vsize)
        self.cx, self.cy = cx, cy
        addList[0] = (cy << 8) + cx
        added[cx][cy] = True
        self.pieces[cx][cy] = 0x10

        addCount = 1
        for connectedCount in range(size):
            # Select a random leave node
            pos = math.floor(random.random() * addCount)
            c = addList[pos]
            x = c & 0xFF
            y = c >> 8

            if connectedCount != 0:
                self._randomConnect(x, y)

            addCount -= 1
            if pos != addCount:
                addList[pos] = addList[addCount]

            if y > 0 and not added[x][y - 1]:
                addList[addCount] = (y - 1 << 8) + x
                added[x][y - 1] = True
                addCount += 1
            if x < hsize - 1 and not added[x + 1][y]:
                addList[addCount] = (y << 8) + x + 1
                added[x + 1][y] = True
                addCount += 1
            if y < vsize - 1 and not added[x][y + 1]:
                addList[addCount] = (y + 1 << 8) + x
                added[x][y + 1] = True
                addCount += 1
            if x > 0 and not added[x - 1][y]:
                addList[addCount] = (y << 8) + x - 1
                added[x - 1][y] = True
                addCount += 1

        self.pieces[cx][cy] &= 0xF

    def scramble(self):
        for x in range(self.hsize):
            for y in range(self.vsize):
                d = math.floor(random.random() * 4)
                i = self.pieces[x][y]
                i = i << d & 0xF | i >> (4 - d)
                self.pieces[x][y] = i

    def light(self, cx=None, cy=None, norefresh=None):
        if cx is None:
            cx = self.cx
        else:
            self.cx = cx

        if cy is None:
            cy = self.cy
        else:
            self.cy = cy

        hsize, vsize = self.hsize, self.vsize
        # Reset Light bit of State
        for x in range(hsize):
            for y in range(vsize):
                self.states[x][y] &= 0xE

        # Perform DFS to find all connected pipes from center
        lighted = 0
        lightList = [False for _ in range(hsize * vsize)]
        lightList[0] = (cy << 8) + cx
        lightCount = 1

        while lightCount:
            lighted += 1
            lightCount -= 1

            c = lightList[lightCount]
            x = c & 0xFF
            y = c >> 8
            self.states[x][y] |= 1

            for i in range(4):
                dir = directions[i]
                _x, _y = x + dir[0], y + dir[1]
                dirBit = 2**i
                oppBit = self._oppDir(dirBit)
                isInBoard = 0 <= _x < hsize and 0 <= _y < vsize
                if (
                    isInBoard
                    and self.pieces[x][y] & dirBit
                    and self.pieces[_x][_y] & oppBit
                    and not self.states[_x][_y] & 1
                ):
                    lightList[lightCount] = (_y << 8) + _x
                    lightCount += 1
        return lighted == hsize * vsize

    # Helper ==========================================================
    def _oppDir(self, dirBit):
        return ((dirBit & 3) << 2) | ((dirBit & 12) >> 2)

    def _randomConnect(self, x, y):
        while True:
            dir = math.floor(random.random() * 4)
            if dir == 0:
                if y > 0 and self.pieces[x][y - 1]:
                    self.pieces[x][y] |= 1
                    self.pieces[x][y - 1] |= 4
                    break
            elif dir == 1:
                if x < self.hsize - 1 and self.pieces[x + 1][y]:
                    self.pieces[x][y] |= 2
                    self.pieces[x + 1][y] |= 8
                    break
            elif dir == 2:
                if y < self.vsize - 1 and self.pieces[x][y + 1]:
                    self.pieces[x][y] |= 4
                    self.pieces[x][y + 1] |= 1
                    break
            else:
                if x > 0 and self.pieces[x - 1][y]:
                    self.pieces[x][y] |= 8
                    self.pieces[x - 1][y] |= 2
                    break

    def _randomConnect2(self, x, y):
        dx, dy = directions[math.floor(random.random() * 4)]
        _x, _y = x + dx, y + dy
        valid = False
        while not valid:
            dir = math.floor(random.random() * 4)
            _x, _y = directions[dir]
            isInBoard = 0 <= _x < self.hsize and 0 <= _y < self.vsize
            valid = isInBoard and self.pieces[_x][_y]
        else:
            dirBit = 2**dir
            self.pieces[x][y] |= dirBit
            self.pieces[x][y - 1] |= ((dirBit & 3) << 2) | ((dirBit & 12) >> 2)

    def _getConnection(self, x, y, hsize, vsize):
        res = []
        for i in range(4):
            dir = directions[i]
            _x, _y = x + dir[0], y + dir[1]
            dirBit = 2**i
            oppBit = self._oppDir(dirBit)
            isInBoard = 0 <= _x < hsize and 0 <= _y < vsize
            if (
                isInBoard
                and self.pieces[x][y] & dirBit
                and self.pieces[_x][_y] & oppBit
                and not self.states[_x][_y] & 1
            ):
                res.append((_y << 8) + _x)
        return res


class PipeLogic:
    def _oppDir(self, dirBit):
        return ((dirBit & 3) << 2) | ((dirBit & 12) >> 2)

    def _checkWinCondition(self, pieces):
        cx, cy = self.cx, self.cy
        hsize, vsize = self.hsize, self.vsize
        states = [[True for _ in range(hsize)] for _ in range(vsize)]

        pipeList = [[0 for _ in range(hsize)] for _ in range(vsize)]
        pipeList[0] = (cy << 8) + cx
        pipeCount = 1

        while pipeCount:
            c = pipeList[pipeCount]
            x = c & 0xFF
            y = c >> 8
            pipeCount -= 1
            states[x][y] |= 1

            for i in range(4):
                dir = DIRECTIONS[i]
                _x, _y = x + dir[0], y + dir[1]
                dirBit = 2**i
                oppBit = self.logic._oppDir(dirBit)
                isInBoard = 0 <= _x < hsize and 0 <= _y < vsize
                if (
                    isInBoard
                    and pieces[x][y] & dirBit == 1
                    and pieces[_x][_y] & oppBit == 1
                    and not states[_x][_y] & 1
                ):
                    pipeList[pipeCount] = (_y << 8) + _x
                    pipeCount += 1

        return pipeCount == hsize * vsize

    def _randomConnect(self, x, y, pieces):
        hsize, vsize = len(pieces), len(pieces[0])
        while True:
            dir = math.floor(random.random() * 4)
            if dir == 0:
                if y > 0 and self.pieces[x][y - 1]:
                    pieces[x][y] |= 1
                    pieces[x][y - 1] |= 4
                    break
            elif dir == 1:
                if x < hsize - 1 and pieces[x + 1][y]:
                    pieces[x][y] |= 2
                    pieces[x + 1][y] |= 8
                    break
            elif dir == 2:
                if y < vsize - 1 and pieces[x][y + 1]:
                    pieces[x][y] |= 4
                    pieces[x][y + 1] |= 1
                    break
            else:
                if x > 0 and pieces[x - 1][y]:
                    pieces[x][y] |= 8
                    pieces[x - 1][y] |= 2
                    break

    def _randomConnect2(self, x, y, pieces):
        hsize, vsize = len(pieces), len(pieces[0])
        dx, dy = directions[math.floor(random.random() * 4)]
        _x, _y = x + dx, y + dy
        valid = False
        while not valid:
            dir = math.floor(random.random() * 4)
            _x, _y = directions[dir]
            isInBoard = 0 <= _x < hsize and 0 <= _y < vsize
            valid = isInBoard and pieces[_x][_y]
        else:
            dirBit = 2**dir
            pieces[x][y] |= dirBit
            pieces[x][y - 1] |= ((dirBit & 3) << 2) | ((dirBit & 12) >> 2)

    def _getConnection(self, x, y, pieces, states):
        hsize, vsize = len(pieces), len(pieces[0])
        res = []
        for i in range(4):
            dir = directions[i]
            _x, _y = x + dir[0], y + dir[1]
            dirBit = 2**i
            oppBit = self._oppDir(dirBit)
            isInBoard = 0 <= _x < hsize and 0 <= _y < vsize
            if (
                isInBoard
                and pieces[x][y] & dirBit
                and pieces[_x][_y] & oppBit
                and not states[_x][_y] & 1
            ):
                res.append((_y << 8) + _x)
        return res
