from typing import Any, Dict
from log_to_db.duckdb_log import DuckDBLog
from log_to_db.postgres_log import PostgresLog
from log_to_db.sqlite_log import SQLiteLog
import platform
from typing import Dict, Any

ERROR_CODES = {
    0: "Success",
    1: "Program failure",
    2: "Logging error",
    3: "Email error.",
    4: "Report error.",
    5: "Database error.",
    6: "No data available",
    9: "Error code doesn't exist.",
}
MODULE_NAME = "firefly_reports"

def config_logger(config:Dict[str, Any]):
    """Will setup logger to either DuckDB, PostgreSQL or SQLite."""

    my_system = platform.uname()
    pc_name = my_system.node
    module_name = "firefly_reports"

    save_level = config.get("save_level","debug")
    enable_logging = config.get("enable_logging",False)
    logging_database = config.get("logging_database","duckdb")
    database_location = config.get("database_location","firefly.duckdb")
    user_name = config.get("username","NA")
    password = config.get("password","NA")
    address = config.get("address","NA")
    port = config.get("port",5432)
    database_name = config.get("database","public")
    schema = config.get("schema","programs")
    timezone = config.get("timezone","America/New_York")
    
    if enable_logging:
        #TODO: Then check for type
        pass
    else:
        #TODO: Will use DuckDB but "save" to memory and then print to screen at end
        pass

    #TODO: Setup logger by type
    if logging_database == "duckdb":
        pass
    elif logging_database == "postgresql":
        db_logger = PostgresLog(
                save_level=save_level,
                connection_info=f"postgres://{user_name}:{password}@{address}:{port}/{database_name}",
                schema=schema,
                pc_name=pc_name,
                program_name=MODULE_NAME,
                #program_timezone=timezone,
                )
    elif logging_database == "sqlite":
        pass
    else:
        #TODO: raise an error though it shouldn't get this far
        pass
                

    db_logger.load_log_levels()
    # TODO: Attempt to log to verify that it will log and save else raise error

    return db_logger
