from argparse import ArgumentParser, Namespace, SUPPRESS
import attr
import hashlib
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from kgtk.value.kgtkvalue import KgtkValue

@attr.s(slots=True, frozen=True)
class KgtkIdBuilderOptions(KgtkFormat):
    DEFAULT_OVERWRITE: bool = False
    DEFAULT_VERIFY_ID_UNIQUE: bool = False

    # TODO: use an enum
    CONCAT_NLN_STYLE: str = "node1-label-node2" # node1-label-node2
    CONCAT_NL_NUM_STYLE: str = "node1-label-num" # node1-label-#
    CONCAT_NLN_NUM_STYLE: str = "node1-label-node2-num" # node1-label-node2-#
    CONCAT_WITH_OLD_ID_STYLE: str = "node1-label-node2-id" # Tag on any existing ID value
    EMPTY_STYLE: str = "empty" # DO not generate an ID (useful for debugging and other special circumstances)
    PREFIXED_STYLE: str = "prefix###" # XXX###
    WIKIDATA_STYLE: str = "wikidata" # node1-label-node2/hash
    WIKIDATA_WITH_CLAIM_ID_STYLE: str = "wikidata-with-claim-id" # node1-label-node2/hash-claimidhash

    STYLES: typing.List[str] = [
        CONCAT_NLN_STYLE,
        CONCAT_NL_NUM_STYLE,
        CONCAT_NLN_NUM_STYLE,
        CONCAT_WITH_OLD_ID_STYLE,
        EMPTY_STYLE,
        PREFIXED_STYLE,
        WIKIDATA_STYLE,
        WIKIDATA_WITH_CLAIM_ID_STYLE,
    ]
    DEFAULT_STYLE: str = PREFIXED_STYLE
    DEFAULT_CONCAT_NUM_WIDTH: int = 4
    DEFAULT_VALUE_HASH_WIDTH: int = 6
    DEFAULT_CLAIM_ID_HASH_WIDTH: int = 8
    DEFAULT_CLAIM_ID_COLUMN_NAME: str = "claim_id"

    # Defaults for prefixed style IDs.
    DEFAULT_PREFIX: str = "E"
    DEFAULT_INITIAL_ID: int = 1
    DEFAULT_PREFIX_NUM_WIDTH: int = 1

    DEFAULT_ID_SEPARATOR: str = "-"

    old_id_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    new_id_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    overwrite_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_OVERWRITE)
    verify_id_unique: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_VERIFY_ID_UNIQUE)
    id_style: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_STYLE)
    id_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_PREFIX)
    initial_id: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_INITIAL_ID)
    id_prefix_num_width: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_PREFIX_NUM_WIDTH)
    id_concat_num_width: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_CONCAT_NUM_WIDTH)
    value_hash_width: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_VALUE_HASH_WIDTH)
    claim_id_hash_width: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_CLAIM_ID_HASH_WIDTH)
    claim_id_column_name: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_CLAIM_ID_COLUMN_NAME)
    id_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_ID_SEPARATOR)

    @classmethod
    def add_arguments(cls, parser: ArgumentParser, expert: bool = False, overwrite: typing.Optional[bool] = None):

        # This helper function makes it easy to suppress options from
        # The help message.  The options are still there, and initialize
        # what they need to initialize.
        def h(msg: str)->str:
            if expert:
                return msg
            else:
                return SUPPRESS

        if overwrite is None:
            overwrite = cls.DEFAULT_OVERWRITE

        # This one is likely to cause conflicts in the future.
        #
        # The default value is indirect.
        parser.add_argument(      "--old-id-column-name", dest="old_id_column_name",
                                  metavar="COLUMN_NAME",
                                  help=h("The name of the old ID column. (default=id)."))
            
        parser.add_argument(      "--new-id-column-name", dest="new_id_column_name",
                                  metavar="COLUMN_NAME",
                                  help=h("The name of the new ID column. (default=id)."))
            
        parser.add_argument(      "--overwrite-id", dest="overwrite_id",
                                  metavar="optional true|false",
                                  help="When true, replace existing ID values.  When false, copy existing ID values. " +
                                  "When --overwrite-id is omitted, it defaults to %(default)s. " +
                                  "When --overwrite-id is supplied without an argument, it is %(const)s.",
                                  type=optional_bool, nargs='?', const=True, default=overwrite)

        parser.add_argument(      "--verify-id-unique", dest="verify_id_unique",
                                  metavar="optional true|false",
                                  help="When true, verify ID uniqueness using an in-memory set of IDs. " +
                                  "When --verify-id-unique is omitted, it defaults to %(default)s. " +
                                  "When --verify-id-unique is supplied without an argument, it is %(const)s. ",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_VERIFY_ID_UNIQUE)

        parser.add_argument(      "--id-style", dest="id_style", default=cls.DEFAULT_STYLE, choices=cls.STYLES,
                                  help=h("The ID generation style. (default=%(default)s)."))

        parser.add_argument(      "--id-prefix", dest="id_prefix", default=cls.DEFAULT_PREFIX,
                                  metavar="PREFIX",
                                  help=h("The prefix for a prefix### ID. (default=%(default)s)."))

        parser.add_argument(      "--initial-id", dest="initial_id", type=int, default=cls.DEFAULT_INITIAL_ID,
                                  metavar="INTEGER",
                                  help=h("The initial numeric value for a prefix### ID. (default=%(default)s)."))

        parser.add_argument(      "--id-prefix-num-width", dest="id_prefix_num_width", type=int, default=cls.DEFAULT_PREFIX_NUM_WIDTH,
                                  metavar="INTEGER",
                                  help=h("The width of the numeric value for a prefix### ID. (default=%(default)s)."))

        parser.add_argument(      "--id-concat-num-width", dest="id_concat_num_width", type=int, default=cls.DEFAULT_CONCAT_NUM_WIDTH,
                                  metavar="INTEGER",
                                  help=h("The width of the numeric value for a concatenated ID. (default=%(default)s)."))

        parser.add_argument(      '--value-hash-width', action="store", type=int, dest="value_hash_width", default=cls.DEFAULT_VALUE_HASH_WIDTH,
                                  help='How many characters should be used in a value hash? (default=%(default)d)')

        parser.add_argument(     '--claim-id-hash-width', action="store", type=int, dest="claim_id_hash_width", default=cls.DEFAULT_CLAIM_ID_HASH_WIDTH,
                                 help='How many characters should be used to hash the claim ID? 0 means do not hash the claim ID. (default=%(default)d)')

        parser.add_argument(     '--claim-id-column-name', action="store", type=str, dest="claim_id_column_name", default=cls.DEFAULT_CLAIM_ID_COLUMN_NAME,
                                 help='The name of the claim_id column. (default=%(default)s)')

        parser.add_argument(     '--id-separator', action="store", type=str, dest="id_separator", default=cls.DEFAULT_ID_SEPARATOR,
                                 help='The separator user between ID subfields. (default=%(default)s)')


    @classmethod
    def from_dict(cls, d: dict)->'KgtkIdBuilderOptions':
        return cls(
            old_id_column_name=d.get("old_id_column_name"),
            new_id_column_name=d.get("new_id_column_name"),
            overwrite_id=d.get("overwrite_id", False),
            verify_id_unique=d.get("verify_id_unique", False),
            id_style=d.get("id_style", cls.PREFIXED_STYLE),
            id_prefix=d.get("id_prefix", cls.DEFAULT_PREFIX),
            initial_id=d.get("initial_id", cls.DEFAULT_INITIAL_ID),
            id_prefix_num_width=d.get("id_prefix_num_width", cls.DEFAULT_PREFIX_NUM_WIDTH),
            id_concat_num_width=d.get("id_concat_num_width", cls.DEFAULT_CONCAT_NUM_WIDTH),
            value_hash_width=d.get("value_hash_width", cls.DEFAULT_VALUE_HASH_WIDTH),
            claim_id_hash_width=d.get("claim_id_hash_width", cls.DEFAULT_CLAIM_ID_HASH_WIDTH),
            claim_id_column_name=d.get("claim_id_column_name", cls.DEFAULT_CLAIM_ID_COLUMN_NAME),
            id_separator=d.get("id_separator", cls.DEFAULT_ID_SEPARATOR),
        )

    # Build the value parsing option structure.
    @classmethod
    def from_args(cls, args: Namespace)->'KgtkIdBuilderOptions':
        return cls.from_dict(vars(args))

    def show(self, out: typing.TextIO=sys.stderr):
        if self.old_id_column_name is not None:
            print("--old-id-column-name=%s" % str(self.old_id_column_name), file=out, flush=True)
        if self.new_id_column_name is not None:
            print("--new-id-column-name=%s" % str(self.new_id_column_name), file=out, flush=True)
        print("--overwrite-id=%s" % str(self.overwrite_id), file=out, flush=True)
        print("--verify_id_unique=%s" % str(self.verify_id_unique), file=out, flush=True)
        print("--id-style=%s" % str(self.id_style), file=out, flush=True)
        print("--id-prefix=%s" % repr(self.id_prefix), file=out, flush=True)
        print("--initial-id=%s" % str(self.initial_id), file=out, flush=True)
        print("--id-prefix-num-width=%s" % str(self.id_prefix_num_width), file=out, flush=True)
        print("--id-concat-num-width=%s" % str(self.id_concat_num_width), file=out, flush=True)
        print("--value-hash-width=%s" % str(self.value_hash_width), file=out, flush=True)
        print("--claim-id-hash-width=%s" % str(self.claim_id_hash_width), file=out, flush=True)
        print("--claim-id-column-name=%s" % repr(self.claim_id_column_name), file=out, flush=True)
        print("--id-separator=%s" % repr(self.id_separator), file=out, flush=True)


