def parse_address(data):
    return {
        "country": data["address_country"],
        "town": data["address_locality"],
        "street": data["address_route"],
    }