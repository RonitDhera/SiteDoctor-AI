import requests
from bs4 import BeautifulSoup
import time

def check_broken_links(soup, base_url):
    links = soup.find_all('a', href=True)
    broken_links = []
    for link in links:
        href = link['href']
        if href.startswith('http'):
            test_url = href
        else:
            test_url = base_url.rstrip('/') + '/' + href.lstrip('/')
        try:
            res = requests.head(test_url, timeout=5)
            if res.status_code >= 400:
                broken_links.append((test_url, res.status_code))
        except:
            broken_links.append((test_url, 'Connection Error'))
    return broken_links

def check_missing_alt_tags(soup):
    images = soup.find_all('img')
    missing = [img['src'] for img in images if not img.get('alt')]
    return missing

def ai_suggestions(report):
    suggestions = []
    if report['title'] == "Missing":
        suggestions.append("Add a <title> tag to improve SEO.")
    if report['meta_description'] == "Missing":
        suggestions.append("Add a meta description for better search visibility.")
    if report['load_time'] > 3:
        suggestions.append("Reduce load time by compressing images or using CDN.")
    if report['broken_links']:
        suggestions.append(f"Fix {len(report['broken_links'])} broken link(s).")
    if report['missing_alt_tags']:
        suggestions.append(f"Add alt text to {len(report['missing_alt_tags'])} images.")
    return suggestions

def analyze_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "Missing"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc['content'] if meta_desc else "Missing"

        broken_links = check_broken_links(soup, url)
        missing_alts = check_missing_alt_tags(soup)

        return {
            "status_code": response.status_code,
            "load_time": round(load_time, 2),
            "content_size": len(response.content),
            "title": title,
            "meta_description": meta_desc,
            "broken_links": broken_links,
            "missing_alt_tags": missing_alts,
            "ai_suggestions": ai_suggestions({
                "title": title,
                "meta_description": meta_desc,
                "load_time": load_time,
                "broken_links": broken_links,
                "missing_alt_tags": missing_alts
            })
        }

    except Exception as e:
        return {"error": str(e)}
