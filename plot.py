import git
import matplotlib.pyplot as plt
import os
import json
import subprocess
import sys

from tqdm import tqdm

def cloc(dir_path):
    try:
        cmd = ['cloc', '--json', '--quiet', dir_path]
        output = subprocess.check_output(cmd)
        return json.loads(output.decode())
    except:
        print("Please install cloc to use this software") 
        exit(-1)

def count_git_log(repo_path):
    dir_path = repo_path # FIXME
    repo = git.Repo(repo_path)
    code_counts = {}
    for commit in tqdm(list(repo.iter_commits())):
        repo.git.checkout(commit)
        code_counts[str(commit)] = cloc(dir_path)['SUM']['code']
    repo.git.checkout('main')
    return code_counts

def plot_code_counts(code_counts):
    plt.plot(list(code_counts.keys()), list(code_counts.values()))
    plt.xticks(list(code_counts.keys())[::len(code_counts)//10], rotation=45)
    plt.xlabel('Commit Hash')
    plt.ylabel('Lines of Code')
    plt.show()

def main():
    root_dir = sys.argv[1]
    counts = count_git_log(root_dir)
    plot_code_counts(counts)

if __name__ == '__main__':
    main()
