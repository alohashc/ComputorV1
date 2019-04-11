import sys
import re


def square_root(num):
    k = 1.0
    while (k*k - num) > 0.0000000001 or (num - k * k) > 0.0000000001:
        k = (k + num / k) / 2
    return k


def reduced(degree, c, b, a):
    if degree != 2:
        text = '{:+.1f} * X^0{:+.1f} * X^1 = 0'.format(c, b)
    else:
        text = '{:+.1f} * X^0{:+.1f} * X^1{:+.1f} * X^2 = 0'.format(c, b, a)
    if text[0] == '+':
        text = text[1:]
    text = text.replace('-', ' - ')
    text = text.replace('+', ' + ')
    return text


def main(equation):
    # print(equation)
    empty = re.compile(r'(\s*=\s*)')
    isEmpty = re.match(empty, equation)
    print(isEmpty)
    if isEmpty:
        exit('Invalid equation')
    parts = equation.split('=')
    # print(parts)
    if not len(parts) == 2:
        exit('There is no right part of equation')
    parts[0] += "="
    parts[0] = " " + parts[0]
    if re.findall('[xX]\^([3-9]|\d{2,})', equation):
        print("The polynomial degree is strictly greater than 2, I can't solve")
        sys.exit(0)
    power_2_matcher = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\^2')
    power_1_matcher = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\^1')
    power_1_matcher_1 = re.compile(r'([-+])\s*[Xx]\s*[-+=]')
    power_1_matcher_2 = re.compile(r'()^\s*[Xx]\s*[-+=]')
    power_0_matcher = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\^0')
    power_0_matcher_1 = re.compile(r'[^\^]\s*(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*[-+=]')

    a1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_2_matcher, parts[0]))))
    print("a1: {}".format(a1))
    b1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_1_matcher, parts[0]))))
    b1_1 = sum(map(float, map(lambda x: "-1" if x == "-" else "1", re.findall(power_1_matcher_1, parts[0]))))
    b1_2 = sum(map(float, map(lambda x: "1" if x == "+" else "1", re.findall(power_1_matcher_2, parts[0]))))
    print("b1: {}".format(b1))
    print("b1: {}".format(b1_1))
    print("b1: {}".format(b1_2))
    c1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_0_matcher, parts[0]))))
    c1_1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_0_matcher_1, parts[0]))))

    b1 = sum([b1, b1_1, b1_2])
    c1 = sum([c1, c1_1])
    print("c1: {}".format(c1))

    a2 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_2_matcher, parts[1])))) * (-1)
    print("a2: {}".format(a2))
    b2 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_1_matcher, parts[1])))) * (-1)
    print("b2: {}".format(b2))
    c2 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_0_matcher, parts[1])))) * (-1)
    print("c2: {}".format(c2))

    a = a1 + a2
    b = b1 + b2
    c = c1 + c2
    print('a = {}, b = {}, c = {}'.format(a, b, c))
    if a or b:
        degree = 2 if a else 1
    else:
        if c1 == -c2:
            exit('All real number are solutions')
        exit('No solutions')
    print('Reduced form: ', reduced(degree, c, b, a))
    print('Polynomial degree: ', degree)
    if degree == 2:
        d = b ** 2 - 4 * a * c
        print('D = {}'.format(d))
        print("x = {:.5f} [+|-] sqrt({:.3f}) / 2 * {:.3f}".format(-b, d, a))
        if d >= 0:
            x1 = (-b + square_root(d)) / (2 * a)
            x2 = (-b - square_root(d)) / (2 * a)
            print("The solution is:\nx1 = {:.5f}\nx2 = {:.5}".format(x1, x2))
        else:
            x1R = (-b / (2 * a))
            x1I = square_root(-d) / (2 * a)
            sign1 = "+" if x1I > 0 else "-"
            x2R = -b / (2 * a)
            x2I = -square_root(-d) / (2 * a)
            sign2 = "+" if x2I > 0 else "-"
            print("The solution is:\nx1 = {:.5f} {} {:.5f}*i\nx2 = {:.5f} {} {:.5}*i".format(abs(x1R), sign1, abs(x1I), abs(x2R), sign2, abs(x2I)))
    else:
        x = c / -b
        print("The solution is:\nx = {:.5f}".format(x))


if __name__ == "__main__":
    main(sys.argv[1])
