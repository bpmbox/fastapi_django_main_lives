import os
import subprocess
import string
import random
import datetime
import requests

def github(token, folder):
    GITHUB_USERNAME = os.getenv("github_user")
    GITHUB_TOKEN = os.getenv("github_token")

    if not GITHUB_USERNAME or not GITHUB_TOKEN:
        print("❌ github_user または github_token が未設定です")
        #exit(1)

    REPO_NAME = "gpt-engeneer"
    # 相対パスを使用してHugging Faceでも動作するようにする
    controllers_dir = "app/Http/controller"  # app/Http/controllerディレクトリ
    target_dir = os.path.join(controllers_dir, folder)

    if not os.path.isdir(target_dir):
        print(f"❌ 指定フォルダが存在しません: {target_dir}")
        return None  # exit(1)の代わりにNoneを返す

    def generate_random_string(length=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    date_part = datetime.datetime.now().strftime("%Y%m%d")
    branch_name = f"{folder}-{date_part}-{generate_random_string()}"

    REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    WEB_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/tree/{branch_name}"
    print(f"🔗 ブランチURL: {WEB_URL}")

    # ✅ 1. リポジトリが存在しなければ作成
    check = requests.get(
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}",
        auth=(GITHUB_USERNAME, GITHUB_TOKEN)
    )
    if check.status_code == 404:
        print(f"ℹ️ リポジトリ {REPO_NAME} が存在しないため、作成します。")
        create = requests.post(
            "https://api.github.com/user/repos",
            auth=(GITHUB_USERNAME, GITHUB_TOKEN),
            json={"name": REPO_NAME, "public": True}
        )
        print(GITHUB_TOKEN)
        if create.status_code != 201:
            print(f"❌ リポジトリ作成失敗: {create.json()}")
            #exit(1)
        else:
            print(f"✅ リポジトリ作成成功: {REPO_NAME}")

    def run_command(command, cwd=None):
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd)
        if result.returncode != 0:
            print(f"❌ Command failed: {command}\n{result.stderr}")
            #exit(1)
        else:
            print(result.stdout)

    if not os.path.isdir(os.path.join(target_dir, ".git")):
        run_command("git init", cwd=target_dir)
        run_command(f"git remote add origin {REPO_URL}", cwd=target_dir)
        print("📁 git 初期化と origin 追加")

    run_command("git reset", cwd=target_dir)
    run_command(f"git checkout -b {branch_name}", cwd=target_dir)
    run_command("git add -f .", cwd=target_dir)
    run_command(f'git commit --allow-empty -m "Initial commit on branch {branch_name}"', cwd=target_dir)

    os.environ['FILTER_BRANCH_SQUELCH_WARNING'] = '1'
    run_command("git filter-branch --force --index-filter "
                '"git rm --cached --ignore-unmatch githubs.sh" '
                "--prune-empty --tag-name-filter cat -- --all", cwd=target_dir)

    remotes = subprocess.run("git remote", shell=True, text=True, capture_output=True, cwd=target_dir)
    if "origin" not in remotes.stdout:
        run_command(f"git remote add origin {REPO_URL}", cwd=target_dir)

    run_command(f"git push -u origin {branch_name}", cwd=target_dir)

    print(f"✅ Successfully pushed to GitHub branch: {branch_name}")
    return WEB_URL


# 使用例（実行時にtokenを渡す）
# github("your_actual_github_token", "test_folders")
