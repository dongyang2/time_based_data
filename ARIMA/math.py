# 包含了求均值，方差，自协方差和自相关系数的函数。


def list_mean(li):
    """平均值"""
    s = 0
    for i in li:
        s += i
    return s/len(li)*1.0        # 返回结果保留小数点后15位


def list_variance(li):
    """方差"""
    mean = list_mean(li)
    s = 0
    for i in li:
        s += (i - mean)*(i - mean)
    return s/len(li)*1.0


def list_autocov(li):
    pass


if __name__ == '__main__':
    li1 = [1, 4, 9]
    print(list_mean(li1))
