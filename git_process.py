import subprocess

def git_operations():
    # Git add
    subprocess.run(['git', 'add', '.'])

    # Git commit
    commit_message = input("Enter the commit message: ")
    subprocess.run(['git', 'commit', '-m', commit_message])

    # Git push
    subprocess.run(['git', 'push'])

if __name__ == "__main__":
    git_operations()
