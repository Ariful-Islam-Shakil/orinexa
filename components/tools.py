from typing import List, Union
import subprocess
import tempfile
from typing import Dict
import arxiv
from pydantic import BaseModel
#from google.colab import userdata
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import os
import requests
import urllib.parse
from typing import Optional 
from dotenv import load_dotenv
from components.schema import Paper
from components.vector_db import vector_memory

load_dotenv()

WEATHER_API = os.getenv('WEATHER_API')

def sum_of_nums(nums: List[float]) -> float:
    """
    Calculate the sum of a list of numbers.

    Args:
        nums (List[float]): A list of numeric values.

    Returns:
        float: The total sum of all numbers in the list.
    """
    print("\n",30*"#",f"\n\tCalling multiply tool with : {nums}\n", 30*"#","\n")
    return sum(nums)


def subtract(a: float, b: float) -> float:
    """
    Subtract one number from another.

    Args:
        a (float): The number from which to subtract.
        b (float): The number to subtract.

    Returns:
        float: The result of a - b.
    """
    print("\n",30*"#",f"\n\tCalling subtract tool with : {a, b}\n", 30*"#","\n")
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    print("\n",30*"#",f"\n\tCalling multiply tool with : {a, b}\n", 30*"#","\n")
    return a * b


def divide(a: float, b: float) -> Union[float, str]:
    """
    Divide one number by another.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The result of division if b is not zero.
        str: Error message if division by zero is attempted.
    """

    print("\n",30*"#",f"\n\tCalling divide tool with : {a, b}\n", 30*"#","\n")

    if b == 0:
        return "Cannot divide by zero"
    return a / b


def percentage(a: float, b: float) -> float:
    """
    Calculate the percentage value.

    Args:
        a (float): The base value.
        b (float): The percentage to apply.

    Returns:
        float: The result of (b% of a).
    """
    print("\n",30*"#",f"\n\tCalling perchangage tool with : {a, b}\n", 30*"#","\n")
    return a * (b / 100)



def run_python_script(code: str) -> Dict[str, str]:
    """
    Execute a Python script safely in a temporary file and return its output.

    Args:
        code (str): Python code as a string.

    Returns:
        dict: Contains stdout and stderr output.
    """

    print("\n",30*"#","\n\tCalling Run_python_script tool\n", 30*"#","\n")
    print(f"\tScript: \n\n {code}\n",30*"#","\n\n")
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            file_path = f.name

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e)
        }


def send_email(
    receiver_email: str,
    subject: str,
    body: str,
    cc_emails: Optional[List[str]] = None,
    attachments: Optional[List[str]] = None,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587
) -> str:
    """
    Send an email using SMTP with optional CC and file attachments.

    Args:
        receiver_email (str): Main receiver email
        subject (str): Email subject
        body (str): Email body
        cc_emails (List[str], optional): CC recipients
        attachments (List[str], optional): File paths to attach

    Returns:
        str: Status message
    """

    print("\n",30*"#","\n\tCalling send mail tool\n", 30*"#","\n")
    try:
        sender_email = userdata.get('EMAIL')
        sender_password = userdata.get('EMAIL_PASS')

        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Recipients list
        recipients = [receiver_email]

        if cc_emails:
            msg["Cc"] = ", ".join(cc_emails)
            recipients += cc_emails

        # Attach body
        msg.attach(MIMEText(body, "plain"))

        # -------------------------
        # Attach files (NEW PART)
        # -------------------------
        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    return f"❌ File not found: {file_path}"

                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)

                filename = os.path.basename(file_path)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )

                msg.attach(part)

        # Connect to SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email
        server.send_message(msg, from_addr=sender_email, to_addrs=recipients)
        server.quit()

        return "✅ Email sent successfully!"

    except Exception as e:
        return f"❌ Failed to send email: {e}"

def ask_user(question: str) -> str:
    """
    Ask the user a question and return their answer.

    Args:
        question (str): The question to ask the user.

    Returns:
        str: The user's answer.
    """
    print("\n",30*"#","\n\tCalling Ask User tool\n", 30*"#","\n")
    user_response = input(f"{question}\t")
    return user_response


def compile_latex_to_pdf(
    latex_code: str,
    output_file: str = "output.pdf",
    timeout: int = 30
) -> Optional[str]:
    """
    Compile LaTeX code into a PDF using LaTeX.Online free API.

    This function sends raw LaTeX code to latexonline.cc,
    compiles it on their server, and downloads the resulting PDF.

    Args:
        latex_code (str): Raw LaTeX source code as a string.
        output_file (str): Local filename to save the generated PDF.
        timeout (int): Request timeout in seconds.

    Returns:
        Optional[str]: Success message with file path if successful,
                       otherwise error message.

    """
    print("\n",30*"#","\n\tCalling latex tool\n", 30*"#","\n")


    try:
        base_url = "https://latexonline.cc/compile"

        # Encode LaTeX safely for URL transmission
        encoded_latex = urllib.parse.quote(latex_code)

        url = f"{base_url}?text={encoded_latex}"

        response = requests.get(url, timeout=timeout)

        # Check response
        if response.status_code != 200:
            return f"❌ Failed to compile LaTeX. Status code: {response.status_code}"

        # Save PDF
        with open(output_file, "wb") as f:
            f.write(response.content)

        return f"✅ PDF successfully generated: {output_file}"

    except requests.exceptions.Timeout:
        return "❌ Request timed out while compiling LaTeX."

    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

