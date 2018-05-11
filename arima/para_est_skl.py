from sklearn import linear_model
import numpy


def get_para_least_sq(x, y):
    lr = linear_model.LinearRegression()  # 此处回归是使用最小二乘无疑
    x_t = numpy.transpose(x)

    lr.fit(x_t, y)
    li_pa = lr.coef_.tolist()
    li_pa.append(lr.intercept_)     # 姑且把这个当成常数项吧
    return li_pa


if __name__ == '__main__':
    reg = linear_model.LinearRegression()  # 此处回归是使用最小二乘无疑
    x1 = [[0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 5, -1]]
    x1_t = numpy.transpose(x1)
    y1 = [1, 5, 11, 16, 24, 10]

    reg.fit(x1_t, y1)
    print(type(reg.coef_))  # 这好像是中心化的回归，无法加入常数项
    print(reg.intercept_)  # 姑且把这个当成常数项吧
