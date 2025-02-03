import os
import requests
import re
from openai import OpenAI
from dotenv import load_dotenv
from scripts.fetch_github import fetch_mystory_files  # fetch_github.py에서 데이터 가져오기

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# 정규식을 사용하여 첫 번째 이미지 찾기
IMAGE_PATTERN = re.compile(r"!\[.*?\]\((.*?)\)")

# OpenAI API를 이용한 300자 요약 생성
def generate_summary(file_url):
    """
    md 파일의 내용을 가져와 OpenAI API를 사용하여 300자 이내 요약을 생성한다.
    """
    response = requests.get(file_url)
    if response.status_code == 200:
        content = response.text[:1000]  # 첫 1000자만 사용하여 요약 생성
        api_response = client.completions.create(
            model="gpt-4-turbo",
            prompt=f"Summarize this text in under 300 characters: {content}",
            max_tokens=100
        )
        return api_response.choices[0].text.strip()
    return "요약을 생성할 수 없습니다."

# md 파일에서 첫 번째 이미지 URL 추출
def extract_first_image(file_url):
    """
    md 파일의 내용을 가져와 첫 번째 이미지 URL을 추출한다.
    """
    response = requests.get(file_url)
    if response.status_code == 200:
        content = response.text
        match = IMAGE_PATTERN.search(content)
        return match.group(1) if match else None
    return None

# fetch_github.py에서 가져온 md 파일 목록을 처리
def process_md_files(md_files):
    """
    fetch_github.py에서 가져온 md 파일 목록을 받아 요약 및 이미지 URL을 처리한다.
    """
    processed_files = []

    for file in md_files:
        file_url = file["download_url"]
        summary = generate_summary(file_url)
        image_url = extract_first_image(file_url)

        processed_files.append({
            "filename": file["filename"],
            "url": file_url,
            "owner": file["owner"],
            "summary": summary,
            "image": image_url
        })

    return processed_files

# 테스트 실행 수정
if __name__ == "__main__":
    repo_url = input("GitHub MyStory 저장소 URL을 입력하세요: ")
    provided_owner = input("GitHub 저장소의 소유자 ID를 입력하세요: ")
    
    md_files = fetch_mystory_files(repo_url, provided_owner)

    if md_files:
        processed_data = process_md_files(md_files)

        if processed_data:
            print("\n📄 md 파일 요약 및 이미지 URL:")
            for data in processed_data:
                print(f"\n📜 파일: {data['filename']}")
                print(f"🔗 URL: {data['url']}")
                print(f"👤 Owner: {data['owner']}")
                print(f"📄 요약: {data['summary']}")
                if data["image"]:
                    print(f"🖼 이미지: {data['image']}")
                else:
                    print("🚫 이미지 없음")
        else:
            print("🚫 스토리 처리 중 인증 오류 발생")

    else:
        print("❌ MyStory 폴더 내 md 파일을 찾을 수 없습니다.")
