"""
This module updates files with a version string.

 * The version string contains a timestamp and a digest.
   * The digest identifies the content of the file.
     * Calcuated using blake2b
   * The timestamp indicates when a change was last detected.
 * The digest is calculated on the input file after removing
the version string from the input file.
   * If a version string is not detected in the input file,
     no action is taken on that file.
 * If the computed digest of the input file is different from
   the recorded digest:
   * The input file is updated with a new version string.
   * The input file is rewritten its filesystem.
"""

from argparse import ArgumentParser
import attr
import base64
import datetime as dt
import hashlib
from pathlib import Path
import re
import sys
import typing

from kgtk.utils.argparsehelpers import optional_bool

@attr.s(slots=True, frozen=True)
class UpdateVersion():
    UPDATE_VERSION: str = "2020-07-22T22:10:11.047901+00:00#uwVDNJhT34iJFhsPf5vafIhNdaD3xcZ0RxgPN9CPRmYY7cfpS5guHbAY7hApoK1aue3W+cz9ftP8kXJIK+budQ=="
    version_pattern: str = attr.ib(validator=attr.validators.instance_of(str), default=r'^\s*UPDATE_VERSION\s*:\s*str\s*=\s*"(?P<version>.*)"$')
    blake_bloke: str = attr.ib(validator=attr.validators.instance_of(str), default="UpdateVersionHsh")

    allow_updates: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    show_changes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Feedback and error output:
    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process_file(self, filepath: Path)->bool:
        hasher = hashlib.blake2b(person=self.blake_bloke.encode())
        version_pattern_re = re.compile(self.version_pattern.encode())

        current_version: typing.Optional[bytes] = None

        lines: typing.List[bytes] = []
        line: bytes
            
        if self.verbose:
            print("Checking the version of %s" % str(filepath), file=self.error_file, flush=True)
        with open(filepath, "rb") as ifile:
            for line in ifile:
                lines.append(line)
                matches = version_pattern_re.match(line)
                if matches:
                    # Retain the last match if multiple hits.
                    current_version = matches.group("version")
                    line = re.sub(rb'".*"', b'""', line)
                hasher.update(line)

        if current_version is None:
            if self.verbose:
                print("No version mark found in %s" % str(filepath))
            return False
        current_timestamp: bytes = b''
        current_digest: bytes = b''
        if len(current_version) > 0:
            current_timestamp, current_digest = current_version.split(b'#', 1)

        new_digest: bytes = base64.b64encode(hasher.digest())
        if new_digest == current_digest:
            if self.verbose:
                print("%s has not changed since %s" % (str(filepath), str(current_timestamp, "utf-8")), file=self.error_file, flush=True)
            return False

        if not self.allow_updates:
            if self.verbose:
                print("%s has changed since %s, but updates are disabled." % (str(filepath), str(current_timestamp, "utf-8")), file=self.error_file, flush=True)
            return True

        new_timestamp: bytes = dt.datetime.now(dt.timezone.utc).isoformat().encode()
        new_version: bytes = new_timestamp + b'#' + new_digest
        
        if self.verbose or self.show_changes:
            print("Updating the version mark in %s" % str(filepath), file=self.error_file, flush=True)
        with open(filepath, "wb") as ofile:
            for line in lines:
                matches = version_pattern_re.match(line)
                if matches:
                    line = re.sub(rb'".*"', b'"' + new_version + b'"', line)
                ofile.write(line)

        return True

    def process_files(self, filepaths: typing.List[Path])->int:
        """
        Returns the count of files that changed.
        """
        changes: int = 0
        filepath: Path
        for filepath in filepaths:
            if self.process_file(filepath):
                changes += 1


        if self.verbose:
            print("%d files updated" % changes, file=self.error_file, flush=True)

        return changes

def main():
    """
    Update version marks.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="filepaths", help="The file(s) to process", type=Path, nargs="+")

    parser.add_argument(       "--allow-updates", dest="allow_updates", type=optional_bool, nargs='?', const=True, default=True,
                               help="Allow updates. (default=%(default)s).")
    
    parser.add_argument(       "--show-changes", dest="show_changes", type=optional_bool, nargs='?', const=True, default=True,
                               help="Write a line for each changed file. (default=%(default)s).")
    
    parser.add_argument(       "--show-version", dest="show_version", type=optional_bool, nargs='?', const=True, default=False,
                               help="Print the version of this program. (default=%(default)s).")

    parser.add_argument("-v", "--verbose", dest="verbose", type=optional_bool, nargs='?', const=True, default=False,
                        help="Print additional progress messages (default=%(default)s).")
    
    args: Namespace = parser.parse_args()

    if args.show_version:
        print("Version: %s" % UpdateVersion.UPDATE_VERSION)

    updater: UpdateVersion = UpdateVersion(allow_updates=args.allow_updates,
                                           show_changes=args.show_changes,
                                           verbose=args.verbose)
    updater.process_files(args.filepaths)
    
if __name__ == "__main__":
    main()

