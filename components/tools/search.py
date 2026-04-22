import re
import arxiv
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from components.schema import Paper

def search_papers(topic: str, max_results: int = 3) -> List[Paper]:
    """Search arXiv for papers and return list of Paper models."""
    print(f"\n[Tool Call] search_papers: {topic}")
    client_arxiv = arxiv.Client(page_size=max_results)
    search = arxiv.Search(query=topic, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    results = []
    for paper in client_arxiv.results(search):
        results.append(Paper(
            title=paper.title,
            authors=[author.name for author in paper.authors],
            summary=paper.summary,
            link=paper.entry_id
        ))
    return results

def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Perform a free web search using DuckDuckGo HTML results."""
    print(f"\n[Tool Call] web_search: {query}")
    try:
        url = "https://duckduckgo.com/html/"
        params = {"q": query}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.post(url, data=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return [{"error": f"Request failed with status {response.status_code}"}]

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        items = soup.find_all("div", class_="result", limit=max_results)

        for item in items:
            title_tag = item.find("a", class_="result__a")
            snippet_tag = item.find("a", class_="result__snippet")
            if not title_tag: continue
            results.append({
                "title": title_tag.get_text(strip=True),
                "link": title_tag.get("href", ""),
                "snippet": snippet_tag.get_text(strip=True) if snippet_tag else ""
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def get_youtube_transcript(video_url: str) -> Optional[str]:
    """Fetch transcript (script) from a YouTube video."""
    print(f"\n[Tool Call] get_youtube_transcript: {video_url}")
    try:
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
        if not match:
            return "❌ Invalid YouTube URL"
        video_id = match.group(1)
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return " ".join([snippet.text for snippet in transcript])
    except Exception as e:
        return f"❌ Failed to fetch transcript: {str(e)}"
