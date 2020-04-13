"""
Constants and helpers for the KGTK file format.

"""

import typing

class KgtkFormat:
    NODE1_COLUMN_NAME: str = "node1"
    NODE2_COLUMN_NAME: str = "node2"
    LABEL_COLUMN_NAME: str = "label"

    REQUIRED_COLUMN_NAMES: typing.List[str] = [ NODE1_COLUMN_NAME, NODE2_COLUMN_NAME, LABEL_COLUMN_NAME ]

    @classmethod
    def validate_kgtk_edge_columns(cls, column_names: typing.List[str])->typing.Mapping[str, int]:
        if len(column_names) < 3:
            # TODO: throw a better exception
            raise ValueError("The edge file header must have at least three columns.")

        # Validate the column names and build a map from column name
        # to column index.
        column_name_map: typing.MutableMapping[str, int] = { }
        column_idx: int = 0 # There may be a more pythonic way to do this
        column_name: str
        for column_name in column_names:
            if column_name is None or len(column_name) == 0:
                # TODO: throw a better exception
                raise ValueError("Column %d has an invalid name in the edge file header" % column_idx)

            # Ensure that columns names are not duplicated:
            if column_name in column_name_map:
                # TODO: throw a better exception
                raise ValueError("Column %d (%s) is a duplicate of column %d" % (column_idx, column_name, column_name_map[column_name]))

            column_name_map[column_name] = column_idx
            column_idx += 1

         # Ensure that the three require columns are present:
        if cls.NODE1_COLUMN_NAME not in column_name_map:
            # TODO: throw a better exception
            raise ValueError("Missing node1 column in the edge file header")
        if cls.NODE2_COLUMN_NAME not in column_name_map:
            # TODO: throw a better exception
            raise ValueError("Missing node2 column in the edge file header")
        if cls.LABEL_COLUMN_NAME not in column_name_map:
            # TODO: throw a better exception
            raise ValueError("Missing label column in the edge file header")

        return column_name_map
