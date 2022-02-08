import os
import platform
import re
import subprocess
from pathlib import Path
from typing import (
    Iterator,
    List,
    Optional,
    Union,
)

from ActiveScout.components import ActiveStateProduct, FoundProductInfo
from ActiveScout.dirwalker import dirwalker


def _list_of_as_products() -> List:
    def _search_file_for_version_string(
        path_to_file: str, version_string_re: str
    ) -> str:
        found_match_str: str = ""
        with open(path_to_file, "rb") as f:
            for line in f:
                result = re.search(version_string_re, str(line))
                if result:
                    found_match_str = result.group(0)
                    break
        return found_match_str

    def get_linux_python_version(path_to_file: str) -> str:
        version_string_re: str = r"libpython(2|3)\.[0-9]+(\.[0-9]+)?"
        basename = os.path.basename(path_to_file)
        result = re.match(version_string_re, basename)
        if result:
            return result.group(0).split("libpython")[1]
        return ""

    def get_linux_perl_version(path_to_file: str) -> str:
        version_string_re: str = r"This is perl 5, version [0-9]+"
        found_match_str: str = _search_file_for_version_string(
            path_to_file, version_string_re
        )
        if found_match_str:
            return f"5.{found_match_str.split(' ')[-1]}"
        return ""

    def get_windows_python_version(path_to_file: str) -> str:
        version_string_re: str = r"ActivePython [23]\.[0-9].[0-9]+"
        version_string_re += r" \(ActiveState Software Inc\.\)"
        found_match_str: str = _search_file_for_version_string(
            path_to_file, version_string_re
        )
        if found_match_str:
            return found_match_str.split(" ")[1]
        return ""

    def get_windows_perl_version(path_to_file: str) -> str:
        version_string_re: str = r"This is perl 5, version [0-9]+"
        found_match_str: str = _search_file_for_version_string(
            path_to_file, version_string_re
        )
        if found_match_str:
            return f"5.{found_match_str.split(' ')[-1]}"
        return ""

    def get_macosx_python_version(path_to_file: str) -> str:
        version_string_re: str = r"libpython(2|3)\.[0-9]+(\.[0-9]+)?"
        basename = os.path.basename(path_to_file)
        result = re.match(version_string_re, basename)
        if result:
            return result.group(0).split("libpython")[1]
        return ""

    def get_macosx_perl_version(path_to_file: str) -> str:
        version_string_re: str = r"This is perl 5, version [0-9]+"
        found_match_str: str = _search_file_for_version_string(
            path_to_file, version_string_re
        )
        if found_match_str:
            return f"5.{found_match_str.split(' ')[-1]}"
        return ""

    products: List = []
    products.append(
        ActiveStateProduct(
            "ActivePython Linux",
            r"^libpython(2|3)\.[0-9]\.so",
            get_version_from_file=get_linux_python_version,
        )
    )
    products.append(
        ActiveStateProduct(
            "ActivePerl Linux",
            r"^perl$",
            get_version_from_file=get_linux_perl_version,
        )
    )
    products.append(
        ActiveStateProduct(
            "ActivePython Windows",
            r"^python(2|3)[0-9]\.dll$",
            get_version_from_file=get_windows_python_version,
        )
    )
    # could also use perl.exe here
    # keep it simple and only look for one thing
    products.append(
        ActiveStateProduct(
            "ActivePerl Windows",
            r"^(P|p)erl5[0-9]{1,2}\.dll$",
            get_version_from_file=get_windows_perl_version,
        )
    )
    products.append(
        ActiveStateProduct(
            "ActivePython Mac OSX",
            r"^libpython(2|3)\.[0-9]\.dylib",
            get_version_from_file=get_macosx_python_version,
        )
    )
    products.append(
        ActiveStateProduct(
            "ActivePerl Mac OSX",
            r"^perl-static$",
            get_version_from_file=get_macosx_perl_version,
        )
    )
    return products


def _accept_path_for_activestate(path) -> bool:
    files: List = [product.regex for product in _list_of_as_products()]

    p = Path(path)
    interesting_files_regex = re.compile("|".join(files))
    if interesting_files_regex.search(p.name):
        return True
    return False


# Code to convert that file into product/version given the path
def _convert_path_to_activestate_information(path: str) -> Optional[FoundProductInfo]:
    """
    Looks for ActiveState branding given a binary file.

    Returns None - if file does not have AS branding or is excluded
    """
    # file exclusion
    def excluded_filetype(path_to_file: Union[Path, str]) -> bool:
        # symlinks can still end up here, ignore them
        if os.path.islink(path_to_file):
            return True
        # exclude shell scripts on Linux
        if platform.system() == "Linux":
            file_type: str = subprocess.run(
                [
                    "file",
                    str(path_to_file),
                ],
                capture_output=True,
                text=True,
            ).stdout
            if re.search(r"POSIX shell script", file_type):
                return True
        return False

    pattern_re = re.compile(bytes("ActiveState", "utf-8"))
    with open(path, "rb") as f:
        for line in f:
            has_as_branding = pattern_re.search(line)
            if has_as_branding:
                products: List = _list_of_as_products()
                filename: str = Path(path).name
                for prod in products:
                    if re.match(prod.regex, filename) and not excluded_filetype(path):
                        summary_obj = FoundProductInfo(
                            path, prod.name, prod.get_version_from_file(path)
                        )
                        return summary_obj
    return None


# Function to filter None data out of a list
def _notNone(data) -> bool:
    if data is None:
        return False
    else:
        return True


def find_as_products() -> Iterator:
    """
    Returns a tuple with the following:
        - full path to file
        - ActiveState product the file is associated with
        - product version
    """
    files_to_check: Iterator[str] = dirwalker()
    interesting_files_to_scan = filter(_accept_path_for_activestate, files_to_check)
    as_products_found: Iterator = filter(
        _notNone,
        map(_convert_path_to_activestate_information, interesting_files_to_scan),
    )
    return as_products_found
