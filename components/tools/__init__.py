from .calculator import (
    sum_of_nums,
    subtract,
    multiply,
    divide,
    percentage
)
from .automation import (
    run_python_script,
    send_email,
    compile_latex_to_pdf
)
from .search import (
    search_papers,
    web_search,
    get_youtube_transcript
)
from .utils import (
    get_weather,
    get_current_date_time,
    ask_user,
    show_local_images
)
from .memory import get_long_term_context

# List of all tools for easy import in main.py
ALL_TOOLS = [
    sum_of_nums,
    subtract,
    multiply,
    divide,
    percentage,
    run_python_script,
    send_email,
    compile_latex_to_pdf,
    search_papers,
    web_search,
    get_youtube_transcript,
    get_weather,
    get_current_date_time,
    ask_user,
    show_local_images,
    get_long_term_context
]
