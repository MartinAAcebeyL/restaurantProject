from . import *


def create_one_pension():
    pension = Pension.create(
        monto=faker.random_element(elements=(350, 300, 250)),
        universitario=faker.boolean(chance_of_getting_true=25),
        almuerzo_completo=faker.boolean(chance_of_getting_true=80),
        activo=faker.boolean(chance_of_getting_true=70),
    )

    return pension
