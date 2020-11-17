import argparse
import os
import requests
import getpass
import json


def github_repo(repo_name, username, password):
    url = 'https://api.github.com/user/repos'
    data = {"name": repo_name, "private": False}
    user = username
    ret = requests.post(url, data=json.dumps(data), auth=(user, password))

    if ret.status_code != 201:
        print(ret.text)
        exit(1)


def git_init(repo_name, username, password, connection_type):
    with open('README.md', 'w') as f:
        f.write('# {}\n'.format(repo_name))
    os.system('git init')
    os.system('git add .')
    os.system('git -c user.name="{}" -c user.email="" commit -m "Initial commit"'.format(username))
    os.system('git branch -M main')

    if connection_type == 'SSH':
        os.system('git remote add origin git@github.com:{}/{}.git'.format(username, repo_name))
        os.system('git push -u origin main')
    elif connection_type == 'HTTPS':
        os.system('git remote add origin https://github.com/{}/{}.git'.format(username, repo_name))
        os.system('git push https://{}:{}@github.com/{}/{}'.format(username, password, username, repo_name))
    else:
        raise ValueError("Unsupported GitHub connection type: {}".format(connection_type))


def run(arguments):
    repo_name = arguments.repo_name
    username = arguments.username
    password = getpass.getpass('GitHub Personal Access Token: ')

    github_repo(repo_name, username, password)

    if args.ssh_mode:
        connection_type = 'SSH'
    else:
        connection_type = 'HTTPS'

    git_init(repo_name, username, password, connection_type)


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
