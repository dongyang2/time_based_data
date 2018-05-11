# 模型评估
import math


def mean_square_error(pre, ver):
    """均方误差"""
    len_p = len(pre)
    sums = 0
    for i in range(len_p):
        sums += pow((pre[i]-ver[i]), 2)
    return sums / len_p * 1.0


if __name__ == '__main__':
    # c1 = pow(2, 3)
    # print(c1)
    li1 = [1, 2, 3]
    li2 = [1.1, 2.2, 3.3, 4.4]
    print(mean_square_error(li1, li2))
