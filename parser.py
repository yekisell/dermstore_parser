import click
import requests
from bs4 import BeautifulSoup
import csv


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "accept": "*/*",
}


def get_html(url, params=None):
    r = requests.get(url, params, headers=HEADERS)
    return r


def save_item(item, path, appending=True):
    if appending:
        with open(path, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                [
                    item["product_name"],
                    item["brand_name"],
                    item["price"],
                    item["main_image_url"],
                    item["product_overview_block"],
                    item["how_to_use_block"],
                ]
            )
    else:
        with open(path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                [
                    "Product name",
                    "Brand name",
                    "Price",
                    "Main image url",
                    "Product overview block",
                    "How to use block",
                ]
            )
            writer.writerow(
                [
                    item["product_name"],
                    item["brand_name"],
                    item["price"],
                    item["main_image_url"],
                    item["product_overview_block"],
                    item["how_to_use_block"],
                ]
            )


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find("div", class_="athenaProductPage_topRow")

    item_attributes = {
        "product_name": item.find("h1", class_="productName_title").get_text(),
        "brand_name": item.find("img", class_="productBrandLogo_image").get("title"),
        "price": item.find("p", class_="productPrice_price").get_text(strip=True),
        "main_image_url": item.find(
            "img", class_="athenaProductImageCarousel_image"
        ).get("src"),
    }

    product_overview_block = item.find(
        "div", class_="productDescription_contentPropertyListItem_synopsis"
    )
    item_attributes["product_overview_block"] = (
        product_overview_block.find("div", class_="productDescription_synopsisContent")
        .get_text()
        .replace("\n", " ")
        .strip()
    )

    how_to_use_block = item.find(
        "div", class_="productDescription_contentPropertyListItem_directions"
    )
    item_attributes["how_to_use_block"] = (
        how_to_use_block.find("div", class_="productDescription_synopsisContent")
        .get_text()
        .replace("\n", " ")
        .strip()
    )

    return item_attributes


@click.command()
@click.option(
    "-u",
    "--url-of-item",
    default="https://www.dermstore.com/tripollar-desire-toning-device/13525895.html",
    type=str,
)
@click.option("-s", "--save-path", default="cosmetics.csv", type=str)
@click.option("-a", "--appending", default=True, type=bool)
def parse(url_of_item, save_path, appending):
    html = get_html(url_of_item)

    if html.status_code == 200:
        item = get_content(html.text)
        save_item(item, save_path, appending)
    else:
        print("Can't get access to this link!")


if __name__ == "__main__":
    parse()
