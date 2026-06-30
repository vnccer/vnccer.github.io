from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2]
FUNCTION_DIR = DATA_DIR / "function"
REPORTS_DIR = DATA_DIR / "reports"
DOWNLOADS_DIR = DATA_DIR / "downloads"

DEFAULT_SOURCE_DIR = str(DATA_DIR / "HaE")
DEFAULT_PRIORITY_FILE = str(REPORTS_DIR / "api_priority_report.txt")
DEFAULT_CONTEXT_OUTPUT_FILE = str(REPORTS_DIR / "api_context_report.md")
DEFAULT_RUNTIME_REPORT_FILE = str(REPORTS_DIR / "api_runtime_validation_report.md")
DEFAULT_CLASSIFY_OUTPUT_FILE = DEFAULT_PRIORITY_FILE
DEFAULT_JS_DIR = str(DOWNLOADS_DIR / "lenovo_js_download")
DEFAULT_BASE_URL = "https://baiying.com.cn"
DEFAULT_CONCURRENT = 10
DEFAULT_HOME_REQUEST_SAMPLE_FILE = str(DATA_DIR / "1.主页的一次请求.txt")
DEFAULT_HOME_RESPONSE_SAMPLE_FILE = str(DATA_DIR / "1.主页的一次原始响应.txt")
DEFAULT_FAKE200_REQUEST_SAMPLE_FILE = str(DATA_DIR / "2.伪200API的请求.txt")
DEFAULT_FAKE200_RESPONSE_SAMPLE_FILE = str(DATA_DIR / "2.伪200API的原始响应.txt")

SOURCE_HINT_FILES = {
    "Linkfinder.txt",
    "ALL URL.txt",
    "Sensitive Field.txt",
}
