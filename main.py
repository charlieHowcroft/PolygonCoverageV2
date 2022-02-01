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
        # else:
        #     # orientation = orientation % 360
        #
        #     if orientation == 0 or 180 or 360:
        #         slope = math.inf
        #         c = None
        #         x = point1.x
        #         domain = None
        #         range_ = None
        #
        #     else:
        #         slope = 1 / math.tan(orientation)
        #         c = point1.y - slope*point1.x
        #         x = None
        #         domain = None
        #         range_ = None

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


class Hole:
    pass


# distance between two points
def distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)


def choose_orientation_algorithm(points, spacing, orientation):

    # User will specify the orientation (True North angle) and that will determine the slope
    # Algorithm will then pick the first point in the polygon getting searched and search above and below the line
    # start forming equation list
    equation_list = []

    for count, point in enumerate(points):
        if count + 1 < len(points):
            equation_list.append(LinearEquation(point, points[count + 1]))

    equation_list.sort(key=lambda a: (a.domain[0], a.domain[1]))
    # equation list end

    # To find the beginning equation (the one describing the orientation line)
    x = points[0].x + 1
    y = (1 / math.tan(orientation)) * x
    beginning_equation = LinearEquation(points[0], Point(x, y))

    # List of intercepts
    intercept_points_above = []
    intercept_points_below = []

    # Scan for intercepts above the beginning equation
    intercept_counter = 1
    count = 0
    a = 0

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

                        if a > 1:
                            if intercept_point.x == intercept_points_above[a - 1].x and \
                                    intercept_point.y == intercept_points_above[a - 1].y:
                                intercept_points_above.pop()
                                a = a - 1
                        a = a + 1

                else:
                    x = equation.x
                    y = beginning_equation.slope * x + beginning_equation.c + spacing * (count + 1) / \
                        math.cos(math.atan(beginning_equation.slope))
                    intercept_point = Point(x, y)

                    if min(equation.range) <= intercept_point.y <= max(equation.range):
                        intercept_points_above.append(intercept_point)
                        intercept_counter = intercept_counter + 1

                        if a > 1:
                            if intercept_point.x == intercept_points_above[a - 1].x and \
                                    intercept_point.y == intercept_points_above[a - 1].y:
                                intercept_points_above.pop()
                                a = a - 1
                        a = a + 1

        count = count + 1

    # to search below the beginning equation
    intercept_counter = 1
    count = 0
    a = 0

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

                        if a > 0:
                            if intercept_point.x == intercept_points_below[a - 1].x and \
                                    intercept_point.y == intercept_points_below[a - 1].y:
                                intercept_points_below.pop()
                                a = a - 1
                        a = a + 1

                else:
                    x = equation.x
                    y = beginning_equation.slope * x + beginning_equation.c - spacing * (count + 1) / \
                        math.cos(math.atan(beginning_equation.slope))
                    intercept_point = Point(x, y)

                    if min(equation.range) <= intercept_point.y <= max(equation.range):
                        intercept_points_below.append(intercept_point)
                        intercept_counter = intercept_counter + 1

                        if a > 1:
                            if intercept_point.x == intercept_points_below[a - 1].x and \
                                    intercept_point.y == intercept_points_below[a - 1].y:
                                intercept_points_below.pop()
                                a = a - 1
                        a = a + 1
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

    # if intercept_points_below:
    #     intercept_points_below.insert(0, max_dist_point2)
    #     intercept_points_below.insert(0, max_dist_point1)
    #
    # if intercept_points_above:
    #     intercept_points_above.insert(0, max_dist_point1)
    #     intercept_points_above.insert(0, max_dist_point2)

    intercept_points_below.extend(intercept_points_above)
    return intercept_points_below


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

    equation_list.sort(key=lambda a: (a.domain[0], a.domain[1]))
    # equation list end

    # To find the beginning equation (the one describing the longest line)
    beginning_equation = LinearEquation(max_dist_point1, max_dist_point2)

    # List of intercepts
    intercept_points_above = []
    intercept_points_below = []

    # Scan for intercepts above the beginning equation
    intercept_counter = 1
    count = 0
    a = 0

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

                        if a > 1:
                            if intercept_point.x == intercept_points_above[a - 1].x and \
                                    intercept_point.y == intercept_points_above[a - 1].y:
                                intercept_points_above.pop()
                                a = a - 1
                        a = a + 1

                else:
                    x = equation.x
                    y = beginning_equation.slope * x + beginning_equation.c + spacing * (count + 1) / \
                        math.cos(math.atan(beginning_equation.slope))
                    intercept_point = Point(x, y)

                    if min(equation.range) <= intercept_point.y <= max(equation.range):
                        intercept_points_above.append(intercept_point)
                        intercept_counter = intercept_counter + 1

                        if a > 1:
                            if intercept_point.x == intercept_points_above[a - 1].x and \
                                    intercept_point.y == intercept_points_above[a - 1].y:
                                intercept_points_above.pop()
                                a = a - 1
                        a = a + 1

        count = count + 1

    # to search below the beginning equation
    intercept_counter = 1
    count = 0
    a = 0

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

                        if a > 0:
                            if intercept_point.x == intercept_points_below[a - 1].x and \
                                    intercept_point.y == intercept_points_below[a - 1].y:
                                intercept_points_below.pop()
                                a = a - 1
                        a = a + 1

                else:
                    x = equation.x
                    y = beginning_equation.slope * x + beginning_equation.c - spacing * (count + 1) / \
                        math.cos(math.atan(beginning_equation.slope))
                    intercept_point = Point(x, y)

                    if min(equation.range) <= intercept_point.y <= max(equation.range):
                        intercept_points_below.append(intercept_point)
                        intercept_counter = intercept_counter + 1

                        if a > 1:
                            if intercept_point.x == intercept_points_below[a - 1].x and \
                                    intercept_point.y == intercept_points_below[a - 1].y:
                                intercept_points_below.pop()
                                a = a - 1
                        a = a + 1
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
    other_polygons = []

    def main_polygon(points_, at):
        main_polygon_list = []
        n = len(points_)

        while at + 1 < n:

            if at > 1 and ccw(points_[at - 2], points_[at - 1], points_[at]):

                counter_clockwise = True
                original_at = at
                new_polygon = [points_[at - 1]]

                while counter_clockwise is True and at + 1 < n:
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

    i = 0

    while i < len(other_polygons):
        polygons.append(main_polygon(other_polygons[i], 0))
        i = i + 1

    return polygons


