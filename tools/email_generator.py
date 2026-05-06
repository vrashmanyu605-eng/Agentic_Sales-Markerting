def generate_possible_emails(
    first_name,
    last_name,
    domain
):

    first = first_name.lower()
    last = last_name.lower()

    emails = [

        f"{first}@{domain}",

        f"{first}.{last}@{domain}",

        f"{first}{last}@{domain}",

        f"{first[0]}{last}@{domain}",

        f"{first}_{last}@{domain}"
    ]

    return emails