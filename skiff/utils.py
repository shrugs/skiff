import requests

DO_TOKEN = None

DO_BASE_URL = "https://api.digitalocean.com/v2"
DO_HEADERS = {
    "Content-Type": "application/json"
}
DO_DELETE_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# @TODO: write decorator that makes sure that token is set


def token(token):
    DO_TOKEN = token
    DO_HEADERS['Authorization'] = "Bearer " + DO_TOKEN
    DO_DELETE_HEADERS['Authorization'] = "Bearer " + DO_TOKEN
    return True


def page_collection(link, action):
    """Given a link to a collection of something (Images, Droplets, etc),
    collect all the items available via the API by paging through it if needed.

    The `action` parameter should be a callable that creates a list from the
    results of each intermediate API call every item found.
    """
    collection = []

    r = requests.get(link, headers=DO_HEADERS)
    r = r.json()

    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        collection.extend(action(r))
        if 'links' in r and 'pages' in r['links'] and 'next' in r['links']['pages']:
            collection.extend(page_collection(r['links']['pages']['next'], action))

    return collection

