import socket
import json

def send_udp_data(json_data, host, port):
    # 将 JSON 数据转换为字节流
    json_bytes = json.dumps(json_data).encode('utf-8')

    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 发送数据
        sock.sendto(json_bytes, (host, port))
        print("数据发送成功")

    except socket.error as e:
        print(f"发送数据时出现错误: {e}")

    finally:
        # 关闭套接字
        sock.close()


if __name__ == '__main__':
    # 要发送的 JSON 数据
    data = {
        'softwareType': 'PDU-MonitorTest',
        'productType': 'IP-PDU_SNMPV3_液晶屏_交流_单相_香港DCL',
        'productSN': '000A 0021 0616 0001 0301',
        'macAddress': '2C:26:5F:3A:00:01',
        "testStep": [
            {
                "no": '1',
                "name": 'xxxx',
                "result": '1'
            },
            {
                "no": '2',
                "name": 'xxxdadadx',
                "result": '0'
            },
            {
                "no": '3',
                "name": 'xxasdsadxx',
                "result": '1'
            }
        ],
        "result": "1",
        "softwareVersion": "V1.0",
        "clientName": "香港DCL",
        "companyName": "clever",
        "protocolVersion": "V1.0",
        "testStartTime": "2023-11-09 9:37:20",
        "testEndTime": "2023-11-09 9:39:20",
        "testTime": "21"
    }

    # 设置目标主机和端口
    host = '127.0.0.1'  # 目标主机的 IP 地址
    port = 1234  # 目标端口号

    # 发送数据
    send_udp_data(data, host, port)