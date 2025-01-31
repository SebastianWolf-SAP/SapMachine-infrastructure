'''
Copyright (c) 2001-2018 by SAP SE, Walldorf, Germany.
All rights reserved. Confidential and proprietary.
'''

import os
import re
import sys
import utils

from os.path import join
from versions import SapMachineTag

def write_index_yaml(assets, target):
    with open(join(target, 'index.yml'), 'w+') as index_yaml:
        index_yaml.write('---\n')
        for version in sorted(assets):
            index_yaml.write(str.format('{0}: {1}\n', version, assets[version]))

def main(argv=None):
    token = utils.get_github_api_accesstoken()
    asset_pattern = re.compile(utils.sapmachine_asset_pattern())
    asset_map_jre = {}
    asset_map_jdk = {}

    releases = utils.get_github_releases()

    for release in releases:
        if release['prerelease'] is True:
            continue

        t = SapMachineTag.from_string(release['name'])
        if t is None:
            continue

        assets = release['assets']
        for asset in assets:
            match = asset_pattern.match(asset['name'])
            if match is None:
                continue

            asset_image_type = match.group(1)
            asset_os = match.group(3)

            if asset_os == 'linux-x64':
                sapmachine_version = t.get_version()
                build_number = t.get_build_number()

                buildpack_version = str.format('{0}.{1}.{2}_{3}.{4}.b{5}',
                    sapmachine_version[0],
                    sapmachine_version[1],
                    sapmachine_version[2],
                    sapmachine_version[3],
                    sapmachine_version[4],
                    build_number if build_number else '0')

                if asset_image_type == 'jre':
                    asset_map_jre[buildpack_version] = asset['browser_download_url']
                else:
                    asset_map_jdk[buildpack_version] = asset['browser_download_url']

    local_repo = join(os.getcwd(), 'gh-pages')
    utils.git_clone('github.com/SAP/SapMachine.git', 'gh-pages', local_repo)
    write_index_yaml(asset_map_jre, join(local_repo, 'assets', 'cf', 'jre', 'linux', 'x86_64'))
    write_index_yaml(asset_map_jdk, join(local_repo, 'assets', 'cf', 'jdk', 'linux', 'x86_64'))
    utils.git_commit(local_repo, 'Updated index.yml', ['assets'])
    utils.git_push(local_repo)
    utils.remove_if_exists(local_repo)

    return 0

if __name__ == "__main__":
    sys.exit(main())
