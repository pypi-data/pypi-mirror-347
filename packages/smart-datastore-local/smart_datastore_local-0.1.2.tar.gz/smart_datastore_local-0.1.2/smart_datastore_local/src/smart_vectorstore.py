# TODO move OurVectorDb to database-infrastructure-python-package
from opensearch_local.our_vector_db import OurVectorDb

# TODO Move generic_method to database-infrastructure-python-package
from smart_datastore import generic_method


class SmartVectorstore(OurVectorDb):
    pass


for method_name in OurVectorDb.__abstractmethods__:
    setattr(SmartVectorstore, method_name, generic_method(method_name))
