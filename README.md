# git-repo-init
`git-repo-init.py` is a script to automate creation of a GitHub repository, a local repository, and make an initial
commit from the command line.

## Installation:
`pip install -r requirements`

## Usage:
`git-repo-init.py` will attempt to send a POST request to GitHub's API in order to authenticate and create the 
repository.  This requires a GitHub `Personal Access Token`, which can be made in your GitHub accounts Developer 
settings.

`git-repo-init.py` will prompt for your `Personal Access Token` and use it for the POST
authentication, as well as the HTTPS connection method for your repository if you didn't choose to use SSH. If SSH 
connection is requested, the standard SSH key procedures apply. 


Required arguments are:
  
```
  -r REPO_NAME, --repo-name REPO_NAME
                        Name of the repository to be created
  -u USERNAME, --username USERNAME
                        Name of the GitHub username
```

Optional arguments are:

```
  -h, --help            Show this help message and exit
  -v, --version         Show program's version number and exit
  --ssh                 Use SSH connection to GitHub
  --https               Use HTTPS connection to GitHub (default)
  -w WEBHOOK_URL, --webhook-url WEBHOOK_URL
                        URL of webhook to setup for the repository
```

Examples:

```
# SSH GitHub initialization
python git-repo-init.py -r TEST_REPO -u USER --ssh

# HTTPS GitHub initialization
python git-repo-init.py -r TEST_REPO -u USER --https

# Also HTTPS GitHub initialization with Webhook setup
python git-repo-init.py -r TEST_REPO -u USER -w https://example.com
```

Webhook:

Currently webhooks are limited to a basic webhook with the following parameters:

* On Push requests
* Insecure SSL
* Content type: JSON