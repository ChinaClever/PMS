import numpy as np
import numpy as np

# 原始列表
data = [4, 4, 4, 4, nan, nan, 4, np.nan, 4, np.nan, 4, np.nan, '2023-12-19 13:30:13', '2023-12-19 13:30:15', 2, '2023-12-19 ', '2023-12-19 ']

# 替换nan为None
for i in range(len(data)):
    if isinstance(data[i], float) and np.isnan(data[i]):
        data[i] = None

print(data)
