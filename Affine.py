def main():
    a = int(input("alpha value "))
    b = int(input("beta value "))
    n = int(input("n value "))

    # print(extended_euclidean_algorithm(17, 101))
    if validate_alpha(a, n):
        print(f"Alpha inverse: {extended_euclidean_algorithm(a, n)[1]}")


def validate_alpha(a: int, b: int):
    if euclidean_algorithm(a, b) > 1:
        return False
    return True


def euclidean_algorithm(a: int, b: int):
    if a < 0:
        return euclidean_algorithm(-a, b)
    if b < 0:
        return euclidean_algorithm(a, -b)
    if b == 0:
        return a
    return euclidean_algorithm(b, a % b)


def extended_euclidean_algorithm(a: int, b: int):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    mcd = b
    return mcd, x, y


if __name__ == '__main__':
    main()
