# n, m = map(int, raw_input().split(' '))
# a = map(int, raw_input().split(' '))
m = 10
a = [5, 6, 10]
ans = 0

def cal(a, b, m, t):
    global ans
    if t == -1:
        return
    tt = 2 ** t
    a1 = [x ^ tt for x in a if x & tt]
    a0 = [x for x in a if not x & tt]
    b1 = [x ^ tt for x in b if x & tt]
    b0 = [x for x in b if not x & tt]

    print a
    print b
    print m
    print t
    print tt
    print a1
    print a0
    print b1
    print b0

    if m & tt:
        cal(a0, b1, m ^ tt, t - 1)
        cal(a1, b0, m ^ tt, t - 1)
    else:
        ans += len(a0) * len(b1) + len(a1) * len(b0)
        cal(a0, b0, m, t - 1)
        cal(a1, b1, m, t - 1)

cal(a, a, m, 4)
print ans / 2