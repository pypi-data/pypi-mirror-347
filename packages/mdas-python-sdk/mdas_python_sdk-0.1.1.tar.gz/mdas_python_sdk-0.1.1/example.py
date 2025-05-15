from mdas_python_sdk import MdasClient
from mdas_python_sdk.models.quote import Quote, QuoteResponse
from openai import OpenAI


def main():
    # Create a client instance
    client = MdasClient(
        base_url="https://mdas-api-dev.viewtrade.dev",
        username="Roxanne-admin2",  # Replace with your username
        password="NewPort@525"     # Replace with your password
    )

    # Get level 1 quote for Tesla
    tesla_quote = client.quote.get_historical_minute_chart("TSLA", "2025-05-12")
    print("\nTesla Quote Response:")
    tesla_quote_data = QuoteResponse.from_dict(tesla_quote[0])
    print(f"Message: {tesla_quote_data}")
    
    # Print the first quote data
    """ if tesla_quote.get('data') and len(tesla_quote.get('data')) > 0:
        quote_data = tesla_quote.get('data')[0]
        print(f"Symbol: {quote_data.get('symbol')}")
        print(f"Last Price: {quote_data.get('last_px')}")
        print(f"Change: {quote_data.get('change')} ({quote_data.get('change_percent')}%)")
        print(f"Volume: {quote_data.get('volume')}")
     """
    # Get level 1 quote for multiple symbols
    """ multi_quotes = client.quote.get_level1_quote(["AAPL", "MSFT"])
    print("\nMultiple Quotes Response:")
    print(f"Message: {multi_quotes.get('message')}")
    print(f"Number of quotes: {len(multi_quotes.get('data', []))}")
    
    # Convert to model objects
    quote_response = QuoteResponse.from_dict(multi_quotes)
    print("\nUsing model objects:")
    for quote in quote_response.data:
        print(f"{quote.symbol}: ${quote.last_px} ({quote.change_percent}%)")
 """
    """  client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "Talk like a pirate."},
            {
                "role": "user",
                "content": "How do I check if a Python object is an instance of a class?",
            },
        ],
    )

    print(completion.choices[0].message.content) """

if __name__ == "__main__":
    main() 