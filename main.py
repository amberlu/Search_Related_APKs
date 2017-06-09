import argparse
from category import *
from developer import *
from datetime import datetime

def _parse_args():
    parser = argparse.ArgumentParser(description="Output all related package names, given a developer or category")
    parser.add_argument("--num_dev", help="Enter the number version of the interested developer ID here")
    parser.add_argument("--str_dev", help="Enter the str version of the interested developer ID here")
    parser.add_argument("--category", help="Enter the interested category name here")
    return parser.parse_args()

def _write_related(name, apk_lst):
    with open( 'outputs/' + name + '.txt', 'w') as f:
        for apk in apk_lst:
            f.write(apk + '\n')

if __name__ == "__main__":
    args = _parse_args()
    output = None
    
    t = datetime.now()
    now = t.strftime('%Y_%m_%d')
    logging.basicConfig(filename = 'logs/'+now+'.log', level=logging.DEBUG)

    if args.num_dev:
        output = get_developer_related(args.num_dev, type=0)
        _write_related('dev_num/' + args.num_dev, output)
    elif args.str_dev:
        output = get_developer_related(args.str_dev, type=1)
        _write_related('dev_str/' + args.str_dev, output)
    elif args.category:
        output = get_category_related(args.category)
        _write_related('categories/' + args.category, output)
    assert output is not None

