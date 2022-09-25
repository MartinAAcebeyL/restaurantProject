from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from faker.providers import phone_number

db = SQLAlchemy()
Faker.seed(50)
fake = Faker()