def search_papers(topic: str, max_results: int = 3) -> List[Paper]:
    """
    Search arXiv for papers using the updated Client API
    Returns list of Paper Pydantic models
    """
    print("\n",30*"#","\n\tCalling Search Paper tool\n", 30*"#","\n")
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
import requests

def get_weather(city: str) -> dict:
    """
    Get current weather for a city using WeatherAPI
    """
    print("\n",30*"#",f"\n\tCalling Get Weather tool for {city} city\n", 30*"#","\n")

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={city}"

    response = requests.get(url)
    data = response.json()
    print(f"Got weather for {city}\n#####\n")

    return {
        "city": data["location"]["name"],
        "temperature": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "description": data["current"]["condition"]["text"]
    }

import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a free web search using DuckDuckGo HTML results (no API key required).

    Args:
        query (str): Search query string.
        max_results (int): Maximum number of results to return.

    Returns:
        List[Dict[str, str]]: A list of search results where each item contains:
            - title (str): Title of the result
            - link (str): URL of the result
            - snippet (str): Short description (if available)

    Example:
        results = web_search("machine learning basics")
        for r in results:
            print(r["title"], r["link"])
    """

    print("\n",30*"#","\n\tCalling Web Search tool\n", 30*"#","\n")

    try:
        url = "https://duckduckgo.com/html/"
        params = {"q": query}

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, data=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return [{"error": f"Request failed with status {response.status_code}"}]

        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        items = soup.find_all("div", class_="result", limit=max_results)

        for item in items:
            title_tag = item.find("a", class_="result__a")
            snippet_tag = item.find("a", class_="result__snippet")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })

        return results

    except Exception as e:
        return [{"error": str(e)}]



from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional
import re



def get_youtube_transcript(
    video_url: str,
) -> Optional[str]:
    """
    Fetch transcript (script) from a YouTube video.

    Args:
        video_url (str): Full YouTube video URL

    Returns:
        Optional[str]: Transcript text or error message
    """

    print("\n",30*"#","\n\tCalling YouTube Search tool\n", 30*"#","\n")

    try:
        # Extract video ID
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
        if not match:
            return "❌ Invalid YouTube URL"

        video_id = match.group(1)

        # ✅ New API usage
        transcript = YouTubeTranscriptApi().fetch(video_id)

        # Extract text (no language filtering here)
        full_text = " ".join([snippet.text for snippet in transcript])

        return full_text

    except Exception as e:
        return f"❌ Failed to fetch transcript: {str(e)}"



from typing import List
import os
import cv2
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


def show_local_images(image_paths: List[str], cols: int = 2) -> str:
    """
    Display local images in a grid using matplotlib.

    Args:
        image_paths (List[str]): List of image file paths
        cols (int): Number of columns

    Returns:
        str: Status message
    """
    print("\n",30*"#","\n\tCalling Showing Images tool\n", 30*"#","\n")

    try:
        if not image_paths:
            return "❌ No images provided."

        valid_images = [p for p in image_paths if os.path.exists(p)]

        if not valid_images:
            return "❌ No valid image paths found."

        rows = (len(valid_images) + cols - 1) // cols

        plt.figure(figsize=(5 * cols, 4 * rows))

        for i, path in enumerate(valid_images):
            img = cv2.imread(path)

            if img is None:
                print(f"❌ Could not read: {path}")
                continue

            # Convert BGR → RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            plt.subplot(rows, cols, i + 1)
            plt.imshow(img)
            plt.title(os.path.basename(path))
            plt.axis("off")

        plt.tight_layout()
        plt.show()

        return f"✅ Successfully displayed {len(valid_images)} images."

    except Exception as e:
        return f"❌ Failed to display images: {e}"

def get_current_date_time(city: str = "Asia/Dhaka") -> dict:
    """
    Get current time for any timezone.

    Args:
        city (str): Timezone (e.g., 'Asia/Dhaka', 'Europe/London')

    Returns:
        dict: time info
    """
    print("\n",30*"#",f"\n\tCalling get_current_date_time tool for {city}\n", 30*"#","\n")

    try:
        tz = pytz.timezone(city)
        now = datetime.now(tz)

        return {
            "timezone": city,
            "date": now.strftime("%Y-%m-%d"),
            "day": now.strftime("%A"),
            "time": now.strftime("%H:%M:%S"),
        }

    except Exception as e:
        return {"error": str(e)}

# =====================================================
# 🔹 Get formatted context for LLM
# =====================================================
def get_long_term_context(query: str, k: int = 2) -> str:
    """
    Get long-term context for a given query.
    Args:
        query (str): well formed query for retrieving context
        k (int): Number of memories to retrieve

    Returns:
        str: Long-term context
    """

    print("\n",30*"#",f"\n\tCalling get_long_term_context tool for : {query} -> {k}\n", 30*"#","\n")

    memories = vector_memory.search(query, k)

    context = []

    for m in memories:
        context.append(
            f"""
              User: {m['query']}
              Answer: {m['final_answer']}
              Tools: {m['meta']['tools_used']}
            """
                          )

    return "\n---\n".join(context)
