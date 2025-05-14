from functools import lru_cache
from importlib.resources import files, as_file
from urllib.parse import quote
import llm_mimetypes.data as data

@lru_cache()
def get_db_uri():
    db_file = files(data).joinpath("models.db")
    with as_file(db_file) as path:
        # Make sure it's a proper URI (POSIX path + quoted)
        uri_path = quote(str(path.resolve().as_posix()))
        return f"file:///{uri_path}?mode=ro&immutable=1"

