import math
import numpy as np
import matplotlib.pyplot as plt


class LinearEquation:
    def __init__(self, point1, point2):

        if point1.x == point2.x:
            slope = math.inf
            c = None
            x = point1.x
        else:
            slope = (point2.y - point1.y) / (point2.x - point1.x)
            c = point1.y - slope * point1.x
            x = None

        domain = [point1.x, point2.x]
        domain.sort()
        range_ = [point1.y, point2.y]
        range_.sort()

        self.slope = slope
        self.c = c
        self.x = x
        self.domain = domain
        self.range = range_

    def __str__(self):
        return "y = " + str(self.slope) + "x + " + str(self.c) + "\n or X = " + str(self.x) + "Domain = " + \
               str(self.domain) + " Range = " + str(self.range) + "\n\n"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + "\n\n"


class Boundary:
    pass


# distance between two points
def distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)


def longest_line_algorithm(points, spacing):
    # to store max distance
    max_dist = {
        "length": 0,
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0
    }

    # To find the max distance
    temp_dist = 0
    max_dist = 0
    for count, point in enumerate(points):

        if count + 1 < len(points):
            temp_dist = distance(point, points[count + 1])

            if temp_dist >= max_dist:
                max_dist = temp_dist
                max_dist_point1 = point
                max_dist_point2 = points[count + 1]
    # Find max distance end

    # start forming equation list
    equation_list = []

    for count, point in enumerate(points):
        if count + 1 < len(points):
            equation_list.append(LinearEquation(point, points[count + 1]))
            equation_list.sort(key=lambda a: a.domain[0])
    # equation list end

    # To find the beginning equation (the one describing the longest line)
    beginning_equation = LinearEquation(max_dist_point1, max_dist_point2)

    # List of intercepts
    intercept_points_above = []
    intercept_points_below = []

    # Scan for intercepts above the beginning equation
    intercept_counter = 1
    count = 0
    while not intercept_counter == 0:
        intercept_counter = 0

        for equation in equation_list:

            if not equation == beginning_equation and not beginning_equation.slope == equation.slope:
                # Otherwise there are infinite solutions

                if equation.x is None:
                    x = (equation.c - beginning_equation.c -
                         spacing * (count + 1) / math.cos(math.atan(beginning_equation.slope))) / \
                        (beginning_equation.slope - equation.slope)
                    y = equation.slope * x + equation.c
                    intercept_point = Point(x, y)

                    # To check if the intercept point is within the domain
                    if min(equation.domain) <= intercept_point.x <= max(equation.domain):
                        intercept_points_above.append(intercept_point)
                        intercept_counter = intercept_counter + 1

                else:
                    x = equation.x
                    y = beginning_equation.slope * x + beginning_equation.c + spacing * (count + 1) / \
                        math.cos(math.atan(beginning_equation.slope))
                    intercept_point = Point(x, y)

                    if min(equation.range) <= intercept_point.y <= max(equation.range):
                        intercept_points_above.append(intercept_point)
                        intercept_counter = intercept_counter + 1

        count = count + 1

    # to search below the beginning equation
    intercept_counter = 1
    count = 0

    while not intercept_counter == 0:
        intercept_counter = 0

        for equation in equation_list:

            if not equation == beginning_equation and not beginning_equation.slope == equation.slope:
                # Otherwise there are infinite solutions

                if equation.x is None:
                    x = (equation.c - beginning_equation.c +
                         spacing * (count + 1) / math.cos(math.atan(beginning_equation.slope))) / \
                        (beginning_equation.slope - equation.slope)
                    y = equation.slope * x + equation.c
                    intercept_point = Point(x, y)

                    # To check if the intercept point is within the domain
                    if min(equation.domain) <= intercept_point.x <= max(equation.domain):
                        intercept_points_below.append(intercept_point)
                        intercept_counter = intercept_counter + 1

                else:
                    x = equation.x
                    y = beginning_equation.slope * x + beginning_equation.c - spacing * (count + 1) / \
                        math.cos(math.atan(beginning_equation.slope))
                    intercept_point = Point(x, y)

                    if min(equation.range) <= intercept_point.y <= max(equation.range):
                        intercept_points_below.append(intercept_point)
                        intercept_counter = intercept_counter + 1
        count = count + 1

    # to sort the intercepts
    for count, point in enumerate(intercept_points_above):
        if count % 4 == 0 and (count < len(intercept_points_above) - 1):
            temp1 = intercept_points_above[count + 1]
            temp2 = point
            intercept_points_above[count], intercept_points_above[count + 1] = temp1, temp2

    for count, point in enumerate(intercept_points_below):
        if count % 4 == 0 and (count < len(intercept_points_below) - 1):
            temp1 = intercept_points_below[count + 1]
            temp2 = point
            intercept_points_below[count], intercept_points_below[count + 1] = temp1, temp2

    if intercept_points_below:
        intercept_points_below.insert(0, max_dist_point2)
        intercept_points_below.insert(0, max_dist_point1)

    if intercept_points_above:
        intercept_points_above.insert(0, max_dist_point1)
        intercept_points_above.insert(0, max_dist_point2)

    intercept_points_below.extend(intercept_points_above)

    return intercept_points_below


