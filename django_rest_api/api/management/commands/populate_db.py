import json
from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = "Utility to populate the database from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        file_path = options["file_path"]

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                users = json.load(file)
                """
                Creates new user instances in the database.

                - This script should ideally be run only once during the initial setup.
                - If re-run, it prevents duplicate users by enforcing the unique constraint.
                """
                for user_data in users:
                    User.objects.update_or_create(
                        email=user_data["email"],
                        defaults=user_data,
                    )

                self.stdout.write(f"Successfully imported users from {file_path}")
        except Exception as e:
            self.stderr.write(f"Error: {e}")
