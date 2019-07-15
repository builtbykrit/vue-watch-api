def parse_github_url(url):
    try:
        org_and_repo = url.split("github.com/", 1)[1]
        return org_and_repo
    except Exception:
        print('could not parse {}'.format(url))
        return None