def ccw(point_a, point_b, point_c):
    if (point_b.x - point_a.x) * (point_c.y - point_a.y) - (point_c.x - point_a.x) * (point_b.y - point_a.y) < 0:
        return False
    return True


# points = [Point(1, 1), Point(1, 4), Point(0, 5), Point(0, 7), Point(-0.5, 10), Point(4, 4), Point(4.5, 6), Point(5, 2),
#           Point(4, 1)]
points = [Point(1,0.5), Point(1,2), Point(3,2), Point(2,0.5)]
# points = [Point(2.76, 4.57), Point(7.05, 6.04), Point(7.8, 1.91), Point(1.98, 1.0)]
# points = [Point(.59, 3.17), Point(7.05, 6.04), Point(7.8, 1.91), Point(3.91, .2)]
# points = [Point(1.5, 1.0), Point(1.4,.8), Point(2.0, 1.0), Point(2.0, 2.0), Point(1.0, 2.0), Point(.5, 1.5)]  #bugged
# points = [Point(3.42, 5.65), Point(6.09, 5.8), Point(7.66, 4.18), Point(5.88, 0), Point(4.53, 1.51)]  # Bugged
# points = [Point(1.5, 2.1), Point(2.2, 2.6), Point(3.3, 2.5), Point(3.2, 1.5), Point(2.6, .75),
#           Point(2.5, 1.3)]  # Bugged
# points = [Point(1.24, 4.01), Point(2.74, 5.7), Point(6.62, 5.02), Point(6.52, 2.93), Point(4.32, 1.07), Point(2.13, 1.72)]
points.append(points[0])


def plotter(boundary_points, search_polygons, orientation=None):

    boundary_points_x = []
    boundary_points_y = []
    for point in boundary_points:
        boundary_points_x.append(point.x)
        boundary_points_y.append(point.y)

    search_polygons_x_y = []
    for search_polygon in search_polygons:
        search_polygon_x = []
        search_polygon_y = []

        for point in search_polygon:
            search_polygon_x.append(point.x)
            search_polygon_y.append(point.y)
        search_polygons_x_y.append([search_polygon_x, search_polygon_y])

    intercept_x_y = []
    for search_polygon in search_polygons:
        if orientation is None:
            intercepts = longest_line_algorithm(search_polygon, .5)
        else:
            intercepts = choose_orientation_algorithm(search_polygon, .5, orientation)
        intercept_xs = []
        intercept_ys = []

        for intercept in intercepts:
            intercept_xs.append(intercept.x)
            intercept_ys.append(intercept.y)

        intercept_x_y.append([intercept_xs, intercept_ys])

    # Boundary plotting start

    plt.plot(boundary_points_x, boundary_points_y)
    plt.title("Original Boundary")
    # plt.axis("off")
    plt.show()

    for path in intercept_x_y:
        plt.plot(boundary_points_x, boundary_points_y)
        plt.plot(path[0], path[1])
        plt.show()


def menu1():
    print("[1] Enter your own polygon")
    print("[2] Select preset polygon")
    print("[0] Exit the program")


def add_point_menu():
    print("[1] Add a point")
    print("[2] Finish Polygon")


def main():
    print("This script shows the path calculated for the given polygon.\n"
          "If the path is un-desirable or bugged you can re calculate.\n")

    menu1()
    option = int(input("Enter your option: "))

    while option != 0:

        if option == 1:

            points.clear()

            while option != 2 or len(points) < 3:

                if option == 2:
                    print("Enter at least 3 points")

                add_point_menu()
                option = int(input("Select: "))

                if option == 1:
                    x = int(input("X: "))
                    y = int(input("Y: "))
                    points.append(Point(x, y))

            points.append(points[0])

            plotter(points, polygon_split_search_algorithm(points))
            print("Do you want to recompute path with different sub polygons?\n[1]: yes\n[2]: no")
            option = int(input("Enter: "))

            while option == 1:
                points.pop(0)
                points.append(points[0])
                plotter(points, polygon_split_search_algorithm(points))
                print("Do you want to recompute path with different sub polygons?\n[1]: yes\n[2]: no")
                option = int(input("Enter: "))

        elif option == 2:

            print("Do you want to choose the orientation? (degrees true north)")
            print("[1] Yes\n[2] No")
            option = int(input("[Y/N]"))

            if option == 1:
                orientation = int(input("Enter orientation"))
                plotter(points, polygon_split_search_algorithm(points), orientation)

            else:
                plotter(points, polygon_split_search_algorithm(points))

            print("Do you want to recompute path with different sub polygons?\n[1]: yes\n[2]: no")
            option = int(input("Enter: "))

            while option == 1:
                points.pop(0)
                points.append(points[0])
                plotter(points, polygon_split_search_algorithm(points))
                print("Do you want to recompute path with different sub polygons?\n[1]: yes\n[2]: no")
                option = int(input("Enter: "))
        else:
            print("Invalid Option, Enter again")

        menu1()
        option = int(input("Enter your option: "))

main()

