"""
Constants and helpers for the KGTK file format.

"""

import typing

class KgtkFormat:
    COLUMN_SEPARATOR: str = "\t"
    COMMENT_INDICATOR: str = "#"

    # These are the required columns in an edge file:
    NODE1_COLUMN_NAMES: typing.List[str] = ["node1", "from", "subject"]
    NODE2_COLUMN_NAMES: typing.List[str] = ["node2", "to", "object"]
    LABEL_COLUMN_NAMES: typing.List[str] = ["label", "predicate", "relation", "relationship"]

    # There is only one required column in a node file:
    ID_COLUMN_NAMES: typing.List[str] = ["id", "ID"]

    @classmethod
    def get_column_idx(cls,
                       name_or_aliases: typing.List[str],
                       column_name_map: typing.Mapping[str, int],
                       is_optional: bool = False)->int:
        """
        Get the indices of the required column using one of its allowable names.
        Return -1 if the column is not found and is optional.
        """
        found_column_name: str = ""
        column_idx: int = -1
        col_name: str
        for col_name in name_or_aliases:
            if col_name in column_name_map:
                if column_idx >= 0:
                    # TODO: throw a better exception
                    raise ValueError("Ambiguous node1 column names %s and %s" % (found_column_name, col_name))
                column_idx = column_name_map[col_name]
                found_column_name = col_name
        if column_idx < 0 and not is_optional:
            # TODO: throw a better exception:
            raise ValueError("Missing required column: %s" % " | ".join(name_or_aliases))
        return column_idx

    @classmethod
    def build_column_name_map(cls, column_names: typing.List[str])->typing.Mapping[str, int]:
        # Validate the column names and build a map from column name
        # to column index.
        column_name_map: typing.MutableMapping[str, int] = { }
        column_idx: int = 0 # There may be a more pythonic way to do this
        column_name: str
        for column_name in column_names:
            if column_name is None or len(column_name) == 0:
                # TODO: throw a better exception
                raise ValueError("Column %d has an invalid name in the file header" % column_idx)

            # Ensure that columns names are not duplicated:
            if column_name in column_name_map:
                # TODO: throw a better exception
                raise ValueError("Column %d (%s) is a duplicate of column %d" % (column_idx, column_name, column_name_map[column_name]))

            column_name_map[column_name] = column_idx
            column_idx += 1
        return column_name_map

    @classmethod
    def required_edge_columns(cls, column_name_map: typing.Mapping[str, int])->typing.Tuple[int, int, int]:
        # Ensure that the three required columns are present:
        node1_column_idx: int = cls.get_column_idx(cls.NODE1_COLUMN_NAMES, column_name_map)
        node2_column_idx: int = cls.get_column_idx(cls.NODE2_COLUMN_NAMES, column_name_map)
        label_column_idx: int = cls.get_column_idx(cls.LABEL_COLUMN_NAMES, column_name_map)

        return (node1_column_idx, node2_column_idx, label_column_idx)

    @classmethod
    def additional_edge_columns(cls, column_names: typing.List[str])->typing.List[str]:
        """
        Return a list of column names in this file excluding the required columns.
        """
        additional_columns: typing.List[str] = [ ]
        column_name: str
        for column_name in column_names:
            if column_name not in KgtkFormat.NODE1_COLUMN_NAMES and \
               column_name not in KgtkFormat.NODE2_COLUMN_NAMES and \
               column_name not in KgtkFormat.LABEL_COLUMN_NAMES:
                additional_columns.append(column_name)
        return additional_columns

    @classmethod
    def required_node_column(cls, column_name_map: typing.Mapping[str, int])->int:
        # Ensure that the required column is present:
        return cls.get_column_idx(cls.ID_COLUMN_NAMES, column_name_map)

    @classmethod
    def additional_node_columns(cls, column_names: typing.List[str])->typing.List[str]:
        """
        Return a list of column names in this file excluding the required columns.
        """
        additional_columns: typing.List[str] = [ ]
        column_name: str
        for column_name in column_names:
            if column_name not in KgtkFormat.ID_COLUMN_NAMES:
                additional_columns.append(column_name)
        return additional_columns
    
