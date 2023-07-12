from src.constant import DIRECTIONS
from src.Board import Board
from src.PipeManager import PipeLogic


class Node:
    def __init__(self, state, parent=None):
        self.state = state

    def expand(self, logic):
        return [Node(state, self) for state in logic.getAction(self.state)]


class Agent:
    def __init__(self, board: Board):
        self.logic = PipeLogic()
        self.pieces = self.logic.pieces
        self.hsize, self.vsize = self.logic.hsize, self.logic.vsize
        self.cx, self.cy = self.logic.cx, self.logic.cy

    def checkWinCondition(self, pieces):
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

    def encodePieces(self, pieces):
        s = ""
        for y in range(self.vsize):
            for x in range(self.hsize):
                s += format(pieces[x][y] % 16, "04b")
        return s

    def decodePieces(self, s):
        pieces = [[0 for _ in range(self.hsize)] for _ in range(self.vsize)]
        for y in range(self.vsize):
            for x in range(self.hsize):
                start = (y * self.hsize + x) * 4
                pieces[x][y] = int(s[start : start + 4], base=2)

    def solve(self):
        pass


class DfsAgent(Agent):
    def __init__(self, board):
        Agent.__init__(self, board)

    def checkWinCondition(self, pieces):
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

    def dfs(self, pieces):
        root = Node(pieces)
        stack = [root]
        while len(stack):
            n = stack.pop()
            if self.logic._checkWinCondition(n.state):
                return self.backtracking(n)

    def solve(self):
        pass

    def backtracking(self, node):
        path = []
        while node != None:
            pos = node.pos
            rot = node.rot
            path.append((pos << 1) + rot)
            node = node.parent
        path.reverse()
        return path
