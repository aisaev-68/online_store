from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender

person = Person(locale=Locale.RU)

print(person.telephone('7##########'))
