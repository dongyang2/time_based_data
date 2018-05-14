from arima import detect_op
from arima import modeling
from arima import model_evaluation
from database import file_op
import pandas
import copy
import numpy
import statsmodels.api as sm


def get_order(li):
    """获得一个数列的拟合方程的内生变量的阶数

    :param li: 数列
    :return 元组(a,b,c)分别是AR的阶数，差分次数，MA的阶数；
            ll1是差分后的平稳序列
            ll2是存储差分前最后一项的列表，用来还原到原序列
    """
    max_d = 12
    max_lag = 10
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
        order = sm.tsa.arma_order_select_ic(ll1, max_ar=max_lag, max_ma=max_lag)
        # print(order.bic_min_order)
        # order = ts.arma_order_select_ic(ll1)
        ord1, ord2 = order.bic_min_order
        return (ord1, d, ord2), ll1, ll2


def predict(filename, n):
    """用state model里的arima模型做预测

    :param filename: 文件名
    :param        n: 预测值的个数
    :return: n个预测值
    """
    li_data = file_op.read_file(filename)
    prd = []
    for j, i in enumerate(li_data):
        if j == 20:
            break
        print('_________the %dth line_______________' % (j + 1))
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
    """获得一个列表，存入均方误差得分和没有预测的原因

    :param pre:     预测的序列
    :param ver_fil: 验证文件名
    """
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


# 先验知识
# 1.在之前错误的EACF方法下，发现不少序列可以跑出来
# 2.在改进的EACF方法下，仍有不少序列跑不出来，可能和AR拟合相关，还可能和阈值选择相关
# 3.在库中自带找阶的方法下，跑出来的序列更少了，但和先验知识1能跑出来的似乎不重叠
# 于是我想到了干脆暴力搜索可行的阶数，然后根据均方误差获得好的阶数，至于均方误差的获得，可以切分测试集来获得
def get_stationary(li):
    """获得平稳序列"""
    max_d = 12
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
        if detect_op.adf_test(lt) == 1:
            d = i
            ll1 = lt
            ll2 = tmp_l  # 如果是0次差分，则是空列表
            break

    if d == n - 1:
        return -1, 'Difference calculate can not make it stationary!'

    if detect_op.random_test(ll1) is False:
        return -1, 'The sequence is purely random process.'

    return ll1, ll2


def slice_li(li, rat, rnd=True):
    """切分序列"""
    len_li = len(li)
    if rnd is True:
        result_num = round(len_li * rat / 10)
    else:
        result_num = len_li * rat / 10 * 1.0
    prev_li = []
    lat_li = []
    for h, i in enumerate(li):
        if h + 1 <= result_num:
            prev_li.append(i)
        else:
            lat_li.append(i)
    return prev_li, lat_li


def brute_predict(file, n, ratio=1):
    """暴力搜索可行阶，然后预测"""
    li_data = file_op.read_file(file)
    max_lag = 10
    rlt = []
    for j, i in enumerate(li_data):
        if j == 20:
            break
        a_data = detect_op.turn_to_np_float_64(i[1:], 1)
        sta_data, dif_elem = get_stationary(a_data)
        if isinstance(sta_data, list):
            test_data, val_data = slice_li(sta_data, 10 - ratio, False)
            data = pandas.Series(test_data)
            data.index = pandas.date_range('2001-01-01', periods=len(data))
            tmp_pre = []
            tmp_ord = []
            for k in range(max_lag):
                for m in range(max_lag):
                    try:
                        model = sm.tsa.ARMA(data, (k, m)).fit(disp=-1, maxiter=10)
                        pre = model.forecast(len(val_data))[0]
                        tmp_pre.append(pre)
                        tmp_ord.append((k, m))
                    except numpy.linalg.linalg.LinAlgError:
                        continue
                    except ValueError:
                        continue
                    else:
                        pre = model.forecast(len(val_data))[0]
                        tmp_pre.append(pre)
                        tmp_ord.append((k, m))
            tmp_mse = []
            o = 0
            if len(tmp_pre):  # 数组不空，则有阶数可用，然后找合适的阶
                for k in tmp_pre:
                    tmp_mse.append(model_evaluation.mean_square_error(k, val_data))
                    o = get_min_li(tmp_mse)[1]  # 找到均方误差小的那一组
                try:
                    fin_data = pandas.Series(test_data)
                    fin_data.index = pandas.date_range('2001-01-01', periods=len(fin_data))
                    fin_mod = sm.tsa.ARMA(fin_data, tmp_ord[o]).fit(disp=-1, maxiter=20)
                except ValueError:
                    rlt.append('Can not get good order.')
                except numpy.linalg.linalg.LinAlgError:
                    rlt.append('Can not get good order.')
                else:
                    fin_pre = fin_mod.forecast(n)[0]
                    fin = re_diff_cal(dif_elem, fin_pre)
                    rlt.append(fin)
            else:
                rlt.append('Can not get good order.')
        else:
            rlt.append(dif_elem)
    return rlt


