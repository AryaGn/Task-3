import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import psycopg2
import time

# ---------------- CONFIG ----------------
BASE_URL = "http://books.toscrape.com/"
DB_CONFIG = {
    "host": "localhost",
    "database": "books_db",
    "user": "postgres",
    "password": "postgres123"   # change if your password is different
}

# ---------------- GLOBALS ----------------
session = requests.Session()
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

total_books = 0
timings = []

# ---------------- SCRAPE BOOK ----------------
def scrape_book(book_url, category):
    global total_books

    try:
        t0 = time.time()
        response = session.get(book_url, timeout=10)
        t1 = time.time()

        soup = BeautifulSoup(response.text, "html.parser")
        t2 = time.time()

        title_tag = soup.find("h1")
        price_tag = soup.find("p", class_="price_color")
        availability_tag = soup.find("p", class_="instock availability")
        rating_tag = soup.find("p", class_="star-rating")
        image_tag = soup.find("img")

        if not all([title_tag, price_tag, availability_tag, rating_tag, image_tag]):
            print(f"⚠️ Skipping broken page: {book_url}")
            return

        # Extract fields
        title = title_tag.text.strip()

        price_text = price_tag.text.encode("ascii", "ignore").decode()
        price = float(price_text.replace("£", "").strip())

        availability = availability_tag.text.strip()

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        rating = rating_map.get(rating_tag["class"][1], 0)

        image_url = urljoin(BASE_URL, image_tag["src"])

        # Insert into DB
        cur.execute("""
            INSERT INTO books (title, category, price, availability, rating, product_url, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_url) DO NOTHING
        """, (
            title,
            category,
            price,
            availability,
            rating,
            book_url,
            image_url
        ))

        conn.commit()
        total_books += 1

        timings.append((t1 - t0) + (t2 - t1))

    except Exception as e:
        conn.rollback()
        print(f"❌ Error scraping {book_url}: {e}")

# ---------------- SCRAPE CATEGORY ----------------
def scrape_category(category_url, category):
    print(f"Scraping category: {category}")
    next_page = category_url

    while next_page:
        response = session.get(next_page, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.select("article.product_pod h3 a")

        for book in books:
            book_url = urljoin(category_url, book["href"])
            scrape_book(book_url, category)

        next_btn = soup.select_one("li.next a")
        if next_btn:
            next_page = urljoin(next_page, next_btn["href"])
        else:
            next_page = None

# ---------------- MAIN ----------------
def main():
    start_time = time.time()

    home = session.get(BASE_URL, timeout=10)
    soup = BeautifulSoup(home.text, "html.parser")

    categories = soup.select("div.side_categories ul li ul li a")

    for cat in categories:
        name = cat.text.strip()
        link = urljoin(BASE_URL, cat["href"])
        scrape_category(link, name)

    total_time = time.time() - start_time

    print("\nSCRAPING REPORT")
    print("Total books scraped:", total_books)

    if timings:
        print("Average time per book:", round(sum(timings) / len(timings), 3), "seconds")
    else:
        print("Average time per book: N/A (no successful scrapes)")

    print("Total runtime:", round(total_time, 2), "seconds")

    cur.close()
    conn.close()

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()

