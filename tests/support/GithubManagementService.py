from github import Github
import json

def submit_battle_data(self):
    pass

def get_repo_string():
    return ':'.join(json.loads(open('boilerplate/group_info.json','r').read())['repo_url'].split(':')[1:]).replace('.git','')
    


def get_commit_id():
    # Replace 'your_access_token' with your GitHub access token
    g = Github("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")

    # Replace 'username/repo_name' with the specific repo
    repo = g.get_repo(get_repo_string())

    # Get the latest commit
    commits = repo.get_commits()
    latest_commit = commits[0]  # The first commit in the list is the latest
    latest_commit_id = latest_commit.sha
    print(latest_commit_id)
    return latest_commit_id
