from pyngrok import ngrok
import time, pathlib
url = ngrok.connect(8501, bind_tls=True).public_url
pathlib.Path('tunnel_url.txt').write_text(url)
print(url, flush=True)
# keep alive
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    ngrok.kill()
