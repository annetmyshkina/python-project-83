from bs4 import BeautifulSoup
from requests import RequestException, get


def get_data(url):
    data = {}
    try:
        response = get(url, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        data["status_code"] = response.status_code

        title_tag = soup.find("title")
        data["title"] = title_tag.get_text(strip=True) if title_tag else None

        h1_tag = soup.find("h1")
        data["h1"] = h1_tag.get_text(strip=True) if h1_tag else None

        desc_tag = soup.find("meta", attrs={"name": "description"})
        data["description"] = desc_tag.get(
            "content",
            "").strip() if desc_tag else None
        return data

    except RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None