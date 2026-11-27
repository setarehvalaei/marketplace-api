from app.repositories.memory import vendors


def find_vendor(vendor_id):
    for vendor in vendors:
        if vendor["id"] == vendor_id:
            return vendor

    return None