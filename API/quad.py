class point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.userdata = data
    def __str__(self):
        return f'{self.x}, {self.y}'


class cell:
    def __init__(self, x, y, half_width, half_height):
        self.x = x
        self.y = y
        self.half_width = half_width
        self.half_height = half_height

        self.min_x = self.x - self.half_width
        self.max_x = self.x + self.half_width
        self.min_y = self.y - self.half_height
        self.max_y = self.y + self.half_height

    def contains(self, pt):
        x, y = abs(pt.x), abs(pt.y)
        # print(x,y)
        # print(self.max_x,self.max_y)
        if (
            x <= abs(self.max_x)
            and x >= abs(self.min_x)
            and y <= abs(self.max_y)
            and y >= abs(self.min_y)
        ):
            return True

        return False

    def intersect(self, cel):
        if (abs(self.min_x) > abs(cel.max_x) or abs(cel.min_x) > abs(self.max_x)) or (
            abs(self.min_y) > abs(cel.max_y) or abs(cel.min_y) > abs(self.max_y)
        ):
            return False

        return True

    def __str__(self):
        return f'{self.x}, {self.y}'


class quad_tree:
    hgt = 1

    def __init__(self, cell, cap=4, lvl=0):
        self.boundary = cell
        self.capacity = cap
        self.points = []
        self.divided = False

        self.n_points = 0
        self.level = lvl

        if self.level + 1 > quad_tree.hgt:
            quad_tree.hgt = self.level + 1

    def subdivide(self):
        new_w = self.boundary.half_width / 2
        new_h = self.boundary.half_height / 2

        x = self.boundary.x
        y = self.boundary.y

        self.divided = True

        self.ne = quad_tree(
            cell(x + new_w, y + new_h, new_w, new_h), self.capacity, self.level + 1
        )
        self.nw = quad_tree(
            cell(x - new_w, y + new_h, new_w, new_h), self.capacity, self.level + 1
        )
        self.se = quad_tree(
            cell(x + new_w, y - new_h, new_w, new_h), self.capacity, self.level + 1
        )
        self.sw = quad_tree(
            cell(x - new_w, y - new_h, new_w, new_h), self.capacity, self.level + 1
        )

    def insert(self, pt):
        if not self.boundary.contains(pt):
            # print('cannot insert')
            return False

        self.n_points += 1

        if len(self.points) < self.capacity:
            self.points.append(pt)
            return True

        if not self.divided:
            self.subdivide()

        if self.nw.insert(pt):
            return True
        if self.ne.insert(pt):
            return True
        if self.sw.insert(pt):
            return True
        if self.se.insert(pt):
            return True

        return False

    def query(self, cell):
        found = []
        if not self.boundary.intersect(cell):
            return found

        for pt in self.points:
            if cell.contains(pt):
                found.append(pt)

        if self.divided:
            found.extend(self.ne.query(cell))
            found.extend(self.nw.query(cell))
            found.extend(self.se.query(cell))
            found.extend(self.sw.query(cell))

        return found

    def __str__(self):
        return str(self.query(self.boundary))
      
    def show(self):
        li = self.query(self.boundary)
        lo = []
        for item in li:
            lo.append([item.x, item.y])
        return lo