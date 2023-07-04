# Deprecation warning
def deprecation_warning():
    message = """
    ================================================================================
    DEPRECATION WARNING - 'proxycrawl'
    ================================================================================

    'proxycrawl' is deprecated and will not be maintained. Please switch to 'crawlbase'.

    More details and migration guide: https://github.com/crawlbase-source/crawlbase-python
    ================================================================================
    """
    print(message)

deprecation_warning()

from proxycrawl.proxycrawl_api import ProxyCrawlAPI # For < 3.0 compatibility
from proxycrawl.crawling_api import CrawlingAPI
from proxycrawl.scraper_api import ScraperAPI
from proxycrawl.leads_api import LeadsAPI
from proxycrawl.screenshots_api import ScreenshotsAPI
from proxycrawl.storage_api import StorageAPI
