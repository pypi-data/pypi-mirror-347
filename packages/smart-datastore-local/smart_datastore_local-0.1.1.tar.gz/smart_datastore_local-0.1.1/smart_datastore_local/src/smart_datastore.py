from database_infrastructure_local.constants import LoggerComponentEnum
from database_infrastructure_local.generic_crud_abstract \
    import GenericCrudAbstract
from database_infrastructure_local.constants import DEFAULT_SQL_SELECT_LIMIT
from database_mysql_local.generic_crud_mysql import GenericCrudMysql

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', 'src')))

# from logger_local import LoggerLocal  # TODO
from logger_local.LoggerLocal import Logger

# TODO Update the python-package-template
DEVELOPER_EMAIL_ADDRESS = 'tal@circlez.ai'
SMART_DATASTORE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = -1  # TODO
SMART_DATASTORE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'database_mysql_local\\smart_datastore'  # TODO
SMART_DATASTORE_LOCAL_CODE_LOGGER_OBJECT = {
    'component_id': SMART_DATASTORE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': SMART_DATASTORE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL_ADDRESS,  # TODO Remove
    'developer_email_address': DEVELOPER_EMAIL_ADDRESS
}

# logger = LoggerLocal()
logger = Logger.create_logger(object=SMART_DATASTORE_LOCAL_CODE_LOGGER_OBJECT)


# TODO Can we make it a static method and avoid the default_table_name
#  parameter
def is_redis_table(table_name: str, default_table_name: str) -> bool:
    if table_name or default_table_name in ("test_mysql_table",
                                            "test_mysql_ml_table",
                                            "test_gender_table"):
        return True
    else:
        return False


# TODO Can we make it a method, rename it and remove the default_table_name
#  parameter
def generic_method(*, schema_name: str = None, table_name: str = None,
                   data_dict: dict = None,
                   ignore_duplicate: bool = False,
                   commit_changes: bool = True,
                   # Added as this is function and not a method
                   default_table_name: str = None
                   ) -> int:

    # TODO Run in parallel
    # self.generic_crud_mysql.insert
    result_mysql = None
    try:
        # result_mysql = generic_crud_mysql.insert(schema_name=schema_name,
        #                                table_name=table_name,
        #                                data_dict=data_dict,
        #                                ignore_duplicate=ignore_duplicate,
        #                                commit_changes=commit_changes)
        pass
    except Exception as e:
        print(f"Exception: {e}")
        logger.error(f"Exception: {e}")

    if is_redis_table(table_name=table_name,
                      default_table_name=default_table_name):
        try:
            # result_redis = generic_crud_redis.insert(
            #     schema_name=schema_name,
            #     table_name=table_name,
            #     data_dict=data_dict,
            #     ignore_duplicate=ignore_duplicate,
            #     commit_changes=commit_changes)
            pass
        except Exception as e:
            print(f"Exception: {e}")
            logger.info(f"Exception: {e}")
    else:
        logger.info(f"table_name {table_name} not in REDIS yet. Consider adding it in SmartDatastore. Later it will come from the database")
    return result_mysql


# Generic Datastore
class SmartDatastore (GenericCrudAbstract):
    def __init__(self, default_schema_name: str = None,
                 default_table_name: str = None,
                 default_view_table_name: str = None,
                 default_view_with_deleted_and_test_data: str = None,
                 default_column_name: str = None,
                 is_test_data: bool = False):
        super().__init__()
        self.generic_crud_mysql = GenericCrudMysql(
            default_schema_name=default_schema_name,
            default_table_name=default_table_name,
            default_view_table_name=default_view_table_name,
            default_view_with_deleted_and_test_data=default_view_with_deleted_and_test_data,
            default_column_name=default_column_name,
            is_test_data=is_test_data)
        self.generic_crud_redis = GenericCrudMysql(
            default_schema_name=default_schema_name,
            default_table_name=default_table_name,
            default_view_table_name=default_view_table_name,
            default_view_with_deleted_and_test_data=default_view_with_deleted_and_test_data,
            default_column_name=default_column_name,
            is_test_data=is_test_data)

    def insert(self, *, schema_name: str = None, table_name: str = None,
               data_dict: dict = None,
               ignore_duplicate: bool = False, commit_changes: bool = True
               ) -> int:
        result_redis = None
        # TODO Run in parallel
        # self.generic_crud_mysql.insert
        try:
            logger.info(f"inserting data_dict {data_dict} in MySQL")
            result_mysql = self.generic_crud_mysql.insert(
                schema_name=schema_name,
                table_name=table_name,
                data_dict=data_dict,
                ignore_duplicate=ignore_duplicate,
                commit_changes=commit_changes)
        except Exception as e:
            print(f"Exception: {e}")
            logger.error(f"Exception: {e}")

        logger.info(f"SmartDatastore: checking if table_name {table_name} is on REDIS")
        if is_redis_table(table_name=table_name,
                          default_table_name=self.generic_crud_mysql.default_table_name):
            logger.info(f"SmartDatastore: table_name {table_name} is on REDIS")
            try:
                result_redis = self.generic_crud_redis.insert(
                    schema_name=schema_name,
                    table_name=table_name,
                    data_dict=data_dict,
                    ignore_duplicate=ignore_duplicate,
                    commit_changes=commit_changes)
                logger.info(f"SmartDatastore: inserted data_dict {data_dict} in REDIS result_redis={result_redis}")
            except Exception as e:
                print(f"Exception: {e}")
                logger.info(f"Exception: {e}")
        else:
            logger.info(f"SmartDatastore: table_name {table_name} not in REDIS yet. Consider adding it in SmartDatastore. Later it will come from the database")

        # TODO Compare result_mysql and result_redis
        # if (result_mysql is not None and result_redis is not None
        #         and result_mysql != result_redis):
        #     logger.error(f"SmartDatastore: result_mysql {result_mysql} != \
        #                   result_redis {result_redis}")
        #     raise Exception(f"SmartDatastore: result_mysql {result_mysql} != \
        #                     result_redis {result_redis}")
        return result_mysql

    def select_multi_tuple_by_where(self, *, schema_name: str = None,
                                    view_table_name: str = None,
                                    select_clause_value: str = None,
                                    where: str = None, params: tuple = None,
                                    distinct: bool = False,
                                    limit: int = DEFAULT_SQL_SELECT_LIMIT,
                                    order_by: str = None) -> list:
        logger.info(f"SmartDatastore: select_multi_tuple_by_where: {select_clause_value}")
        print(f"SmartDatastore: select_multi_tuple_by_where: {select_clause_value}", flush=True)
        result_mysql = self.generic_crud_mysql.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name,
            select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit,
            order_by=order_by)
        return result_mysql


# for method_name in GenericCrudAbstract.__abstractmethods__:
#     setattr(SmartDatastore, method_name, generic_method(method_name))
