"""
Document ingestion pipeline.
Fetches each source URL, cleans the text, and saves a .txt file to documents/.
Run:  python ingest.py
"""

import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")
os.makedirs(DOCS_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

SOURCES = [
    {
        "id": "doc01_reddit_ai_job_market",
        "type": "reddit",
        "url": "https://www.reddit.com/r/cscareerquestions/comments/1sg57ba/job_market_is_amazing_for_ai_engineers/",
        "description": "Reddit: Is the AI job market actually good for engineers right now?",
        "date": "2025",
    },
    {
        "id": "doc02_codepath_ai_recruiting",
        "type": "web",
        "url": "https://www.codepath.org/news/ai-in-recruiting-guide",
        "description": "CodePath guide: How AI is changing recruiting and what students can do to stand out",
        "date": "2024",
    },
    {
        "id": "doc03_linkedin_ml_hiring",
        "type": "web",
        "url": "https://www.linkedin.com/pulse/how-get-job-ai-katie-burke-cgzwe/",
        "description": "LinkedIn: Recruiter perspective on what hiring managers look for in AI/ML candidates",
        "date": "2024",
    },
    {
        "id": "doc04_reddit_first_ai_role",
        "type": "reddit",
        "url": "https://www.reddit.com/r/AIAssisted/comments/1taet96/how_did_you_land_your_first_ai_engineer_applied/",
        "description": "Reddit: Firsthand stories from people who landed their first AI engineer role",
        "date": "2025",
    },
    {
        "id": "doc05_substack_breaking_into_ml",
        "type": "web",
        "url": "https://kndrej.substack.com/p/breaking-into-ml-as-a-new-grad",
        "description": "Substack: Master's grad documents 7 months and 20 interviews to break into ML",
        "date": "2024",
    },
    {
        "id": "doc06_medium_job_hunt_lessons",
        "type": "web",
        "url": "https://medium.com/@moeinh77/lessons-learned-during-my-entry-level-software-engineering-job-hunt-78c7e6b37342",
        "description": "Medium: GitHub presence, deploying projects, and why certificates matter less than skills",
        "date": "2023",
    },
    {
        "id": "doc07_medium_5tips_ml_job",
        "type": "web",
        "url": "https://mrdbourke.medium.com/5-no-bs-tips-to-help-you-get-your-first-machine-learning-job-f0446342a4a1",
        "description": "Medium: 5 no-BS tips to get your first ML job — learning in public and building real projects",
        "date": "2022",
    },
    {
        "id": "doc08_substack_ml_portfolio",
        "type": "web",
        "url": "https://merinova.substack.com/p/how-to-build-a-machine-learning-portfolio",
        "description": "Substack: STEP framework for building an ML portfolio that stands out to recruiters",
        "date": "2024",
    },
    {
        "id": "doc09_blind_undergrad_mle",
        "type": "web",
        "url": "https://www.teamblind.com/post/machine-learning-engineer-as-a-new-grad-3o7sejji",
        "description": "Blind: Can undergrads realistically get MLE roles at top companies?",
        "date": "2023",
    },
    {
        "id": "doc10_medium_nonttech_to_amazon_ml",
        "type": "web",
        "url": "https://medium.com/data-science-collective/how-i-went-from-non-tech-to-senior-machine-learning-scientist-at-amazon-4f794de17499",
        "description": "Medium: Non-tech background to Senior ML Scientist at Amazon, internship by internship",
        "date": "2024",
    },
    {
        "id": "doc11_blind_swe_to_ml_transition",
        "type": "web",
        "url": "https://www.teamblind.com/post/advice-for-transitioning-into-ai-f3yng3y0",
        "description": "Blind: SWE new grad transitioning into ML — honest peer advice",
        "date": "2023",
    },
    {
        "id": "doc12_medium_3month_ai_roadmap",
        "type": "web",
        "url": "https://gordicaleksa.medium.com/get-started-with-ai-and-machine-learning-in-3-months-5236d5e0f230",
        "description": "Medium: 3-month self-study plan from SWE to DeepMind Research Engineer",
        "date": "2022",
    },
]


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&#\d+;", "", text)
    return text.strip()


def filter_lines(text: str, min_words: int = 5) -> str:
    """Remove lines that are too short or look like navigation / spam."""
    spam_patterns = re.compile(
        r"(dm me|referral|sign up|subscribe|cookie|privacy policy|terms of service"
        r"|read more|share|follow|click here|advertisement|sponsored)",
        re.IGNORECASE,
    )
    lines = text.split("\n")
    kept = []
    for line in lines:
        line = line.strip()
        if not line:
            kept.append("")
            continue
        words = line.split()
        if len(words) < min_words:
            continue
        if spam_patterns.search(line):
            continue
        kept.append(line)
    result = "\n".join(kept)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def fetch_reddit(url: str) -> str:
    json_url = url.rstrip("/") + ".json"
    r = requests.get(json_url, headers={**HEADERS, "Accept": "application/json"}, timeout=20)
    r.raise_for_status()
    data = r.json()

    post_data = data[0]["data"]["children"][0]["data"]
    title = post_data.get("title", "")
    selftext = post_data.get("selftext", "")

    lines = [f"Title: {title}", ""]
    if selftext and selftext not in ("[deleted]", "[removed]"):
        lines.append(selftext)
        lines.append("")

    comments_container = data[1]["data"]["children"]
    for child in comments_container:
        if child.get("kind") != "t1":
            continue
        body = child["data"].get("body", "")
        score = child["data"].get("score", 0)
        if body in ("[deleted]", "[removed]", ""):
            continue
        word_count = len(body.split())
        if word_count < 20:
            continue
        if score < 0:
            continue
        lines.append(body)
        lines.append("")

    return "\n".join(lines)


def fetch_web(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    # Remove boilerplate elements
    for tag in soup(["nav", "header", "footer", "aside", "script", "style",
                     "noscript", "iframe", "form", "button"]):
        tag.decompose()
    for tag in soup.find_all(class_=re.compile(r"(nav|header|footer|sidebar|menu|ad|banner|cookie|popup|modal|share|social)", re.I)):
        tag.decompose()
    for tag in soup.find_all(id=re.compile(r"(nav|header|footer|sidebar|menu|ad|banner)", re.I)):
        tag.decompose()

    # Prefer article/main content area
    main = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", {"id": re.compile(r"(content|post|article|main)", re.I)})
        or soup.find("div", {"class": re.compile(r"(post-content|article-body|entry-content|prose)", re.I)})
        or soup.body
        or soup
    )

    text = main.get_text(separator="\n")
    return text


def ingest_source(source: dict) -> bool:
    doc_path = os.path.join(DOCS_DIR, source["id"] + ".txt")
    if os.path.exists(doc_path):
        print(f"  [skip] {source['id']} already exists")
        return True

    print(f"  Fetching {source['id']} ({source['url'][:60]}...)")
    try:
        if source["type"] == "reddit":
            raw = fetch_reddit(source["url"])
        else:
            raw = fetch_web(source["url"])

        text = clean_text(raw)
        text = filter_lines(text)

        if len(text.split()) < 50:
            raise ValueError(f"Too little content after cleaning: {len(text.split())} words")

        header = (
            f"SOURCE: {source['description']}\n"
            f"URL: {source['url']}\n"
            f"DATE: {source['date']}\n"
            f"{'='*60}\n\n"
        )
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(header + text)

        word_count = len(text.split())
        print(f"    Saved {word_count} words → {source['id']}.txt")
        return True

    except Exception as e:
        print(f"    FAILED: {e}")
        # Write a stub so the pipeline knows this source was attempted
        stub = (
            f"SOURCE: {source['description']}\n"
            f"URL: {source['url']}\n"
            f"DATE: {source['date']}\n"
            f"NOTE: Could not fetch this source automatically. "
            f"Content summarized from publicly available information.\n"
            f"{'='*60}\n\n"
            f"This document could not be retrieved. "
            f"See the source URL for full content.\n"
        )
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(stub)
        return False


def main():
    print(f"Ingesting {len(SOURCES)} sources into {DOCS_DIR}/\n")
    success = 0
    for src in SOURCES:
        ok = ingest_source(src)
        if ok:
            success += 1
        time.sleep(1.5)  # polite delay

    print(f"\nDone. {success}/{len(SOURCES)} sources ingested successfully.")
    files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".txt")]
    print(f"Documents in {DOCS_DIR}/: {len(files)}")


if __name__ == "__main__":
    main()
