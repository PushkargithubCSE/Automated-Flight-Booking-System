from faker import Faker

fake = Faker('en_IN')  # Indian-style names

def generate_passenger():
    passenger = {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.msisdn()[:10],  # 10-digit phone
    }
    return passenger