@attr.s(slots=True, frozen=False)
class KgtkIdBuilder(KgtkFormat):
    options: KgtkIdBuilderOptions = attr.ib(validator=attr.validators.instance_of(KgtkIdBuilderOptions))

    column_names: typing.List[str]= attr.ib() # TODO: add validator

    old_id_column_name: str = attr.ib(validator=attr.validators.instance_of(str))
    old_id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    new_id_column_name: str = attr.ib(validator=attr.validators.instance_of(str))
    new_id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    add_new_id_column: bool = attr.ib(validator=attr.validators.instance_of(bool))

    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    label_column_idx: int= attr.ib(validator=attr.validators.instance_of(int))
    node2_column_idx: int= attr.ib(validator=attr.validators.instance_of(int))

    claim_id_column_idx: int= attr.ib(validator=attr.validators.instance_of(int))

    current_id: int = attr.ib(validator=attr.validators.instance_of(int))

    id_set: typing.Set[str] =attr.ib(validator=attr.validators.instance_of(set), factory=set)

    nl_keys: typing.MutableMapping[str, int] = attr.ib(validator=attr.validators.instance_of(dict), factory=dict)

    @classmethod
    def new(cls,
            kr: KgtkReader,
            options: KgtkIdBuilderOptions,
    )->'KgtkIdBuilder':
        """
        This is the KgtkIdBuilder factory method.
        """
        column_names: typing.List[str] = kr.column_names.copy()
        column_name_map: typing.Mapping[str, int] = kr.column_name_map
        node1_column_idx: int = kr.node1_column_idx
        label_column_idx: int = kr.label_column_idx
        node2_column_idx: int = kr.node2_column_idx
        id_column_idx: int = kr.id_column_idx

        return cls.new1(column_names, column_name_map, node1_column_idx, label_column_idx, node2_column_idx, id_column_idx, options)

    @classmethod
    def from_column_names(cls,
             column_names: typing.List[str],
             options: KgtkIdBuilderOptions,
    )->'KgtkIdBuilder':
        column_name_map: typing.MutableMapping[str, int] = { }
        column_idx: int
        column_name: str
        for column_idx, column_name in enumerate(column_names):
            column_name_map[column_name] = column_idx
        
        node1_column_idx: int
        label_column_idx: int
        node2_column_idx: int
        id_column_idx: int

        node1_column_idx, label_column_idx, node2_column_idx, id_column_idx = \
            KgtkReader.get_special_columns(column_name_map, "", "idbuilder")

        return cls.new1(column_names, column_name_map, node1_column_idx, label_column_idx, node2_column_idx, id_column_idx, options)

    @classmethod
    def new1(cls,
             column_names: typing.List[str],
             column_name_map: typing.Mapping[str, int],
             node1_column_idx: int,
             label_column_idx: int,
             node2_column_idx: int,
             id_column_idx: int,
             options: KgtkIdBuilderOptions,
    )->'KgtkIdBuilder':

        # Find the old ID column.
        old_id_column_idx: int
        old_id_column_name: str
        if options.old_id_column_name is not None:
            # The old ID column was explicitly named.
            old_id_column_name = options.old_id_column_name
            if old_id_column_name in column_name_map:
                # The new ID column already exists.
                old_id_column_idx = column_name_map[old_id_column_name]
            else:
                raise ValueError("The old ID column named '%s' is not known." % options.old_id_column_name)
        else:
            # The old ID column was not explicitly named.
            if id_column_idx >= 0:
                # The input file has an ID column.  Use it.
                old_id_column_name = column_names[id_column_idx]
                old_id_column_idx = id_column_idx
            else:
                # There is not old ID column index.
                old_id_column_idx = -1
                old_id_column_name = ""

        # Find the new ID column.
        new_id_column_idx: int
        add_new_id_column: bool
        new_id_column_name: str
        if options.new_id_column_name is not None:
            # The new ID column was explicitly named.
            new_id_column_name = options.new_id_column_name
            if new_id_column_name in column_name_map:
                # The new ID column already exists.
                new_id_column_idx = column_name_map[new_id_column_name]
                add_new_id_column = False
            else:
                # Create a new ID column.
                new_id_column_idx = len(column_names)
                column_names.append(new_id_column_name)
                add_new_id_column = True
        else:
            # The new ID column was not explicitly named.
            if id_column_idx >= 0:
                # The input file has an ID column.  Use it.
                new_id_column_name = column_names[id_column_idx]
                new_id_column_idx = id_column_idx
                add_new_id_column = False
            else:
                # Create a new ID column.
                new_id_column_idx = len(column_names)
                new_id_column_name = KgtkFormat.ID
                column_names.append(KgtkFormat.ID)
                add_new_id_column = True

        claim_id_column_idx: int = column_name_map.get(options.claim_id_column_name, -1)

        # Any prerequisites?
        if options.id_style == KgtkIdBuilderOptions.CONCAT_NLN_STYLE:
            if node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if label_column_idx < 0:
                raise ValueError("No label column index")
            if node2_column_idx < 0:
                raise ValueError("No node2 column index")

        elif options.id_style == KgtkIdBuilderOptions.CONCAT_NL_NUM_STYLE:
            if node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if label_column_idx < 0:
                raise ValueError("No label column index")

        elif options.id_style == KgtkIdBuilderOptions.CONCAT_NLN_NUM_STYLE:
            if node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if label_column_idx < 0:
                raise ValueError("No label column index")
            if node2_column_idx < 0:
                raise ValueError("No node2 column index")

        elif options.id_style == KgtkIdBuilderOptions.CONCAT_WITH_OLD_ID_STYLE:
            if node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if label_column_idx < 0:
                raise ValueError("No label column index")
            if node2_column_idx < 0:
                raise ValueError("No node2 column index")
            if old_id_column_idx < 0:
                raise ValueError("No old ID column index")

        elif options.id_style == KgtkIdBuilderOptions.WIKIDATA_STYLE:
            if node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if label_column_idx < 0:
                raise ValueError("No label column index")
            if node2_column_idx < 0:
                raise ValueError("No node2 column index")
        
        elif options.id_style == KgtkIdBuilderOptions.WIKIDATA_WITH_CLAIM_ID_STYLE:
            if node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if label_column_idx < 0:
                raise ValueError("No label column index")
            if node2_column_idx < 0:
                raise ValueError("No node2 column index")
            if claim_id_column_idx < 0:
                raise ValueError("No claim_id column index")
        
        return cls(options=options,
                   column_names=column_names,
                   old_id_column_name=old_id_column_name,
                   old_id_column_idx=old_id_column_idx,
                   new_id_column_name=new_id_column_name,
                   new_id_column_idx=new_id_column_idx,
                   add_new_id_column=add_new_id_column,
                   node1_column_idx=node1_column_idx,
                   label_column_idx=label_column_idx,
                   node2_column_idx=node2_column_idx,
                   claim_id_column_idx=claim_id_column_idx,
                   current_id=options.initial_id
        )

    def verify_uniqueness(self, id_value: str, row: typing.List[str], line_number, who: str):
        """
        Verify that ID values are not repeated.  This is OK for the output
        of `kgtk compact`, but is a little too strong for general use.
        The weaker constraint should be that the ID values don't repeat
        with different (node1, label, node2) tuples in an edge file.
        """
        if KgtkFormat.LIST_SEPARATOR in id_value:
            # The ID value might be a list.
            id_v: str
            for id_v in KgtkValue.split_list(id_value):
                if id_v in self.id_set:
                    # TODO: Probably want more error handling options, such as
                    # printing the offending row and choosing to continue.
                    raise ValueError("Line %d: %s ID '%s' duplicates a previous ID '%s'." % (line_number, who, id_value, id_v))
                else:
                    self.id_set.add(id_v)
        else:
            # Not a list, we can process this faster.
            if id_value in self.id_set:
                # TODO: Probably want more error handling options, such as
                # printing the offending row and choosing to continue.
                raise ValueError("Line %d: %s ID '%s' duplicates a previous ID '%s'." % (line_number, who, id_value, id_value))
            else:
                self.id_set.add(id_value)
        

    def build(self, row: typing.List[str], line_number: int)->typing.List[str]:
        """
        Build a new ID value if needed.
        """
        row = row.copy() # as a precaution
        if self.add_new_id_column:
            row.append("")
        elif self.old_id_column_idx >= 0:
            if row[self.old_id_column_idx] != "" and not self.options.overwrite_id:
                if self.new_id_column_idx != self.old_id_column_idx:
                    row[self.new_id_column_idx] = row[self.old_id_column_idx]
                if self.options.verify_id_unique:
                    self.verify_uniqueness(row[self.old_id_column_idx], row, line_number, "existing")

                return row

        # Perhaps we also want to lookup (node1, label, node2), and if an ID
        # has already been assigned, reuse it.

        new_id: str
        if self.options.id_style == KgtkIdBuilderOptions.CONCAT_NLN_STYLE:
            new_id = self.build_concat_nln(row)
        elif self.options.id_style == KgtkIdBuilderOptions.CONCAT_NL_NUM_STYLE:
            new_id = self.build_concat_nl_num(row)
        elif self.options.id_style == KgtkIdBuilderOptions.CONCAT_NLN_NUM_STYLE:
            new_id = self.build_concat_nln_num(row)
        elif self.options.id_style == KgtkIdBuilderOptions.CONCAT_WITH_OLD_ID_STYLE:
            new_id = self.build_concat_with_old_id(row)
        elif self.options.id_style == KgtkIdBuilderOptions.PREFIXED_STYLE:
            new_id = self.build_prefixed(row)
        elif self.options.id_style == KgtkIdBuilderOptions.EMPTY_STYLE:
            new_id = "" # Useful for debugging and other unusual circumstances.
        elif self.options.id_style == KgtkIdBuilderOptions.WIKIDATA_STYLE:
            new_id = self.build_wikidata_id(row)
        elif self.options.id_style == KgtkIdBuilderOptions.WIKIDATA_WITH_CLAIM_ID_STYLE:
            new_id = self.build_wikidata_id_with_claim_id(row)
        else:
            raise ValueError("Unknown ID style '%s'." % self.options.id_style)

        row[self.new_id_column_idx] = new_id
        if self.options.verify_id_unique:
            self.verify_uniqueness(new_id, row, line_number, "new")
        return row

    def build_concat_nln(self, row: typing.List[str])->str:
        return row[self.node1_column_idx] + self.options.id_separator + row[self.label_column_idx] + self.options.id_separator + row[self.node2_column_idx]

    def build_concat_nl_num(self, row: typing.List[str])->str:
        # Returns node1-label-### where ### starts at 0.
        # Assumes that records are compact on (node2) or (node2, id), as needed.
        key: str = row[self.node1_column_idx] + self.options.id_separator + row[self.label_column_idx]
        if key in self.nl_keys:
            self.nl_keys[key] += 1
        else:
            self.nl_keys[key] = 0
        return key + self.options.id_separator + str(self.nl_keys[key]).zfill(self.options.id_concat_num_width)

    def build_concat_nln_num(self, row: typing.List[str])->str:
        # Returns node1-label-node2-### where ### starts at 0.
        # Assumes that records are compact on (node2) or (node2, id), as needed.
        key: str = row[self.node1_column_idx] + self.options.id_separator + row[self.label_column_idx] + self.options.id_separator + row[self.node2_column_idx]
        if key in self.nl_keys:
            self.nl_keys[key] += 1
        else:
            self.nl_keys[key] = 0
        return key + self.options.id_separator + str(self.nl_keys[key]).zfill(self.options.id_concat_num_width)

    def build_concat_with_old_id(self, row: typing.List[str])->str:
        key: str = row[self.node1_column_idx] + self.options.id_separator + row[self.label_column_idx] + self.options.id_separator + row[self.node2_column_idx]
        if row[self.old_id_column_idx] != "":
            key += self.options.id_separator + row[self.old_id_column_idx]
        return key

    def build_prefixed(self, row: typing.List[str])->str:
        new_id: str =  self.options.id_prefix + str(self.current_id).zfill(self.options.id_prefix_num_width)
        self.current_id += 1
        return new_id

    def build_wikidata_id(self, row: typing.List[str])->str:
        node2_value: str = row[self.node2_column_idx]
        if self.options.value_hash_width > 0 and node2_value.startswith(('L', 'P', 'Q')):
            return self.build_concat_nln(row)
        else:
            return row[self.node1_column_idx] + self.options.id_separator + row[self.label_column_idx] + self.options.id_separator + \
                hashlib.sha256(node2_value.encode('utf-8')).hexdigest()[:self.options.value_hash_width]

    def build_wikidata_id_with_claim_id(self, row: typing.List[str])->str:
        claim_id: str = row[self.claim_id_column_idx]
        if len(claim_id) == 0:
            # TODO: Perhaps raise an exception?
            return self.build_wikidata_id(row)

        elif self.options.claim_id_hash_width == 0:
            return self.build_wikidata_id(row) + self.options.id_separator + claim_id.lower()

        else:
            return self.build_wikidata_id(row) + self.options.id_separator + hashlib.sha256(claim_id.lower().encode('utf-8')).hexdigest()[:self.options.claim_id_hash_width]

    def process(self, kr: KgtkReader, kw: KgtkWriter):
        line_number: int = 0
        row: typing.List[str]
        for row in kr:
            line_number += 1
            kw.write(self.build(row, line_number))

