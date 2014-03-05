from .base import Plugin
from ..operation import Operation
from ..utils import versioned_column_properties


class NullDeletePlugin(Plugin):
    def should_nullify_column(self, version_obj, prop):
        """
        Return whether or not given column of given version object should
        be nullified (set to None) at the end of the transaction.

        :param version_obj:
            Version object to check the attribute nullification
        :paremt attr:
            SQLAlchemy ColumnProperty object
        """
        return (
            version_obj.operation_type == Operation.DELETE and
            not prop.columns[0].primary_key and
            prop.key !=
            self.manager.option(
                version_obj,
                'transaction_column_name'
            )
        )

    def after_create_history_object(self, uow, parent_obj, version_obj):
        for prop in versioned_column_properties(parent_obj):
            if self.should_nullify_column(version_obj, prop):
                setattr(version_obj, prop.key, None)