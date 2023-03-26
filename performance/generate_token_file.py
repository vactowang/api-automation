from performance.common.get_bid_token_for_real_time import exec_function as r_exec
from performance.common.get_bid_token import exec_function as pre_exec
import json
from settings import get_root
from settings import test_common_os


def main(name=None):
    file_root = get_root + '\\performance'
    if name is not None:
        data = r_exec()
    else:
        data = pre_exec()

    for key, value in data.items():
        json_file = test_common_os+'_'+key+'_bid_token.json'
        json_file_path = file_root+'\\'+json_file
        update_file(json_file_path, value)


def update_file(file_path, data):
    if not file_path:
        return False
    f = open(file_path, 'a+')
    f.seek(0)
    all_data = f.read()
    new_data = all_data.replace(all_data, str(data))
    f.seek(0)
    f.truncate()
    json_str = json.dumps(eval(new_data), indent=4, separators=(',', ':'))
    f.write(json_str)
    f.flush()
    f.close()


if __name__ == '__main__':
    main()