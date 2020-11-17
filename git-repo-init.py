import argparse
import os
import requests
import getpass
import json


def github_repo(arguments, password):
    url = 'https://api.github.com/user/repos'
    data = {"name": arguments.repo_name, "private": False}
    user = arguments.username
    ret = requests.post(url, data=json.dumps(data), auth=(user, password))

    if ret.status_code != 201:
        print(ret.text)
        exit(1)


def git_init(arguments, conn, password):
    with open('README.md', 'w') as f:
        f.write('# {}\n'.format(arguments.repo_name))
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "Initial commit"')
    os.system('git branch -M main')

    if conn == 'SSH':
        os.system('git remote add origin git@github.com:{}/{}.git'.format(arguments.username, arguments.repo_name))
        os.system('git push -u origin master')
    elif conn == 'HTTPS':
        os.system('git remote add origin https://github.com/{}/{}.git'.format(arguments.username, arguments.repo_name))
        os.system('git push https://{}:{}@github.com/{}/{}.git'.format(arguments.username, password, arguments.username,
                                                                       arguments.repo_name))
    else:
        raise ValueError("Unsupported GitHub connection type: {}".format(conn))


def run(arguments):
    password = getpass.getpass('GitHub Personal Access Token: ')
    github_repo(arguments, password)

    if args.ssh_mode:
        conn_mode = 'SSH'
    else:
        conn_mode = 'HTTPS'

    git_init(arguments, conn_mode, password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initialize a GitHub repository from the command line.")
    parser.add_argument('-r', '--repo-name', type=str, help='Name of the repository to be created.', required=True)
    parser.add_argument('-u', '--username', type=str, help='Name of the GitHub username.', required=True)
    parser.add_argument('--ssh', action='store_true', default=False, help='Use SSH connection to GitHub.',
                        dest='ssh_mode')
    parser.add_argument('--https', action='store_true', default=False, help='Use HTTPS connection to GitHub. (default)',
                        dest='https_mode')
    args = parser.parse_args()
    run(args)
