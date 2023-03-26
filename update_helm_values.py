from ruamel import yaml
import getopt
import sys


def main(argvs):
    values_file = './performance/locust-charts-vungle-v0.1/values.yaml'
    # Open values.yaml
    try:
        opts, args = getopt.getopt(argvs, '', ['service=', 'host=', 'users=', 'spawnRate=', 'runtime=',
                                               'replicas=', 'branch=', 'headless='])
    except getopt.GetoptError as ex:
        raise ex
    try:
        with open(values_file, encoding="utf-8") as f:
            content = yaml.load(f, Loader=yaml.RoundTripLoader)
        for opt, arg in opts:
            if opt in ('--service',):
                name = arg + '-locust'
                locust_locustfile = arg + '_service.py'
                content['loadtest']['name'] = name
                print('set loadtest.name to %s' % name)
                content['loadtest']['locust_locustfile'] = locust_locustfile
                print('set loadtest.locust_locustfile to %s' % locust_locustfile)
            elif opt in ('--host',):
                content['loadtest']['locust_host'] = arg
                print('set host to %s' % arg)
            elif opt in ('--users',):
                content['loadtest']['users'] = int(arg)
                print('set users to %s' % arg)
            elif opt in ('--spawnRate', ):
                content['loadtest']['spawn_rate'] = int(arg)
                print('set spawnRate to %s' % arg)
            elif opt in ('--runtime',):
                content['loadtest']['run_time'] = arg
                print('set runtime to %s' % arg)
            elif opt in ('--replicas',):
                content['worker']['replicas'] = int(arg)
                print('set replicas to %s' % arg)
            elif opt in ('--branch',):
                content['loadtest']['branch'] = arg
                print('set branch to %s' % arg)
            elif opt in ('--headless',):
                if arg == "false":
                    arg = ""
                content['loadtest']['headless'] = arg

        # update yaml file
        with open(values_file, 'w', encoding="utf-8") as nf:
            yaml.dump(content, nf, Dumper=yaml.RoundTripDumper)


    except Exception as ex:
        raise ex


if __name__ == "__main__":
    main(sys.argv[1:])