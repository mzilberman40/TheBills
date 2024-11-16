
class Country:
    def __init__(self, rus_name, rus_name_official, rus_name_short, name, official_name,
                 iso3166=None, numeric=None, alfa2=None, alfa3=None, status=None):
        self.rus_name = rus_name
        self.rus_name_official = rus_name_official
        self.rus_name_short = rus_name_short
        self.iso3166 = self.numeric = iso3166 or numeric
        self.alfa2 = alfa2
        self.alfa3 = alfa3
        self.name = name
        self.official_name = official_name
        self.status = status

    def to_dict(self):
        """Convert the Country object to a dictionary."""
        return {
            'rus_name': self.rus_name,
            'rus_name_official': self.rus_name_official,
            'rus_name_short': self.rus_name_short,
            'iso3166': self.iso3166,
            'alfa2': self.alfa2,
            'alfa3': self.alfa3,
            'name': self.name,
            'official_name': self.official_name,
            'numeric': self.numeric,
            'status': self.status,
        }


class CustomCountries:
    def __init__(self):
        self.countries = []

    def add_country(self, country_data):
        """Add a new Country object from a dictionary."""
        country = Country(
            rus_name=country_data['rus_name'],
            rus_name_official=country_data['rus_name_official'],
            rus_name_short=country_data['rus_name_short'],
            iso3166=country_data['iso3166'],
            alfa2=country_data['alfa2'],
            alfa3=country_data['alfa3'],
            name=country_data['name'],
            official_name=country_data['official_name'],
            numeric=country_data['numeric'],
            status=country_data['status'],
        )
        self.countries.append(country)

    def find(self, substring):
        """
        Find a country by checking if the given substring is present in any of the Country's attributes.
        Returns a list of matching Country objects.
        """
        results = []
        for country in self.countries:
            # Iterate through all the attributes of the country object
            for value in country.to_dict().values():
                if isinstance(value, str) and substring.lower() in value.lower():  # Check if substring is in the string attribute
                    results.append(country)
                    break  # No need to check other attributes once we have a match
        return results

    def to_dict(self):
        """Convert the list of Country objects to a list of dictionaries."""
        return [country.to_dict() for country in self.countries]
