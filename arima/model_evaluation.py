# 模型评估
# import math
import sklearn.metrics as skm


def mean_square_error(pre, ver):
    """均方误差"""
    len_p = len(pre)
    sums = 0
    for i in range(len_p):
        sums += pow((pre[i]-ver[i]), 2)
    return sums / len_p * 1.0


def eval_sk(pre, ver, st):
    """

    :param pre: 预测值
    :param ver: 验证值
    :param st:  评估函数选择
                mse  - 均值平方误差 mean squared error
                evs  - 方差回归评分 explained variance regression score
                mae  - 均值绝对误差 mean absolute error
                msle - 均值平方对数误差 mean_squared_log_error
                r2   - 确定系数 R^2  score
                mdae - 中位数绝对误差 median absolute error
    """
    lp = len(pre)
    lv = len(ver)
    if lp <= lv:
        ver = ver[:lp]
    else:
        pre = pre[:lv]
    if st == 'mse':
        return skm.mean_squared_error(ver, pre)
    elif st == 'evs':
        return skm.explained_variance_score(ver, pre)
    elif st == 'mae':
        return skm.mean_absolute_error(ver, pre)
    elif st == 'msle':
        return skm.mean_squared_log_error(ver, pre)
    elif st == 'r2':
        return skm.r2_score(ver, pre)
    elif st == 'mdae':
        return skm.median_absolute_error(ver, pre)
    else:
        print('The function is not support!')
        return False


if __name__ == '__main__':
    # c1 = pow(2, 3)
    # print(c1)
    li1 = [1, 2, 3]
    li2 = [1.1, 2.2, 3.3, 4.4]
    # print(mean_square_error(li1, li2))
    print(eval_sk(li1, li2, 'mse'))
