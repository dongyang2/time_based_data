from arima import detect_op
from arima import modeling
from arima import model_evaluation
from database import file_op
import pandas
import copy
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts


def get_order(li):
    """获得一个数列的拟合方程的内生变量的阶数

    :param li: 数列
    :return 元组(a,b,c)分别是AR的阶数，差分次数，MA的阶数；
            ll1是差分后的平稳序列
            ll2是存储差分前最后一项的列表，用来还原到原序列
    """
    max_d = 12
    # max_lag = 5
    if len(li) > max_d:  # 最多做十次差分
        n = max_d - 2
    else:
        n = len(li) - 2
    d = 0

    ll1 = []  # 存储最后的平稳序列
    ll2 = []  # 存储每次差分前的列表的最后一项
    for i in range(n):
        tmp_li = copy.deepcopy(li)
        tmp_l = []
        lt, tmp_l = modeling.diff_cal_l(tmp_li, i, tmp_l)
        # print(lt)
        if detect_op.adf_test(lt) == 1:
            d = i
            ll1 = lt
            ll2 = tmp_l  # 如果是0次差分，则是空列表
            # print(ll2)
            break

    if d == n - 1:
        print('Difference calculate can not make it stationary!')
        return False

    if detect_op.random_test(ll1) is False:
        # print('The sequence is purely random process. Can not use ARMA.')
        return 'The sequence is purely random process.'

    fig_test = detect_op.fig_test_stat_mod(ll1)
    if fig_test[0] == 'AR':
        print('----------------AR model-------------------')
        return (fig_test[1], d, 0), ll1, ll2
    elif fig_test[0] == 'MA':
        print('----------------MA model-------------------')
        return (0, d, fig_test[1]), ll1, ll2
    elif fig_test[0] == 'same':
        return (fig_test[1][0], d, fig_test[1][1]), ll1, ll2
    else:
        # order = ts.arma_order_select_ic(ll1, max_ar=max_lag, max_ma=max_lag)
        # print(order.bic_min_order)
        order = ts.arma_order_select_ic(ll1)
        ord1, ord2 = order.bic_min_order
        return (ord1, d, ord2), ll1, ll2


def predict(filename, n):
    """用state model里的arima模型做预测

    :param filename: 文件名
    :param n: 预测值的个数
    :return: n个预测值
    """
    li_data = file_op.read_file(filename)
    prd = []
    for j, i in enumerate(li_data):
        if j == 20:
            break
        print('_________the %dth line_______________' % (j+1))
        a_data = detect_op.turn_to_np_float_64(i[1:], 1)
        model_order = get_order(a_data)
        print('the order is ', model_order[0])
        if model_order is not False:
            data = pandas.Series(model_order[1])
            data.index = pandas.date_range('2001-01-01', periods=len(data))
            order_ar = model_order[0][0]
            order_ma = model_order[0][2]
            # d_times = model_order[0][1]
            last_elem = model_order[2]  # 用来还原预测数据
            try:
                model = sm.tsa.ARMA(data, (order_ar, order_ma)).fit(disp=-1, maxiter=20)
                predict_ordinary = model.forecast(n)[0]
                prd.append(re_diff_cal(last_elem, predict_ordinary))
            except ValueError:
                prd.append('Can not get good order.')
            # for j in last_elem:
            #     predict_ordinary += j
        elif isinstance(model_order, str):
            prd.append(model_order)
    return prd


def re_diff_cal(la, pre):
    """逆差分运算

    :param la: 每次差分元算前的数列的最后一项组成的数列
    :param pre: 基于差分后的序列的预测值
    :return: 原序列的预测值
    """
    rst = [pre]
    n = len(la)
    i = 0
    while i < n:
        tmp = [la[-1 - i] + rst[i][0]]
        for j in rst[i][1:]:
            tmp.append(tmp[-1] + j)
        rst.append(tmp)
        i += 1
    return rst[-1]


def get_index_range(li):
    n = len(li)
    return str(1), str(n)


def get_result(pre, ver_fil):
    ver_li = file_op.read_file(ver_fil, is_num=1, del_first=1)

    li_re = []
    for ii, i in enumerate(pre):
        if isinstance(i, str) is False:
            # print(i, ver_li[ii])
            mse = model_evaluation.mean_square_error(i, ver_li[ii])
            li_re.append(mse)
        else:
            li_re.append(i)
    return li_re


if __name__ == '__main__':
    li1 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
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
    # li3 = detect_op.turn_to_np_float_64(li2, 1)

    filename1 = 'F:/database_needed/UCR_TS_Archive_2015/50words/50words_TRAIN'
    pre1 = predict(filename1, 2)
    # print(pre1)
    # li_data1 = file_op.read_file(filename1)
    # a_data0 = detect_op.turn_to_np_float_64(li_data1[0][1:], 1)
    # print(a_data0)
    # get_order(a_data0)

    # tmp_pre1 = [[-0.8158099732324016, -0.8117203958111989], 'Can not get good order.',
    #             [-0.9581913285719178, -0.9560450594916866], 'Can not get good order.', 'Can not get good order.',
    #             'Can not get good order.', 'Can not get good order.', 'Can not get good order.',
    #             'Can not get good order.', [-1.0627400619982441, -1.200295723663895], 'Can not get good order.',
    #             [-2.007030421739809, -2.0040700955664383], 'Can not get good order.', 'Can not get good order.',
    #             'Can not get good order.', 'Can not get good order.', 'Can not get good order.',
    #             [-0.9132767808307618, -0.9106131205267486], 'Can not get good order.', 'Can not get good order.']
    filename2 = 'F:/database_needed/UCR_TS_Archive_2015/50words/50words_TEST'
    # print(get_result(tmp_pre1, filename2))
