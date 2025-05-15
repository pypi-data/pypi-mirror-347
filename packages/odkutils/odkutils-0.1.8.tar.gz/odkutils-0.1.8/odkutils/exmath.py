import numpy as np
from scipy.stats import norm
from datetime import datetime

def bs_price(S, K, r, sigma, expiry_date, today=None):
    """
    计算 Black–Scholes 欧式看涨期权价格
    S: 标的现价
    K: 行权价
    r: 无风险年利率（小数）
    sigma: 波动率（小数）
    expiry_date: 到期日 (datetime.date 或 datetime.datetime)
    today: 计算基准日，默认使用当前系统日期
    """
    if today is None:
        today = datetime.utcnow()
    # 计算剩余时间 T（年）
    T = (expiry_date - today).days / 365.0
    # 防止 T <= 0
    if T <= 0:
        return max(S - K, 0.0)

    # 计算 d1, d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # 标准正态分布的累积分布函数
    N = norm.cdf
    # Black–Scholes 看涨期权公式
    call = S * N(d1) - K * np.exp(-r * T) * N(d2)
    put = K * np.exp(-r * T) * N(-d2) - S * N(-d1)  # Put option formula
    return call,put

# if __name__ == "__main__":
#     S = 95000.0
#     K = 100000.0
#     r = 0.03
#     sigma = 0.60
#     expiry = datetime(2025, 5, 30)

#     price = bs_price(S, K, r, sigma, expiry)
#     print(price)
