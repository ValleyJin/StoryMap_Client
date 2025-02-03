import os
import requests
from dotenv import load_dotenv
from scripts.process import process_md_files  # process.py에서 처리된 데이터 가져오기
from scripts.fetch_github import fetch_mystory_files, get_github_username  # GitHub에서 md 파일 목록 가져오기

# 환경 변수 로드
load_dotenv()

# StoryMap API 엔드포인트 (StoryMap 프로젝트 서버의 URL)
STORYMAP_API_URL = os.getenv("STORYMAP_API_URL")  # StoryMap 프로젝트의 API 엔드포인트

# StoryMap 서버로 데이터 전송 (Firestore에 직접 업로드하지 않음)
def send_to_storymap_api(story_title, md_files, provided_owner):
    """
    process.py에서 처리된 md 파일 데이터를 StoryMap 프로젝트(API)로 전송한다.
    """
    # 인증은 이미 fetch_mystory_files에서 수행되었으므로 제거

    # process.py에서 md 파일 처리
    processed_files = process_md_files(md_files)

    if not processed_files:
        print("🚫 StoryMap 서버로 전송할 데이터가 없습니다.")
        return

    # StoryMap API로 보낼 데이터 구성
    payload = {
        "title": story_title,
        "owner": provided_owner,  # 저장소 소유자 정보만 유지
        "chapters": processed_files  # 각 md 파일별 데이터 포함
    }

    # StoryMap API에 데이터 전송
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{STORYMAP_API_URL}/upload_story", json=payload, headers=headers)

    if response.status_code == 200:
        print(f"✅ StoryMap 서버에 '{story_title}' 스토리가 성공적으로 전송되었습니다!")
    else:
        print(f"❌ StoryMap 서버 전송 실패: {response.status_code} {response.text}")

# 실행 예제 (독립 실행 가능)
if __name__ == "__main__":
    repo_url = input("GitHub MyStory 저장소 URL을 입력하세요: ")
    provided_owner = input("GitHub 저장소의 소유자 ID를 입력하세요: ")  # 사용자가 자신의 GitHub ID를 입력
    story_title = input("스토리 제목을 입력하세요: ")

    md_files = fetch_mystory_files(repo_url, provided_owner)

    if md_files:
        send_to_storymap_api(story_title, md_files, provided_owner)
    else:
        print("❌ MyStory 폴더 내 md 파일을 찾을 수 없습니다.")
