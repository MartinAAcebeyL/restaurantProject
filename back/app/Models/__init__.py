from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from faker.providers import phone_number

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy.event import listen
from sqlalchemy import asc, desc
from sqlalchemy import or_
import random


db = SQLAlchemy()
Faker.seed(40)
fake = Faker()