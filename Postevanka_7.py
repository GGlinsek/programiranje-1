for n in range(1, 101):
    a = [int(x) for x in str(n)]
    if n%7 == 0 or 7 in a:
        print("BUM")
    else:
        print(n)
