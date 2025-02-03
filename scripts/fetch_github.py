import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# GitHub API 인증 정보 (환경 변수에서 불러오기)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 사용자 인증을 위해 GitHub 사용자 이름 확인
def is_authorized_user(repo_url, provided_owner):
    """
    GitHub 저장소에서 owner 정보를 추출하고, 사용자가 입력한 소유자와 비교하여 인증을 수행한다.
    """
    actual_owner = get_github_username(repo_url)
    return actual_owner == provided_owner

# GitHub 저장소에서 사용자 ID 가져오기
def get_github_username(repo_url):
    """GitHub 저장소 URL에서 소유자(username) 추출"""
    parts = repo_url.split("/")
    if len(parts) >= 4:
        return parts[3]  # https://github.com/{USERNAME}/{REPO_NAME}.git → {USERNAME}
    return None

# GitHub API를 사용하여 MyStory 폴더 내 md 파일 목록 가져오기
def fetch_mystory_files(repo_url, provided_owner):
    """
    사용자의 GitHub 저장소에서 MyStory 폴더 내 md 파일 목록을 가져오고,
    각 md 파일의 URL과 소유자 정보를 포함한 리스트를 반환한다.
    """

    # 사용자 인증
    if not is_authorized_user(repo_url, provided_owner):
        print("🚫 인증 실패: 제공된 사용자 정보가 GitHub 저장소의 실제 소유자와 일치하지 않습니다.")
        return None

    repo_api_url = repo_url.replace("github.com", "api.github.com/repos").replace(".git", "") + "/contents/MyStory"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(repo_api_url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        md_files = []

        for file in files:
            if file['name'].endswith(".md"):
                file_data = {
                    "filename": file['name'],
                    "download_url": file['download_url'],
                    "owner": get_github_username(repo_url)  # 파일 소유자 정보 추가
                }
                md_files.append(file_data)

        return md_files  # md 파일 리스트 반환
    else:
        print(f"❌ GitHub API 요청 실패: {response.status_code} {response.text}")
        return []

# 테스트 실행 (독립 실행 가능)
if __name__ == "__main__":
    repo_url = input("GitHub MyStory 저장소 URL을 입력하세요: ")
    provided_owner = input("GitHub 저장소의 소유자 ID를 입력하세요: ")  # 사용자가 자신의 GitHub ID를 입력

    md_files = fetch_mystory_files(repo_url, provided_owner)

    if md_files:
        print("\n📜 MyStory 폴더 내 md 파일 목록:")
        for file in md_files:
            print(f"- {file['filename']} ({file['download_url']}) | Owner: {file['owner']}")
    else:
        print("❌ MyStory 폴더 내 md 파일을 찾을 수 없습니다.")