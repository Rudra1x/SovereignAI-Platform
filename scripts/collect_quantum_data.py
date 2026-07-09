from pathlib import Path

import requests
import trafilatura

RAW_DIR = Path("data/raw")


SOURCES = {

    "qiskit": [

        "https://qiskit.org/documentation/"

    ],

    "ibm": [

        "https://quantum.cloud.ibm.com/docs"

    ],

    "pennylane": [

        "https://docs.pennylane.ai/"

    ],
}


def download_page(url: str):

    downloaded = trafilatura.fetch_url(url)

    if downloaded is None:

        print(f"Failed : {url}")

        return None

    text = trafilatura.extract(downloaded)

    return text


def save(name, url, text):

    folder = RAW_DIR / name

    folder.mkdir(

        parents=True,

        exist_ok=True,

    )

    filename = (

        url.replace("https://", "")

        .replace("/", "_")

        + ".md"

    )

    with open(

        folder / filename,

        "w",

        encoding="utf-8",

    ) as fp:

        fp.write(text)


def main():

    for source, urls in SOURCES.items():

        print("=" * 60)

        print(source)

        print("=" * 60)

        for url in urls:

            print(url)

            text = download_page(url)

            if text:

                save(

                    source,

                    url,

                    text,

                )


if __name__ == "__main__":

    main()