try:
    # Python 2
    from proxycrawl_api import ProxyCrawlAPI
except ModuleNotFoundError:
    # Python 3
    import proxycrawl.proxycrawl_api
