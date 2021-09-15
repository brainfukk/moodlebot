from src.core.config import TABLES_PREFIX


def create_table_name(table_name: str) -> str:
    return "{}_{}".format(TABLES_PREFIX, table_name)


def create_id_reference_string(table_name: str) -> str:
    return "{}_{}.id".format(TABLES_PREFIX, table_name)