def get_min_li(li):
    """获得一维列表中最小元素的值和下标"""
    if len(li) == 0:
        print('The list has nothing.')
        return False
    m = li[0]
    sub = 0
    for ii, i in enumerate(li):
        if m > i:
            m = i
            sub = ii
    return m, sub


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
    # pre1 = predict(filename1, 2)
    # print(pre1)
    li_data1 = file_op.read_file(filename1)
    a_data0 = detect_op.turn_to_np_float_64(li_data1[0][1:], 1)

    # brute get order
    # test_data, val_data = slice_li(a_data0, 2)
    # data1 = pandas.Series(test_data)
    # data1.index = pandas.date_range('2001-01-01', periods=len(data1))
    # max_lag = 5
    # tmp_pre = []
    # tmp_ord = []
    # for k in range(max_lag):
    #     for m in range(max_lag):
    #         if k != 0 or m != 0:
    #             # print(k, m)
    #             try:
    #                 model = sm.tsa.ARMA(data1, (k, m)).fit(disp=-1, maxiter=5)
    #             except numpy.linalg.linalg.LinAlgError:
    #                 continue
    #             except ValueError:
    #                 continue
    #             else:
    #                 pre = model.forecast(len(val_data))[0]
    #                 tmp_pre.append(pre)
    #                 tmp_ord.append((k, m))
    # # print(tmp_pre)
    # # print(tmp_ord)
    # tmp_mse = []
    # if len(tmp_pre):
    #     for k in tmp_pre:
    #         tmp_mse.append(model_evaluation.mean_square_error(k, val_data))
    # o = get_min_li(tmp_mse)[1]
    # print(tmp_mse)
    # print(tmp_ord[o])

    # brute predict
    print(brute_predict(filename1, 2))

    # or1 = sm.tsa.arma_order_select_ic(a_data0, ic=['aic', 'bic'], trend='nc')

    # print(or1.bic_min_order)
    # model1 = sm.tsa.ARMA(a_data0, or1.bic_min_order).fit(disp=-1, maxiter=20)
    # predict_ordinary = model.forecast(2)[0]

    # get_order(a_data0)

    filename2 = 'F:/database_needed/UCR_TS_Archive_2015/50words/50words_TEST'
    pre1 = [[-0.8105819333010666, -0.7900895082833033], [-0.7556184333185776, -0.7409519460065357],
            [-0.9564858328670514, -0.9472688304457626], [-1.1235940500529389, -1.1070495163349725],
            [-0.7865809017870451, -0.9985518027687232], [-1.509406842581641, -1.5260275358872977],
            [-1.1410641959963612, -1.2126113199855548], [-1.3154250514670507, -1.3035830257722325],
            [-1.0857707777621468, -1.0881655880490648], [-1.0383072069502843, -1.1527097274337177],
            [-0.8195715198822983, -0.8348941542249685], [-2.0066988989230765, -2.0043165249729107],
            [-1.4295934900892475, -1.769872259380202], [-1.0269551580428111, -0.9722040055748346],
            [-0.8643753477528209, -0.9641709817869812], [-1.6401574812088096, -1.736739224006919],
            [-1.3051195266235711, -1.3010912563017427], [-0.9130733590960547, -0.910998833792175],
            [-1.0253633417230932, -1.072950829532926], [-1.0774536512878385, -1.1858535137004163]]
    # print(get_result(pre1, filename2))

    # from statsmodels.tsa.arima_process import arma_generate_sample
    # arparams = np.array([.75, -.25])
    # maparams = np.array([.65, .35])
    # arparams = np.r_[1, -arparams]
    # maparam = np.r_[1, maparams]
    # nobs = 250
    # np.random.seed(2014)
    # y = arma_generate_sample(arparams, maparams, nobs)
    # res = sm.tsa.arma_order_select_ic(y, ic=['aic', 'bic'], trend='nc')
    # # res.aic_min_order
    # print(res.bic_min_order)
