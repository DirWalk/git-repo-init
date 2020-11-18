"""
git-repo-init is used to initialize a repository on GitHub and locally, then sync the two.
This will allow for a quick start to a project utilizing Git.
"""

__version__ = '1.1'


import argparse
import os
import requests
import getpass
import json


def github_repo(repo_name, username, password):
    """
    Authenticate to GitHub utilizing GitHub API and initialize a repository.
    :param repo_name: The name of the repository to initialize on GitHub.
    :param username: The username that will be used to authenticate with GitHub.
    :param password: The password or personal access token to authenticate with GitHub.
    """
    url = 'https://api.github.com/user/repos'
    data = {"name": repo_name, "private": False}
    user = username
    ret = requests.post(url, data=json.dumps(data), auth=(user, password))

    if ret.status_code != 201:
        print(ret.text)
        exit(1)


def github_webhook(repo_name, username, password, webhook):
    """
    Authenticate to GitHub utilizing GitHub API and create a webhook.
    :param repo_name: The name of the repository to initialize on GitHub.
    :param username: The username that will be used to authenticate with GitHub.
    :param password: The password or personal access token to authenticate with GitHub.
    :param webhook: The URL for GitHub to send post requests.
    """
    url = 'https://api.github.com/repos/{}/{}/hooks'.format(username, repo_name)
    data = {
        "name": "web",
        "active": True,
        "events": [
            "push",
        ],
        "config": {
            "url": webhook,
            "content_type": "json",
            "insecure_ssl": "0"
        }
    }
    user = username
    ret = requests.post(url, data=json.dumps(data), auth=(user, password))

    if ret.status_code != 201:
        print(ret.text)
        exit(1)


def git_init(repo_name, username, password, connection_type):
    """
    Create an Git repository in the current directory and push it to a repository on GitHub.
    :param repo_name: The name of the GitHub repository.
    :param username: The username that will be used to authenticate with GitHub.
    :param password: The password or personal access token to authenticate with GitHub.
    :param connection_type: The type of connection to use to authenticate with GitHub. (default: https)
    """
    with open('README.md', 'w') as f:
        f.write('# {}\n'.format(repo_name))
    os.system('git init')
    os.system('git add .')
    os.system('git -c user.name="{}" -c user.email="" commit -m "Initial commit"'.format(username))
    os.system('git branch -M main')
    os.system('git branch --set-upstream-to=origin/main main')

    if connection_type == 'SSH':
        os.system('git remote add origin git@github.com:{}/{}.git'.format(username, repo_name))
        os.system('git push -u origin main')
    elif connection_type == 'HTTPS':
        os.system('git remote add origin https://github.com/{}/{}.git'.format(username, repo_name))
        os.system('git push https://{}:{}@github.com/{}/{}'.format(username, password, username, repo_name))
    else:
        raise ValueError("Unsupported GitHub connection type: {}".format(connection_type))


def main(arguments):
    """
    Invokes Git initialization process.
    """
    repo_name = arguments.repo_name
    username = arguments.username
    password = getpass.getpass('GitHub Personal Access Token: ')

    github_repo(repo_name, username, password)

    if arguments.webhook_mode:
        github_webhook(repo_name, username, password, arguments.webhook_mode)

    if args.ssh_mode:
        connection_type = 'SSH'
    else:
        connection_type = 'HTTPS'

    git_init(repo_name, username, password, connection_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initialize a GitHub repository from the command line.",
                                     add_help=False)

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-r', '--repo-name', type=str, help='Name of the repository to be created',
                               required=True)
    required_args.add_argument('-u', '--username', type=str, help='Name of the GitHub username', required=True)

    optional_args = parser.add_argument_group('optional arguments')
    optional_args.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    optional_args.add_argument('-v', '--version', action='version', help='Show program\'s version number and exit',
                               version='%(prog)s ver. ' + __version__)
    optional_args.add_argument('--ssh', action='store_true', default=False, help='Use SSH connection to GitHub',
                               dest='ssh_mode')
    optional_args.add_argument('--https', action='store_true', default=False,
                               help='Use HTTPS connection to GitHub (default)', dest='https_mode')
    optional_args.add_argument('-w', '--webhook-url', type=str, help='URL of webhook to setup for the repository',
                               dest='webhook_mode', metavar='WEBHOOK_URL')

    args = parser.parse_args()
    main(args)
