import os
from dotenv import load_dotenv
from scripts.fetch_github import fetch_mystory_files
from scripts.process import process_md_files
from scripts.upload_to_firestore import send_to_storymap_api

# 환경 변수 로드
load_dotenv()

# GitHub 토큰
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# StoryMap API URL
STORYMAP_API_URL = "https://storymap.tokamak.network/api"  # 실제 배포된 StoryMap 서버 URL

# 실행 예제
if __name__ == "__main__":
    print("\n🚀 StoryMap_Client 스토리 등록을 시작합니다...\n")

    story_title = input("📌 등록할 스토리 제목을 입력하세요: ").strip()
    repo_url = input("📌 GitHub MyStory 저장소 URL을 입력하세요: ").strip()
    provided_owner = input("📌 GitHub 저장소의 소유자 ID를 입력하세요: ").strip()

    print("\n🔍 GitHub 저장소에서 MyStory 폴더의 md 파일을 가져오는 중...")
    md_files = fetch_mystory_files(repo_url, provided_owner)

    if not md_files:
        print("❌ MyStory 폴더에서 md 파일을 찾을 수 없거나 인증에 실패했습니다. 프로그램을 종료합니다.")
        exit(1)

    print(f"✅ {len(md_files)}개의 md 파일을 가져왔습니다.")

    # StoryMap API로 데이터 전송
    print("\n📡 StoryMap 프로젝트로 데이터 전송 중...")
    send_to_storymap_api(story_title, md_files, provided_owner)

    print("\n🎉 스토리가 성공적으로 등록되었습니다!")
