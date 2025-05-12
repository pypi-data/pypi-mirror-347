from typing import Type

from ..model_base import AdminModel


def get_default_column_renderers():
    # NB: order matters (first one handling it wins)
    return [
        ModelColumnRenderer,
    ]


class ColumnRenderer:
    @classmethod
    def handles(cls, admin, ModelType: AdminModel, column: dict[str, str]):
        """
        Return True if this renderer can render the column 'key' in `ModelType`.
        """
        return False

    def __init__(self, admin, ModelType: AdminModel, column: dict[str, str]):
        super(ColumnRenderer).__init__()
        self.admin = admin
        self.ModelType = ModelType
        self.column = column

    def apply(self, table):
        raise NotImplementedError()


class ModelColumnRenderer(ColumnRenderer):
    @classmethod
    def handles(cls, admin, ModelType: Type[AdminModel], column: dict[str, str]):
        """
        Return True if this renderer can render the column 'key' in `ModelType`.
        """
        field_name = column["field"]
        field = ModelType.model_fields.get(field_name)
        if field is None:
            return False
        return True

    def apply(self, table):
        print("APPLY", self, self.column)
        card_prefix = f"{self.admin.prefix}/{self.ModelType.__name__}"
        table.add_slot(
            f"body-cell-{self.column['field']}",
            f"""
            <q-td :props="props">
                <q-chip esize="xs">
                <a :href="'{card_prefix}/'+props.row.name.value">{{{{ props.value }}}}</a>
                </q-chip>
            </q-td>
            """,
        )
