from write_schema import initialize_database
from write_mimetypes import insert_mime_types
from write_providers import insert_providers
from write_api_types import insert_api_types
from write_models import insert_models_with_provider_and_api
from write_model_mime_types import associate_model_mime_types_patterned

def print_sqlite_version():
    import sqlite3
    print(sqlite3.sqlite_version)

def build_database():
    print_sqlite_version()
    initialize_database()
    insert_mime_types()
    insert_providers()
    insert_api_types()
    insert_models_with_provider_and_api()
    associate_model_mime_types_patterned()


if __name__ == "__main__":
    build_database()