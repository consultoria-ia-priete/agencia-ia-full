"""
upload_media.py — Upload de arquivo local para CRM Funnels Media Library.

Retorna URL pública em assets.cdn.filesafe.space (Google Cloud Storage),
que Instagram aceita para publicação de carrosséis.

Uso:
    python upload_media.py /path/to/image.jpg
    python upload_media.py /path/to/dir/  # uploa todos os .jpg do diretório
"""
import os
import sys
import json
import time
import urllib.request
from _common import LOC, API_KEY, ctx


def upload_file(filepath: str) -> dict:
    """Upload um arquivo JPEG para CRM Funnels media library.

    Returns:
        dict com keys: fileId, url, traceId
    """
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    with open(filepath, "rb") as f:
        file_data = f.read()
    filename = os.path.basename(filepath)

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="altId"\r\n\r\n{LOC}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="altType"\r\n\r\nlocation\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"https://services.leadconnectorhq.com/medias/upload-file",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Version": "2021-07-28",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            # User-Agent é OBRIGATÓRIO — sem ele Cloudflare WAF retorna 403/1010
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Accept": "application/json",
        },
    )
    r = urllib.request.urlopen(req, context=ctx)
    return json.loads(r.read().decode())


def upload_directory(dir_path: str, pattern_suffix: str = ".jpg") -> dict[str, str]:
    """Faz upload de todos os arquivos com o sufixo dado, em ordem alfabética.

    Returns:
        dict mapeando filename -> URL pública
    """
    files = sorted([f for f in os.listdir(dir_path) if f.endswith(pattern_suffix)])
    urls = {}
    for f in files:
        full_path = os.path.join(dir_path, f)
        try:
            res = upload_file(full_path)
            urls[f] = res["url"]
            print(f"  ✅ {f}: {res['url']}")
            time.sleep(1)  # rate limiting safety
        except Exception as e:
            print(f"  ❌ {f}: {e}")
            urls[f] = None
    return urls


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python upload_media.py <file.jpg | directory/>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isdir(target):
        urls = upload_directory(target)
        out_path = os.path.join(target, "_ghl_urls.json")
        with open(out_path, "w") as f:
            json.dump(urls, f, indent=2)
        print(f"\nSaved to {out_path}")
    elif os.path.isfile(target):
        res = upload_file(target)
        print(json.dumps(res, indent=2))
    else:
        print(f"Path not found: {target}")
        sys.exit(1)
