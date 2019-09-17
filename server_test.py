import os
import time
import re


def get_server_name():
    '''
    获取配置的服务器名
    :return: 服务器列表
    '''
    server_names = [a.strip() for a in open('config_name.txt', 'r', encoding='utf-8').readlines()]
    return server_names


def get_server_ip():
    '''
    获取所有服务器ip和端口
    :return:
    '''
    verify_list = []
    server_names = get_server_name()
    with open('json_data.txt', 'r') as f:
        file_data = f.read()
    try:
        for name in server_names:
            regular = '(\w+\.){3}\w+[\s\S]{120,300}' + name
            regular = re.compile(regular, re.S)
            response = re.search(regular, file_data)
            if response is None:
                print('%s ip获取失败' % name)
                break
            response_data = response.group(0)

            # 获取 ip
            ip = '\d{2,3}\D\d{2,3}\D\d{2,3}\D\d{2,3}'  # ip regular
            ip_re = re.compile(ip, re.S)
            ip_key = re.search(ip_re, response_data).group(0)

            # 获取 port
            port = '"port":(\d{5})'  # port regular
            port_re = re.compile(port, re.S)
            port_key = re.search(port_re, response_data).group(0)[-5:]
            sever_ip = ip_key + ' ' + port_key
            print('已获取服务器 %s 的IP和端口: %s' % (name, sever_ip))
            os_dir = os.popen('java -jar ff.client.jar %s 1 None@-1' % sever_ip, 'r')
            # loading()

            if 'opened' in os_dir.read():
                print('%s 测试通过' % name)
                verify_list.append(name)
            else:
                print('%s 意料之外的错误' % name)
        if len(verify_list) == len(server_names):
            print('全部测试通过,成功 %s 个, list: %s' % (len(verify_list), verify_list))
        else:
            print('没全部通过')
        os.system('pause')
    except Exception as err:
        print(err)

if __name__ == '__main__':
    get_server_ip()
