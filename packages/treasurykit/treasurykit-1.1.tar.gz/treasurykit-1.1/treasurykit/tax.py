from zeep import Client

def check_vat_rate(country_code, vat_number):
    """
    Connects to the VIES VAT number validation service and checks a VAT number.

    Args:
        country_code (str): The two-letter country code (e.g., 'DE', 'FR').
        vat_number (str): The VAT number to check (without the country code).

    Returns:
        dict: A dictionary containing the validation result.
              Returns None if an error occurs during the connection.
    """
    wsdl_url = "https://ec.europa.eu/taxation_customs/vies/services/checkVatService.wsdl"
    try:
        client = Client(wsdl_url)
        response = client.service.checkVat(countryCode=country_code, vatNumber=vat_number)
        return {
            "countryCode": response.countryCode,
            "vatNumber": response.vatNumber,
            "valid": response.valid,
            "name": response.name,
            "address": response.address
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None