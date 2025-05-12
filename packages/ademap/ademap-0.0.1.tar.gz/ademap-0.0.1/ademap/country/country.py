import requests

def country():
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()

        result = []
        for country in countries:
            name = country.get('name', {}).get('common', 'N/A')
            capital = ", ".join(country.get('capital', ['N/A']))

            # Get currency name(s)
            currencies = country.get('currencies', {})
            currency_list = []
            for code, currency_info in currencies.items():
                currency_name = currency_info.get('name', 'N/A')
                currency_list.append(f"{currency_name} ({code})")
            currency = ", ".join(currency_list) if currency_list else 'N/A'
            
            # Continent
            continents = country.get('continents', ['N/A'])
            continent = ", ".join(continents)


            each_result = {
                "Continent": continent,
                "Country": name,
                "Capital": capital,
                "Currency": currency
            }
            result.append(each_result)
        return(result)

    except requests.RequestException as e:
        return(f"Error fetching data: {e}")



