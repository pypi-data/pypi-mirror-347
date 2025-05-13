"""Constants for OARC Crawlers."""

# Default log levels
DEFAULT_LOG_LEVEL = "INFO"
VERBOSE_LOG_LEVEL = "DEBUG"

# Status constants
SUCCESS = 0
FAILURE = 1
ERROR = "error"
VERSION = "0.1.5"

# Default values for configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
DEFAULT_USER_AGENT = f"OARC-Crawlers/{VERSION}"

# Configuration key names
CONFIG_KEY_DATA_DIR = "data_dir"
CONFIG_KEY_LOG_LEVEL = "log_level"
CONFIG_KEY_MAX_RETRIES = "max_retries"
CONFIG_KEY_TIMEOUT = "timeout"
CONFIG_KEY_USER_AGENT = "user_agent"
CONFIG_KEY_GITHUB_TOKEN = "github_token"

# Environment variable names
ENV_DATA_DIR = "OARC_DATA_DIR"
ENV_LOG_LEVEL = "OARC_LOG_LEVEL"
ENV_MAX_RETRIES = "OARC_MAX_RETRIES"
ENV_TIMEOUT = "OARC_TIMEOUT"
ENV_USER_AGENT = "OARC_USER_AGENT"
ENV_HOME_DIR = "OARC_HOME_DIR"
ENV_GITHUB_TOKEN = "OARC_GITHUB_TOKEN"

# Configuration
DEFAULT_CONFIG_FILENAME = "crawlers.ini"
OARC_DIR = ".oarc"
CONFIG_DIR = "config"
CONFIG_SECTION = "oarc-crawlers"
CONFIG_ENV_PREFIX = "OARC_"

# Config keys that match both env vars and config file keys
CONFIG_KEYS = {
    CONFIG_KEY_DATA_DIR: ENV_DATA_DIR,
    CONFIG_KEY_LOG_LEVEL: ENV_LOG_LEVEL,
    CONFIG_KEY_MAX_RETRIES: ENV_MAX_RETRIES,
    CONFIG_KEY_TIMEOUT: ENV_TIMEOUT, 
    CONFIG_KEY_USER_AGENT: ENV_USER_AGENT,
    CONFIG_KEY_GITHUB_TOKEN: ENV_GITHUB_TOKEN,
}

# Path-related constants
DATA_SUBDIR = "data"
TEMP_DIR_PREFIX = "oarc-crawlers"
YOUTUBE_DATA_DIR = "youtube_data"
GITHUB_REPOS_DIR = "github_repos"
WEB_CRAWLS_DIR = "crawls"
ARXIV_PAPERS_DIR = "papers"
ARXIV_SOURCES_DIR = "sources"
ARXIV_COMBINED_DIR = "combined"
DDG_SEARCHES_DIR = "searches"

# Default headers for web requests
DEFAULT_HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT
}

# URLs
PYPI_PACKAGE_URL = "https://pypi.org/project/{package}/"
PYPI_JSON_URL = "https://pypi.org/pypi/{package}/json"

# YouTube URL formats
YOUTUBE_VIDEO_URL_FORMAT = "https://www.youtube.com/watch?v={video_id}"
YOUTUBE_CHANNEL_URL_FORMAT = "https://www.youtube.com/channel/{channel_id}"

# YouTube URL patterns for detection
YOUTUBE_WATCH_PATTERN = "youtube.com/watch"
YOUTUBE_SHORT_PATTERN = "youtu.be/"

# YouTube video format constants
YT_FORMAT_MP4 = "mp4"
YT_FORMAT_WEBM = "webm"
YT_FORMAT_MP3 = "mp3"

# YouTube resolution constants
YT_RESOLUTION_HIGHEST = "highest"
YT_RESOLUTION_LOWEST = "lowest"
YT_RESOLUTION_720P = "720p"
YT_RESOLUTION_1080P = "1080p"
YT_RESOLUTION_480P = "480p"
YT_RESOLUTION_360P = "360p"
YT_RESOLUTION_240P = "240p"
YT_RESOLUTION_144P = "144p"

# DuckDuckGo API constants
DDG_BASE_URL = "https://api.duckduckgo.com/"
DDG_API_PARAMS = "format=json&pretty=1"
DDG_IMAGES_PARAMS = "iax=images&ia=images"
DDG_NEWS_PARAMS = "ia=news"

# DuckDuckGo result headers
DDG_TEXT_SEARCH_HEADER = "# DuckDuckGo Search Results"
DDG_IMAGE_SEARCH_HEADER = "# DuckDuckGo Image Search Results"
DDG_NEWS_SEARCH_HEADER = "# DuckDuckGo News Search Results"

# ArXiv API constants
ARXIV_API_BASE_URL = "http://export.arxiv.org/api/query"
ARXIV_BASE_URL = "https://arxiv.org/"
ARXIV_SOURCE_URL_FORMAT = "https://arxiv.org/e-print/{arxiv_id}"
ARXIV_ABS_URL_FORMAT = "https://arxiv.org/abs/{arxiv_id}"
ARXIV_PDF_URL_FORMAT = "https://arxiv.org/pdf/{arxiv_id}.pdf"
ARXIV_URL_PATTERNS = ["/abs/", "/pdf/"]
ARXIV_NAMESPACES = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom'
}

# ArXiv processing limits
ARXIV_MAX_KEYWORDS = 10
ARXIV_MAX_EQUATIONS = 100
ARXIV_MAX_REFERENCES = 200
ARXIV_CATEGORY_MAX_RESULTS = 100
ARXIV_CITATION_MAX_DEPTH = 1
ARXIV_BATCH_CHUNK_SIZE = 10

# GitHub binary file extensions
GITHUB_BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.exe', '.dll', '.so', '.dylib',
    '.pyc', '.pyd', '.pyo',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf',
    '.mp3', '.mp4', '.wav', '.avi', '.mov', '.mkv',
    '.ttf', '.otf', '.woff', '.woff2'
}

# GitHub language mapping from extension
GITHUB_LANGUAGE_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React',
    '.tsx': 'React TypeScript',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.cs': 'C#',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.rs': 'Rust',
    '.sh': 'Shell',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.xml': 'XML',
    '.sql': 'SQL',
    '.r': 'R',
    '.m': 'Objective-C',
    '.dart': 'Dart',
    '.lua': 'Lua',
    '.pl': 'Perl',
    '.toml': 'TOML',
    '.ipynb': 'Jupyter Notebook'
}

# NLTK resources
NLTK_RESOURCES = ['tokenizers/punkt', 'corpora/stopwords']
