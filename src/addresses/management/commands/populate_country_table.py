import csv
from django.core.management.base import BaseCommand
from addresses.models import Country

class Command(BaseCommand):
    help = 'Populate the Country table with data from a CSV file'

    def handle(self, *args, **kwargs):
        try:
            with open('addresses/management/commands/country_codes.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        Country.objects.create(
                            name=row['country_name'],
                            iso_alpha_2=row['alpha_2_code'],
                            iso_alpha_3=row['alpha_3_code'],
                        )
                    except KeyError as e:
                        self.stdout.write(self.style.ERROR(f"Missing expected column in CSV: {e}"))
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Error converting value: {e}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("The file was not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred while opening the file: {e}"))
