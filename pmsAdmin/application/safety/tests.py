# 定义原始 MAC 地址
original_mac = '01:12:23:34:45:60'

# 将原始 MAC 地址转换为十进制整数，并增加1
new_mac_int = (int(original_mac.replace(':', ''), 16) + 1) % (256**6)

# 将新的值转换为十六进制字符串，并保持12位长度
new_mac_str = hex(new_mac_int)[2:].zfill(12)

# 在每两位字符之间加上冒号并生成新的 MAC 地址
new_mac = ':'.join([new_mac_str[i:i+2] for i in range(0, len(new_mac_str), 2)])

# 打印新的 MAC 地址
print(new_mac)
