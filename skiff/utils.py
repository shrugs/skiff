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
