import sys
import re
import glob
import numpy as np
from os.path import basename

import environments
import experiments
from experiments.plotting import plot_policy_map, plot_policy_map1, \
    plot_policy_map_combined, plot_value_map, plot_value_map1, plot_value_map2

base_dir = 'output/Q'
#base_dir = 'test-heatmap'
output_dir = 'output/images/Q'
#output_dir = 'test-heatmap'

envs = {}
envs['4x4']   = environments.get_small_frozen_lake_environment()
envs['8x8']   = environments.get_medium_rewarding_frozen_lake_environment()
envs['15x15'] = environments.get_large_frozen_lake_environment()
envs['4x12']  = environments.get_windy_cliff_walking_environment()

title_regex = re.compile('v-(.*)\.txt')

env_strs = ['4x4', '8x8', '15x15', '4x12']
#env_strs = ['4x12']

for env_str in env_strs:
    grid_files = glob.glob('{}/v-*{}*.txt'.format(base_dir, env_str))
    print(grid_files)

    env = envs[env_str]

    for path in grid_files:
        file = basename(path)
        search_result = title_regex.search(basename(file))
        if search_result is None:
            print("Could not parse: {}".format(basename(file)))
            continue

        match = search_result.groups()[0]
        mdp_name = match

        policy = np.loadtxt(base_dir + '/policy-' + mdp_name + '.txt')
        v      = np.loadtxt(base_dir + '/v-' + mdp_name + '.txt')

        p = plot_policy_map(mdp_name, policy, env.desc, env.colors(), env.directions())
        p.savefig(output_dir + '/policy-' + mdp_name + '-0.png', format='png', dpi=150)
        p.close()

        p = plot_policy_map1(mdp_name, policy, env.desc, env.colors(), env.directions())
        p.savefig(output_dir + '/policy-' + mdp_name + '-1.png', format='png', dpi=150)
        p.close()

        p = plot_policy_map_combined(mdp_name, policy, v, env.desc, env.colors(), env.directions())
        p.savefig(output_dir + '/combined-' + mdp_name + '-0.png', format='png', dpi=150)
        p.close()

        p = plot_value_map(mdp_name, v, env.desc, env.colors())
        p.savefig(output_dir + '/v-' + mdp_name + '-0.png', format='png', dpi=150)
        p.close()

        p = plot_value_map1(mdp_name, v, env.desc, env.colors())
        p.savefig(output_dir + '/v-' + mdp_name + '-1.png', format='png', dpi=150)
        p.close()

        p = plot_value_map2(mdp_name, v, env.desc, env.colors())
        p.savefig(output_dir + '/v-' + mdp_name + '-2.png', format='png', dpi=150)
        p.close()
