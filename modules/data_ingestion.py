import hashlib

class UserEntity:
    def __init__(self, name, birth_year, birth_month, birth_day, birth_hour, phone, lat=39.9, lon=116.4):
        self.name = name
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.birth_hour = birth_hour
        self.phone = phone
        self.lat = lat
        self.lon = lon
        self.entropy_seed = self._generate_entropy_seed()

    def _generate_entropy_seed(self):
        """
        Generates a privacy-preserving 'Entropy Seed' from sensitive data.
        Uses SHA-256 on Name + Phone.
        """
        raw_string = f"{self.name}:{self.phone}"
        return hashlib.sha256(raw_string.encode()).hexdigest()[:12]

    def get_birth_tuple(self):
        return (self.birth_year, self.birth_month, self.birth_day, self.birth_hour)
