import numpy as np

def gini_coefficient(values):
    """
    计算Gini系数，用于衡量持仓集中度
    
    参数:
        values: numpy array或list，包含需要计算Gini系数的数值
        
    返回:
        float: Gini系数，范围在0到1之间
        - 0表示完全平均分布
        - 1表示完全集中分布
    """
    # 确保输入为numpy数组
    values = np.array(values)
    
    # 处理空值或负值
    if len(values) == 0 or np.any(values < 0):
        return 0
    
    # 如果所有值都为0，返回0
    if np.sum(values) == 0:
        return 0
    
    # 对数据进行排序
    values = np.sort(values)
    n = len(values)
    
    # 计算洛伦兹曲线下的面积
    index = np.arange(1, n + 1)
    lorenz = np.cumsum(values) / np.sum(values)
    
    # 计算Gini系数
    # Gini = (A - B) / A，其中A = 0.5，B是洛伦兹曲线下的面积
    B = np.sum(lorenz[:-1]) / n
    gini = 1 - 2 * B
    
    return round(gini, 4)