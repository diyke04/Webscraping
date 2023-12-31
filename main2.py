import pandas as pd
import httpx
import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup

all_data = []


def parse_html(html):
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.find("table", class_="table table-bordered table-striped")
    body = table.find("tbody")
    rows = body.find_all("tr")

    for i, row in enumerate(rows):
        tds = row.find_all("td", class_="")
        state = tds[0].text
        lga = tds[1].text
        ward = tds[2].text
        facility_uid = tds[3].text
        facility_code = tds[4].text
        facility_name = tds[5].text
        facility_level = tds[6].text
        ownership = tds[7].text

        views = soup.find_all("button", class_="btn btn-success btn-sm")[i].attrs

        lang = views["data-longitude"]
        lat = views["data-latitude"]
        status = views["data-operation_status"]
        beds_num = views["data-beds"]
        doctors = views["data-doctors"]
        nurse = views["data-nurses"]
        midwifes = views["data-midwifes"]
        nurse_midwifes = views["data-nurse_midwife"]
        community_health_officers = views["data-community_health_officer"]
        extension_workers = views["data-community_extension_workers"]
        envoronmental_health_officers = views["data-env_health_officers"]
        health_attendants = views["data-attendants"]

        all_data.append(
            [
                state,
                lga,
                ward,
                facility_uid,
                facility_code,
                facility_name,
                facility_level,
                ownership,
                lang,
                lat,
                status,
                beds_num,
                doctors,
                nurse,
                midwifes,
                nurse_midwifes,
                community_health_officers,
                extension_workers,
                envoronmental_health_officers,
                health_attendants,
            ]
        )


def get_links():
    links = []
    for i in range(1, 100):
        links.append(f"https://hfr.health.gov.ng/facilities/hospitals-list?page={i}#")
    # print(links)
    return links


async def get_data(client, url):
    response = await client.get(url)
    return response.text


async def get_all(client, urls):
    tasks = [asyncio.create_task(get_data(client=client, url=url)) for url in urls]
    results = await asyncio.gather(*tasks)
    print("gathered")
    return results


async def main(urls):
    async with httpx.AsyncClient(timeout=None) as client:
        data = await get_all(urls=urls, client=client)
        return data


if __name__ == "__main__":
    urls = get_links()
    datas = asyncio.run(main(urls=urls))

    print("dumping")

    with open("data.json", "w") as f:
        json.dump(datas, fp=f)

    # for data in datas:
    # parse_html(data)

# df = pd.DataFrame(all_data)
# df.to_csv("data.csv")
