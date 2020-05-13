import attr
import typing


from kgtk.io.kgtkreader import KgtkReader

@attr.s(slots=True, frozen=False)
class KgtkMergeColumns:
    """Merge columns from multiple KgtkReaders, respecting predefined column
    names with aliases.

    """
    # For attrs 19.1.0 and later:
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)),
                                             factory=list)

    # Keep a record of the reserved columns with aliases as we encounter them.
    # We will retain the first alias encountered of each group.
    id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1)
    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1)
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1)
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1)

    # The column name map is a debugging convenience.  It is not required for
    # the merge algorithm.
    column_name_map: typing.MutableMapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                                      value_validator=attr.validators.instance_of(int)),
                                                               factory=dict)
    
    # Maintain a list of the old and new column name lists as a convenience
    # for debugging and feedback.
    old_column_name_lists: typing.List[typing.List[str]] = attr.ib(factory=list)
    new_column_name_lists: typing.List[typing.List[str]] = attr.ib(factory=list)

    def merge(self, kr: KgtkReader):
        """
        Add the columns from a KgtkReader into the merged column list,
        respecting predefined column names with aliases.

        Return a list of new column names for the KgtkReader, with
        predefined names replaced with the name first used in the 
        joint list of column names.
        """
        new_column_names: typing.List[str] = [ ]

        # Record the old column names for debugging.
        self.old_column_name_lists.append(kr.column_names)

        column_name: str
        idx: int = 0
        for idx, column_name in enumerate(kr.column_names):
            if idx == kr.id_column_idx:
                if self.id_column_idx >= 0:
                    column_name = self.column_names[self.id_column_idx]
                else:
                    self.idx_column_idx = len(self.column_names)

            elif idx == kr.node1_column_idx:
                if self.node1_column_idx >= 0:
                    column_name = self.column_names[self.node1_column_idx]
                else:
                    self.node1_column_idx = len(self.column_names)
            
            elif idx == kr.label_column_idx:
                if self.label_column_idx >= 0:
                    column_name = self.column_names[self.labelcolumn_idx]
                else:
                    self.label_column_idx = len(self.column_names)
            
            elif idx == kr.node2_column_idx:
                if self.node2_column_idx >= 0:
                    column_name = self.column_names[self.node2_column_idx]
                else:
                    self.node2_column_idx = len(self.column_names)
            
            new_column_names.append(column_name)
            if column_name not in self.column_name_map:
                self.column_name_map[column_name] = len(self.column_names)
                self.column_names.append(column_name)

        self.new_column_name_lists.append(new_column_names)
        return new_column_names
                    


