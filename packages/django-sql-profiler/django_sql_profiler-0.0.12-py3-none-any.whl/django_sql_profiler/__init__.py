import contextlib
import hashlib
import os
import re
import socket
import sys
import time

from pymongo import MongoClient


def merge_two_dicts(x, y):
    """
    Merge two dictionaries.

    Args:
        x (dict): The first dictionary.
        y (dict): The second dictionary.

    Returns:
        dict: A new dictionary that contains the keys and values from both x and y.

    """
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


def _is_external_source(abs_path):
    # type: (str) -> bool
    """
    Check if the given absolute path belongs to an external source.

    Args:
        abs_path (str): The absolute path to check.

    Returns:
        bool: True if the path belongs to an external source (e.g., 'site-packages' or 'dist-packages'),
              False otherwise.
    """
    external_source = (
        re.search(r"[\\/](?:dist|site)-packages[\\/]", abs_path) is not None
    )
    return external_source


def hash_query_id(source, sql):
    """
    Generate a unique hash for a SQL query.

    Args:
        source (dict): A dictionary containing information about the source of the query.
            It should have the following keys: 'filepath', 'code_function', and 'lineno'.
        sql (str): The SQL query to hash.

    Returns:
        str: The MD5 hash of the query.

    """
    before_hash = sql
    if source:
        before_hash = f"{source.get('filepath')}:{source.get('code_function')}:{source.get('lineno')}:{sql}"
    return hashlib.md5(before_hash.encode()).hexdigest()

def _valid_app_namespace(namespace, options):
    """
    Check if the given namespace is valid for the current application.

    Args:
        namespace (str): The namespace to check.
        options (dict): Additional options for validation.
            {
                'app_namespace': ['apps.'],
            }

    Returns:
        bool: True if the namespace is valid, False otherwise.
    """
    app_namespaces = options.get("app_namespace", ["apps."])
    return any(namespace.startswith(app_ns) for app_ns in app_namespaces)
    
def find_source(options={}):
    """
    Finds the source of the current execution frame.

    Returns a dictionary containing information about the source, including the filepath,
    namespace, code function, and line number.
    """
    frame = sys._getframe()
    while frame is not None:
        try:
            abs_path = frame.f_code.co_filename
            if abs_path:
                abs_path = os.path.abspath(abs_path)
        except Exception:
            abs_path = ""

        try:
            namespace = frame.f_globals.get("__name__")
        except Exception:
            namespace = None
        should_be_included = not _is_external_source(abs_path)
        is_app_module = namespace is not None and _valid_app_namespace(namespace, options)

        if should_be_included and is_app_module and "wsgi" not in abs_path:
            break
        frame = frame.f_back

    if frame is None:
        return {}
    if frame is not None:
        try:
            lineno = frame.f_lineno
        except Exception:
            lineno = None
        try:
            namespace = frame.f_globals.get("__name__")
        except Exception:
            namespace = None
        try:
            filepath = frame.f_code.co_filename
        except Exception:
            filepath = None
        try:
            code_function = frame.f_code.co_name
        except Exception:
            code_function = None

        return {
            "filepath": filepath,
            "namespace": namespace,
            "code_function": code_function,
            "lineno": lineno,
        }


@contextlib.contextmanager
def capture_sql_query(sql, params=None, executemany=False, options={}):
    """
    Context manager for capturing and profiling SQL queries.

    Args:
        sql (str): The SQL query to be executed.
        params (tuple, optional): The parameters to be passed to the SQL query. Defaults to None.
        executemany (bool, optional): Indicates whether the query is executed multiple times. Defaults to False.
        options (dict, optional): Additional options for profiling. Defaults to {}.

    Yields:
        None

    Raises:
        None

    Returns:
        None
    """
    source = find_source(options=options)
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        is_slow_query = duration > options.get("slow_queries_threshold", 0)
        query_id = hash_query_id(source, sql)
        mongo_opts = options.get("mongodb", None)
        if is_slow_query:
            if mongo_opts:
                mongo_instance = get_mongodb_instance(
                    mongo_opts.get("uri", ""),
                    mongo_opts.get("db", ""),
                    mongo_opts.get("collection", ""),
                )
                mongo_instance.insert_one(
                    {
                        "host_name": socket.gethostname(),
                        "host_ip": socket.gethostbyname(socket.gethostname()),
                        "source": source,
                        "query_id": query_id,
                        "sql": sql,
                        "params": params,
                        "is_slow_query": is_slow_query,
                        "duration": duration,
                        "timestamp": start_time,
                    }
                )

        # print(f"Source: {source}")
        # print(f"Hash: {hash_query_id(source, sql)}")
        # print(f"SQL: {sql}")
        # print(f"Duration: {time.time() - start_time}")


def get_mongodb_instance(uri, db_name, collection):
    """
    Connects to a MongoDB instance and returns a specific collection.

    Args:
        uri (str): The URI of the MongoDB instance.
        db_name (str): The name of the database.
        collection (str): The name of the collection.

    Returns:
        pymongo.collection.Collection: The specified collection.

    """
    conn = MongoClient(host=uri, maxPoolSize=30)
    return conn[db_name][collection]

_sql_hook_installed = False

def install_sql_hook(options={}):
    global _sql_hook_installed
    if _sql_hook_installed:
        return # Or log a warning

    """
    Installs a hook to capture Django's queries.

    Args:
        options (dict): Optional dictionary of options.

    Returns:
        None
    """
    _options = merge_two_dicts({"slow_queries_threshold": 0.2}, options)

    try:
        from django.db.backends.utils import CursorWrapper
    except ImportError:
        from django.db.backends.util import CursorWrapper

    try:
        real_execute = CursorWrapper.execute
        real_executemany = CursorWrapper.executemany
    except AttributeError:
        return

    def execute(self, sql, params=None):
        with capture_sql_query(sql, params, executemany=False, options=_options):
            return real_execute(self, sql, params)

    def executemany(self, sql, param_list):
        with capture_sql_query(sql, param_list, executemany=True, options=_options):
            return real_executemany(self, sql, param_list)


    CursorWrapper.execute = execute
    CursorWrapper.executemany = executemany
    _sql_hook_installed = True
