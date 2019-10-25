















if __name__ == '__main__':
    a, b, c =[int (x) for x in input().split()]
    if a==b and b==c:
        print('Equilateral Triangle')
    elif (a==b) or (b==c) or (c==a):
        print('Isosceles Triangle')
    else:
        print('Bad Triangle')