def main():
    """
    Test the KGTK ID builder.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data (default=%(default)s)", type=Path, nargs="?", default="-")
    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    KgtkIdBuilderOptions.add_arguments(parser)
    
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_args(args)    
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    # First create the KgtkReader.  It provides parameters used by the ID
    # column builder. Next, create the ID column builder, which provides a
    # possibly revised list of column names for the KgtkWriter.  Last, create
    # the KgtkWriter.

    # Open the input file.
    kr: KgtkReader =  KgtkReader.open(args.input_file_path,
                                      error_file=error_file,
                                      options=reader_options,
                                      value_options = value_options,
                                      verbose=args.verbose,
                                      very_verbose=args.very_verbose,
    )

    # Create the ID builder.
    idb: KgtkIdBuilder = KgtkIdBuilder.new(kr, idbuilder_options)

    # Open the output file.
    ew: KgtkWriter = KgtkWriter.open(idb.column_names,
                                     args.output_file_path,
                                     mode=kr.mode,
                                     require_all_columns=True,
                                     prohibit_extra_columns=True,
                                     fill_missing_columns=False,
                                     gzip_in_parallel=False,
                                     verbose=args.verbose,
                                     very_verbose=args.very_verbose)

    # Process the input file, building IDs.
    idb.process(kr, ew)

    ew.close()
    kr.close()

if __name__ == "__main__":
    main()
