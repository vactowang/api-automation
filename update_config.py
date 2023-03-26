
import json
import getopt
import sys

from utils.behaviors import get_bflat_exp_list


def main(argvs):
    # Load config
    config = None
    json_config_file = 'config.json'
    
    try:
        opts, args = getopt.getopt(argvs, '', ['env=', 'skip_int=', 'ads_host=', 'config_host=', 'hbp_host=', 'scrat_all_host=', 'bflat_host='])
    except getopt.GetoptError as ex:
        print(ex)
        raise ex

    # Open config.json
    try:
        with open(json_config_file, 'r') as config_file:
            config = json.load(config_file)

        env = ''
        for opt, arg in opts:
            if opt in ('--env', ):
                env = arg.lower()
                config['env'] = env
                print('Set the env to %s' % env)

            if opt in ('--skip_int', ):
                skip_int = arg.lower()
                config['skip_int'] = skip_int
                print('Set the skip_int to %s' % arg.lower())

        for opt, arg in opts:
            if opt in ('--ads_host', ):
                config['endpoints']['ads'][env] = arg
                print('Set the ads %s host endpoint to %s' % (env, arg))
            elif opt in ('--config_host', ):
                config['endpoints']['config'][env] = arg
                print('Set the config %s host endpoint to %s' % (env, arg))
            elif opt in ('--hbp_host', ):
                config['endpoints']['hbp'][env] = arg
                print('Set the HBP %s host endpoint to %s' % (env, arg))
            elif opt in ('--scrat_all_host', ):
                config['endpoints']['scrat_all'][env] = arg
                print('Set the report ad %s host endpoint to %s' % (env, arg))
            elif opt in ('--bflat_host', ):
                config['endpoints']['bflat'][env] = arg
                print('Set the Bflat %s host endpoint to %s' % (env, arg))
                config['bflat']['random_exp_list'] = get_bflat_exp_list('random')

        # Write config.json
        with open(json_config_file, 'w') as outfile:  
            json.dump(config, outfile, indent=4)
        
        print('Done.')

    except Exception as ex:
        print(ex.msg)
        raise ex


if __name__=='__main__':
    main(sys.argv[1:])