# 定义原始 MAC 地址
original_mac = '00:11:22:33:44:5F'

# 将原始 MAC 地址拆分成每个部分
mac_parts = original_mac.split(':')

# 将每个部分转换为十六进制整数，并增加1
new_mac_parts = [hex(int(part, 16) + 1)[2:].zfill(2) for part in mac_parts]

# 连接每个部分并生成新的 MAC 地址
new_mac = ':'.join(new_mac_parts)

# 打印新的 MAC 地址
print(new_mac)