def polygon_split_search_algorithm(points):
    # travels clockwise around the polygon

    other_polygons = []

    def main_polygon(points_, at):
        main_polygon_list = []
        n = len(points_)

        while at + 1 < n:

            if at > 1 and not ccw(points_[at - 2], points_[at - 1], points_[at]):

                counter_clockwise = False
                original_at = at
                new_polygon = [points_[at - 1]]

                while counter_clockwise is False and at + 1 < n:
                    new_polygon.append(points_[at])
                    at = at + 1
                    counter_clockwise = ccw(points_[original_at - 2], points_[original_at - 1], points_[at])

                new_polygon.append(points_[at])
                new_polygon.append(new_polygon[0])
                other_polygons.append(new_polygon)

            main_polygon_list.append(points_[at])

            at = at + 1

        main_polygon_list.append(points_[at])

        return main_polygon_list

    polygons = [main_polygon(points, 0)]
    # polygons.extend(other_polygons)

    print(polygons[0])

    i = 0

    while i < len(other_polygons):
        polygons.append(main_polygon(other_polygons[i], 0))
        i = i + 1

    return polygons


def ccw(point_a, point_b, point_c):

    if (point_b.x - point_a.x) * (point_c.y - point_a.y) - (point_c.x - point_a.x) * (point_b.y - point_a.y) < 0:
        return True
    return False


# points = [Point(1, 1), Point(1, 4), Point(0, 5), Point(0, 7),Point(-0.5, 10), Point(4, 4), Point(4.5, 6), Point(5, 2), Point(4, 1)]
# points = [Point(1,0.5), Point(1,2), Point(3,2), Point(2,0.5)]
# points = [Point(2.76, 4.57), Point(7.05, 6.04), Point(7.8, 1.91), Point(1.98, 1.0)]
# points = [Point(.59, 3.17), Point(7.05, 6.04), Point(7.8, 1.91), Point(3.91, .2)]
# points = [Point(1.5, 1.0), Point(1.4,.8), Point(2.0, 1.0), Point(2.0, 2.0), Point(1.0, 2.0), Point(.5, 1.5)]
points = [Point(3.42, 5.65), Point(6.09, 5.8), Point(7.66, 4.18), Point(5.88, 2.37), Point(4.53, 1.51)]
# points = [Point(15, 21), Point(22, 26), Point(33, 25), Point(32, 15), Point(26, 7.5), Point(25, 13)]
# points = [Point(12.4, 40.1), Point(27.4, 57), Point(66.2, 50.2), Point(65.2, 29.3), Point(43.2, 10.7), Point(21.3, 17.2)]
points.append(points[0])

# # polygon splitter start
#
# x = []
# y = []
# for point in points:
#     x.append(point.x)
#     y.append(point.y)
#
# xs = []
# ys = []
# for point in polygon_split_search_algorithm(points)[3]:
#     xs.append(point.x)
#     ys.append(point.y)
#
# # print(*polygon_split_search_algorithm(points)[0])
# # print(ccw(Point(1,1), Point(1,4), Point(0,5)))
#
# plt.plot(xs, ys)
# plt.plot(x, y)
# plt.show()
# # polygon splitter end

# path finding start
intercepts = longest_line_algorithm(points, .5)
intercept_xs = []
intercept_ys = []

for intercept in intercepts:
    intercept_xs.append(intercept.x)
    intercept_ys.append(intercept.y)

xs = []
ys = []
for point in points:
    xs.append(point.x)
    ys.append(point.y)

sequence = np.arange(len(intercept_xs))

plt.figure()
plt.plot(xs, ys)
plt.plot(intercept_xs, intercept_ys)
plt.plot(intercept_xs[0], intercept_ys[0], marker="o")
plt.show()
# plt.close()
# path finding end

