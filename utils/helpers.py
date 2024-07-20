from utils.constraints import LENGTH

def extract_country_code(phone_number) -> str:
    return phone_number[:len(phone_number) - LENGTH.PHONE_NUMBER]

def get_phone_without_country_code(phone_number) -> str:
    return phone_number[len(phone_number) - LENGTH.PHONE_NUMBER:]

# Get the country Code from the phone country code.
def get_country_code(country_code)->str:
    countries = {
            '91': 'IN',
            '1': 'US',
            '44': 'UK',
            '65': 'SG',
            '60': 'MY',
            '62': 'ID',
            '63': 'PH',
            '66': 'TH',
            '84': 'VN',
            '855': 'KH',
            '856': 'LA',
            '880': 'BD',
            '977': 'NP',
            '94': 'LK',
            '95': 'MM',
            '971': 'AE',
            '966': 'SA',
            '962': 'JO',
            '972': 'IL',
            '964': 'IQ',
            '965': 'KW',
            '968': 'OM',
            '974': 'QA',
            '973': 'BH',
        }
    return countries.get(country_code, 'Unknown Country')
        