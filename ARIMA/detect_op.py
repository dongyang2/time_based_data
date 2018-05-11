# 用来做平稳性检测，纯随机检测。
import math
from arima import statistical_properties as sp
from arima import modeling as mod
from statsmodels.stats.diagnostic import acorr_ljungbox
from database import file_op as fo
import numpy as np
import statsmodels.tsa.stattools as ts
import pandas
import statsmodels.api as sm


def adf_test(li, d=0):
    """单位根检验"""
    x = np.array(li)
    result_adf = ts.adfuller(x, d)  # 第一个值小于1%说明是平稳的，第二个（p值）越小越平稳
    # print(result_adf)
    if result_adf[0] < result_adf[4]['1%']:
        return 1  # 平稳
    elif result_adf[1] > 0.9 or result_adf[4]['1%'] < result_adf[0]:
        return 0  # 不平稳
    else:
        print('Consider other detection methods')
        return result_adf  # 出现错误，考虑其它检测方法


def fig_test_stat_mod(li):
    """图检验，此处偏相关系数借用了ts库中的函数"""
    bool_ar = 0
    bool_ma = 0
    standard = 2 * math.sqrt(sp.variance(li))
    # print('fig standard = ', standard)
    if len(li) > 42:
        n = 40
    else:
        n = len(li) - 2
    p_acf = ts.pacf(li, nlags=n)

    i = n
    while i > 0:
        if i == n and abs(p_acf[i]) > standard and abs(sp.acf(li, i)) > standard:
            break
        if abs(p_acf[i]) > standard:
            bool_ar = i
        if abs(sp.acf(li, i)) > standard:
            bool_ma = i
        i -= 1

    print('Figure test completed!')
    if bool_ar == 0 and bool_ma == 0:
        return 'failed', 0
    elif bool_ar != 0 and bool_ma != 0:
        # if bool_ar < bool_ma:
        #     return 'AR', bool_ar
        # elif bool_ma < bool_ar:
        #     return 'MA', bool_ma
        # else:
        #     return 'same', bool_ar
        return 'same', [bool_ar, bool_ma]
    else:
        if bool_ar:
            return 'AR', bool_ar
        else:
            return 'MA', bool_ma


def li_pos(li, up_num):
    """让二维列表中每个元素加一个很大的值"""
    for i in li:
        for j in i:
            j = float(j) + up_num
    return li


def li_u32(li, multiple, up_num, tmp, d):
    """让一维或者二维列表每个元素加一个大数再乘以一个整数"""
    if d == 1:
        for j in li:
            j = round((float(j) + up_num) * multiple)
            tmp.append(np.float64(j))
        return tmp
    elif d == 2:
        for i in li:
            tmp_i = []
            for j in i:
                j = round((float(j) + up_num) * multiple)
                tmp_i.append(np.float64(j))
            tmp.append(tmp_i)
        return tmp


def turn_to_np_float_64(li, d):
    """让列表中每个元素变为float64的"""
    np_f64 = []
    if d == 1:
        for i in li:
            np_f64.append(np.float64(i))
        return np_f64
    if d == 2:
        for i in li:
            tmp = []
            for j in i:
                tmp.append(np.float64(j))
            np_f64.append(tmp)
        return np_f64


def random_test(li):
    """纯随机性检验"""
    # print(u'差分序列的白噪声检验结果为：', acorr_ljungbox(li, lags=1))
    al = acorr_ljungbox(li, lags=1)[1]
    # print(al[0])
    if al[0] < 0.05:  # 不是纯随机序列,可以用ARMA
        return True
    else:
        return False


def get_min_from_2d_list(li):
    """获得二维列表中最小元素的值和下标"""
    m = li[0][0]
    subs1 = 0
    subs2 = 0
    for ii, i in enumerate(li):
        for jj, j in enumerate(i):
            if m > j:
                m = j
                subs1 = ii
                subs2 = jj
    return m, subs1, subs2


if __name__ == '__main__':
    li1 = [1, 2, 2, 1, 1]
    li2 = [10930, 10318, 10595, 10972, 7706, 6756, 9092, 10551, 9722,
           10913, 11151, 8186, 6422, 6337, 11649, 11652, 10310, 12043,
           7937, 6476, 9662, 9570, 9981, 9331, 9449, 6773, 6304, 9355,
           10477, 10148, 10395, 11261, 8713, 7299, 10424, 10795, 11069,
           11602, 11427, 9095, 7707, 10767, 12136, 12812, 12006, 12528,
           10329, 7818, 11719, 11683, 12603, 11495, 13670, 11337, 10232,
           13261, 13230, 15535, 16837, 19598, 14823, 11622, 19391, 18177,
           19994, 14723, 15694, 13248, 9543, 12872, 13101, 15053, 12619,
           13749, 10228, 9725, 14729, 12518, 14564, 15085, 14722, 11999,
           9390, 13481, 14795, 15845, 15271, 14686, 11054, 10395]
    # print(len(li2))
    adf1 = adf_test(li1)
    # print(adf1[0], type(adf1[0]))
    # print(adf1)

    # r1 = ts.pacf(li2).tolist()
    # print(r1)
    # print(fig_test_stat_mod(li2))

    # train = li2[:20]
    # history = [x for x in train]    # 这句话应该等于深复制
    # print(history)

    # dta = pandas.Series(li1)
    # print(dta)

    # dat = fo.read_file('F:/database_needed/UCR_TS_Archive_2015/50words/50words_TEST')
    # print(type(dat))

    # li3 = [[0.25362463476234746123461236461236426, 8.26347146123461234436324723726,
    #        9.215612361234612612641261461246123462316246321, 3.423673471374374717162464235],
    #        [0.43613427642172512345462374363416, 0.436712373716423127235235634612636216256]]
    # print(li_precision_control(li3, 16))

    li3 = []
    # print(li_u32([li1], 100, 0, li3, 2))

    # print(extended_acf(li2))
    # li3 = turn_to_np_float_64(li2, 1)
    # # print(get_order(li2)[0])
    # # model_order1 = get_order(li3)
    # model_order1 = False
    # if model_order1 is not False:
    #     data1 = pandas.Series(model_order1[1])
    #
    #     order_ar1 = model_order1[0][0]
    #     order_ma1 = model_order1[0][2]
    #     # data.index = pandas.DatetimeIndex(data.index)
    #     # ind = get_index_range(data)
    #     # data.index = pandas.Index(sm.tsa.datetools.dates_from_range(ind[0], ind[1]))  # 转化为Datetime index
    #     data1.index = pandas.date_range('2001-01-01', periods=len(li3))  # 使用这个data range主要是为了加freq标签
    #     # for i1 in data.index:
    #     #     print(i1)
    #     # print(data.index)
    #     # model = sta.ARMA(data, (order_ar, order_ma)).fit()  # 这个sta里面的ARMA不如sm.tsa里面的好用，亲测
    #     model1 = sm.tsa.ARMA(data1, (order_ar1, order_ma1)).fit(maxiter=20, disp=0)
    #     result = model1.forecast(5)
    #     print(result)

    print(random_test(li2))
