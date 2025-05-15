import os
import re
import urllib.parse
import requests

MAIN_SPEC_URL = "https://bird.ecb.europa.eu/documentation/api/v2/bird/bird-API-V2-documentation-Swagger-OpenAPI.yml"
LOCAL_BASE = "bird_openapi_download"
V2_PREFIX = "https://bird.ecb.europa.eu/documentation/api/v2/"

DOWNLOADED = set()

def download_yaml(url, local_path):
    print(f"Downloading: {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return resp.text

def find_refs(yaml_text):
    # Find all $ref: 'something.yml#/...' or "something.yml#/..."
    return set(re.findall(r"\$ref:\s*[\"']?([^\s\"']+\.ya?ml)[^\"']*[\"']?", yaml_text))

def resolve_url(base_url, ref_path):
    # Remove any #fragment
    ref_file = ref_path.split("#")[0]
    return urllib.parse.urljoin(base_url, ref_file)

def get_local_path(url):
    # Ensure the URL starts with the expected prefix
    if not url.startswith(V2_PREFIX):
        raise ValueError(f"Unexpected URL: {url}")
    rel_path = url[len(V2_PREFIX):]
    return os.path.join(LOCAL_BASE, rel_path)

def recursive_download(url, base_url):
    if url in DOWNLOADED:
        return
    DOWNLOADED.add(url)
    local_path = get_local_path(url)
    yaml_text = download_yaml(url, local_path)
    refs = find_refs(yaml_text)
    for ref in refs:
        ref_url = resolve_url(url, ref)
        recursive_download(ref_url, base_url)

if __name__ == "__main__":
    recursive_download(MAIN_SPEC_URL, V2_PREFIX)
    print("Done.")
