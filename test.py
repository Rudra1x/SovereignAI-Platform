from sovereign.synthetic.ollama_client import OllamaClient


def main():

    client = OllamaClient()

    response = client.generate(
        "Explain what a Bell State is in two sentences."
    )

    print()
    print("=" * 70)
    print("MODEL OUTPUT")
    print("=" * 70)
    print(response)
    print("=" * 70)


if __name__ == "__main__":
    main()