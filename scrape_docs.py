from scrapling import Fetcher
import time

fetcher = Fetcher(engine='playwright')
# Scrapling's playwright engine should handle wait_until but let's be explicit if possible
# or just use a longer timeout or wait for selector
page = fetcher.get("https://apis.hyperbots.com/docs")

# If scrapling doesn't support manual waits easily, let's try to find a selector
# that indicates the docs are loaded.
print(f"Title: {page.css('title::text').get()}")
print(f"Body snippet: {page.text[:5000]}")

# Save the full HTML to a file for analysis
with open("docs.html", "w") as f:
    f.write(page.text)
