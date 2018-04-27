import math;
from matplotlib import pyplot;
import random;

def divide(array, divLeft, divRight, return_left = False, return_right = False):
	region = {'left': [], 'right': []};

	a = divLeft[0] * divRight[1];
	d = divLeft[1] * divRight[0];

	for point in array:
		b = divLeft[1] * point[0];
		c = divRight[0] * point[1];
		e = divRight[1] * point[0];
		f = divLeft[0] * point[1];
		
		acc = (a + b + c) - (d + e + f); 

		if (acc > 0):
			region['left'].append(point);
		else:
			region['right'].append(point);

	if return_left:
		return region['left'];
	elif return_right:
		return region['right'];
	else:
		return region;

def point_distance(pa, pb):
	x = pa[0] - pb[0];
	y = pa[1] - pb[1];
	return math.sqrt((x * x) + (y * y));

def count_degrees(pa, pMid , pb):
	ea = point_distance(pMid, pa);
	eb = point_distance(pMid, pb);
	eMid = point_distance(pa, pb);

	cos_a = ((ea * ea) + (eb * eb) - (eMid * eMid)) / (2 * ea * eb);

	return math.acos(cos_a);

def make_line(left, right):
	gradien_pembilang = abs(right[1] - left[1]);
	gradien_penyebut = abs(right[0] - left[0]);
	konstanta_c = right[1] - (gradien_pembilang * right[0] / gradien_penyebut);

	coef_A = gradien_pembilang;
	coef_B = gradien_penyebut * (-1);
	coef_C = konstanta_c * gradien_penyebut;

	line = {'A': coef_A, 'B': coef_B, 'C': coef_C};
	return line;

def search_furthest(array, left, right):
	line = make_line(left, right);

	min_degrees = 360;
	index = None;

	i = 0;
	for point in array:
		degrees = count_degrees(left, point, right);
		if (degrees != 0):
			if (degrees < min_degrees):
				min_degrees = degrees;
				index = i;
		i = i + 1;
	return index; 

def point_comparation(a, b):
	if (a[0] < b[0]):
		return -1;
	elif (a[0] == b[0]):
		return 0;
	else:
		return 1;


def quicksort(array, compare = point_comparation, left = 0, right = None):
	if (right == None):
		right = len(array)-1;

	pivot = array[left];

	leftCursor = left;
	rightCursor = right;

	while (leftCursor < rightCursor):
		while ((compare(array[leftCursor], pivot) == -1) and (leftCursor < rightCursor)):
			leftCursor = leftCursor + 1;
		while ((compare(array[rightCursor], pivot) >= 0) and (leftCursor < rightCursor)):
			rightCursor = rightCursor - 1;
		if (leftCursor < rightCursor):
			temp = array[leftCursor];
			array[leftCursor] = array[rightCursor];
			array[rightCursor] = temp;
			leftCursor = leftCursor + 1;
			rightCursor = rightCursor - 1;

	if (leftCursor == rightCursor):
		if ((compare(array[leftCursor], pivot) >= 0) and (rightCursor != left)):
			rightCursor = rightCursor - 1;
		else:
			leftCursor = leftCursor + 1;

	if (rightCursor - left > 0):
		array = quicksort(array, compare, left, rightCursor);
	if (right - leftCursor > 0):
		array = quicksort(array, compare, leftCursor, right);

	return array;

def create_convex_hull(array_input, left = None, right = None, init = False):
	convex_hull = []; 

	array = list(array_input);
	if (0 <= len(array) <= 1):
		return array;

	if init:
		array = quicksort(array);

		left = array[0];
		right = array[len(array)-1];

		del array[len(array)-1];
		del array[0];

		region = divide(array, left, right);

		convex_hull.append(left);
		convex_hull.extend(create_convex_hull(region['left'], left, right));
		convex_hull.append(right);
		convex_hull.extend(create_convex_hull(region['right'], right, left));

		return convex_hull;
	else:
		furthest_point_index = search_furthest(array, left, right);

		furthest_point = array[furthest_point_index];

		del array[furthest_point_index];

		region_left = divide(array, left, furthest_point, return_left = True);
		region_right = divide(array, furthest_point, right, return_left = True);

		left_convex_hull = create_convex_hull(region_left, left, furthest_point);
		right_convex_hull = create_convex_hull(region_right, furthest_point, right);

		convex_hull.extend(left_convex_hull);
		convex_hull.append(furthest_point);
		convex_hull.extend(right_convex_hull);

		return convex_hull;

if __name__ == '__main__':
	n_point = int(raw_input("number of points: "));

	array = [];
	i = 0;
	while (i < n_point):
		x = random.randint(0, 100);
		y = random.randint(0, 100);
		if not ((x, y) in array):
			array.append((x, y));
			i = i + 1;
	array = quicksort(array);

	print "Points List:", array;
	convex_hull = create_convex_hull(array, init = True);
	print "Convex Hull:", convex_hull;

	x_points = [];
	y_points = [];
	for point in convex_hull:
		x_points.append(point[0]);
		y_points.append(point[1]);
		if point in array:
			array.remove(point);

	x_points.append(convex_hull[0][0]);
	y_points.append(convex_hull[0][1]);

	pyplot.plot(x_points, y_points, "r-");
	for point in array:
		pyplot.plot(point[0], point[1], "b.");

	pyplot.show();