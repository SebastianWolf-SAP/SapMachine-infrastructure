'''
Copyright (c) 2001-2019 by SAP SE, Walldorf, Germany.
All rights reserved. Confidential and proprietary.
'''

import os
import sys
import json
import re
import utils
import argparse

from utils import JDKTag
from os.path import join

branch_pattern = re.compile('sapmachine([\d]+)?$')
merge_commit_pattern = re.compile('Merge pull request #\d+ from SAP/pr-jdk-')

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--workdir', help='the temporary working directory', metavar='DIR', default="tags_work", required=False)
    args = parser.parse_args()

    workdir = os.path.realpath(args.workdir)
    utils.remove_if_exists(workdir)
    os.makedirs(workdir)

    # clone the SapMachine repository
    git_target_dir = join(workdir, 'sapmachine')
    utils.git_clone('github.com/SAP/SapMachine.git', 'sapmachine', git_target_dir)

    # fetch all branches
    branches = utils.github_api_request('branches', per_page=100)

    # iterate all branches of the SapMachine repository
    for branch in branches:
        # filter for sapmachine branches
        match = branch_pattern.match(branch['name'])

        if match is not None:
            if match.group(1) is not None:
                # found sapmachine branch
                major = int(match.group(1))
                utils.run_cmd(str.format('git checkout {0}', branch['name']).split(' '), cwd=git_target_dir)

                # find the last merge commit and check wether it is a merge from the jdk branch
                _, commit_message, _ = utils.run_cmd('git log --merges -n 1 --format=%s'.split(' '), cwd=git_target_dir, std=True, throw=False)
                match_merge_commit = re.search(merge_commit_pattern, commit_message)
                match_jdk_tag = re.search(JDKTag.jdk_tag_pattern, commit_message)

                if match_merge_commit is not None and match_jdk_tag is not None:
                    # get the commit id of the merge commit
                    _, commit_id, _ = utils.run_cmd('git log --merges -n 1 --format=%H'.split(' '), cwd=git_target_dir, std=True, throw=False)
                    commit_id = commit_id.rstrip()

                    if commit_id:
                        # get the tags pointing to the merge commit
                        _, tags, _ = utils.run_cmd(str.format('git tag --contains {0}', commit_id).split(' '), cwd=git_target_dir, std=True, throw=False)

                        if not tags:
                            # create sapmachine tag
                            jdk_tag = JDKTag(match_jdk_tag)
                            print(str.format('creating tag "{0}"', jdk_tag.as_sapmachine_tag()))
                            utils.run_cmd(str.format('git checkout {0}', commit_id).split(' '), cwd=git_target_dir)
                            utils.run_cmd(str.format('git tag {0}', jdk_tag.as_sapmachine_tag()).split(' '), cwd=git_target_dir)
                            utils.run_cmd(str.format('git push origin {0}', jdk_tag.as_sapmachine_tag()).split(' '), cwd=git_target_dir)

    utils.remove_if_exists(workdir)
    return 0

if __name__ == "__main__":
    sys.exit(main())