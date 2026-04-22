import os
import requests
import cv2
import matplotlib.pyplot as plt
import pytz
from datetime import datetime
from typing import List, Dict
from components.config import Config

def get_weather(city: str) -> dict:
    """Get current weather for a city using WeatherAPI."""
    print(f"\n[Tool Call] get_weather for {city}")
    if not Config.WEATHER_API:
        return {"error": "Weather API key not configured."}
    
    url = f"http://api.weatherapi.com/v1/current.json?key={Config.WEATHER_API}&q={city}"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "description": data["current"]["condition"]["text"]
        }
    except Exception as e:
        return {"error": str(e)}

def get_current_date_time(timezone: str = Config.DEFAULT_TIMEZONE) -> dict:
    """Get current time for any timezone."""
    print(f"\n[Tool Call] get_current_date_time for {timezone}")
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return {
            "timezone": timezone,
            "date": now.strftime("%Y-%m-%d"),
            "day": now.strftime("%A"),
            "time": now.strftime("%H:%M:%S"),
        }
    except Exception as e:
        return {"error": str(e)}

def ask_user(question: str) -> str:
    """Ask the user a question and return their answer."""
    print(f"\n[Tool Call] ask_user: {question}")
    return input(f"{question}\t")

def show_local_images(image_paths: List[str], cols: int = 2) -> str:
    """Display local images in a grid using matplotlib."""
    print(f"\n[Tool Call] show_local_images: {image_paths}")
    try:
        valid_images = [p for p in image_paths if os.path.exists(p)]
        if not valid_images:
            return "❌ No valid image paths found."

        rows = (len(valid_images) + cols - 1) // cols
        plt.figure(figsize=(5 * cols, 4 * rows))

        for i, path in enumerate(valid_images):
            img = cv2.imread(path)
            if img is None: continue
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
