import os
import json
import yaml
import shutil
import traceback
from pathlib import Path
from .text import current_time
from .types import is_string, is_array, is_list
from typing import Any, Literal, Optional, Union, Sequence, List, Tuple, Dict
from .misc import flatten_list, filter_list


def scan_dir(
    path: Union[str, Path],
    pattern: Optional[str] = None,
    expected_dir: Literal["file", "path", "any"] = "any",
) -> list[Path]:
    path = Path(path)
    if expected_dir == "file":
        fn_checker = lambda path: Path.is_file(path)
    else:
        fn_checker = lambda path: Path.is_dir(path)
    if not pattern:
        pattern = "*"
    return [x for x in Path(path).glob(pattern) if fn_checker(x)]


def _validate_path_messages(
    entry: Union[str, Path],
    expected_dir: Literal["file", "path", "any"],
    error_type: Literal["unexpected_path", "path_not_exist", "invalid_type"],
):
    if error_type == "invalid_type":
        return f"Invalid type provided, received: '{type(entry)}' while expected 'str', 'bytes' or 'Path'."

    entry = str(entry).replace("\\", "/")
    if error_type == "path_not_exist":
        return 'The provided Path "{}" does not exist!'.format(entry)

    match expected_dir: # unexpected_path
        case "any":
            return 'The provided Path "{}" is not a valid directory or file.'.format(
                entry
            )
        case "file":
            return 'The provided Path "{}" is not a valid directory. It is a file not a directory!'.format(
                entry
            )
        case "path":
            return 'The provided Path "{}" is not a valid file. It is a directory and not a file!'.format(
                entry
            )


def validate_path(
    entry: Union[str, Path],
    expected_dir: Literal["file", "path", "any"] = "any",
    *,
    raise_exception: bool = False,
) -> bool:
    """Checks if `entry` is a valid existent path."""
    if not isinstance(entry, (str, bytes, Path)):
        if raise_exception:
            raise ValueError(_validate_path_messages(entry, expected_dir, "invalid_type"))
        return False
    if not Path(entry).exists():
        if raise_exception:
            raise ValueError(_validate_path_messages(entry, expected_dir, "path_not_exist"))
        return False
    entry = Path(entry)
    if expected_dir == "any":
        if raise_exception:
            raise ValueError(_validate_path_messages(entry, expected_dir, "unexpected_path"))
        return True
    else:
        is_file_type = entry.is_file()
        if expected_dir == "file":
            if not is_file_type and raise_exception:
                raise ValueError(_validate_path_messages(entry, expected_dir, "unexpected_path"))
            return is_file_type
        if is_file_type and raise_exception:
            raise ValueError(_validate_path_messages(entry, expected_dir, "unexpected_path"))
        return not is_file_type


def get_folders(
    path: Union[str, Path],
    pattern: str = "*",
    *args,
    **kwargs,
) -> list[Path] | list:
    if is_list(path):
        results = []
        paths = [x for x in path if validate_path(x, expected_dir="path")]
        if not paths:
            return []
        [
            results.extend(scan_dir(x, pattern=pattern, expected_dir="path"))
            for x in paths
        ]
        return list(sorted(results))
    if not validate_path(path, "path"):
        return []
    return scan_dir(path, pattern=pattern, expected_dir="path")


def _get_files_ext_set(extension: str):
    if extension.startswith("*."):
        return extension
    if extension.startswith("."):
        return "*" + extension
    return "*." + extension


def get_files(
    path: Union[List[Union[str, Path]], str, Path],
    extensions: Optional[Union[str, List[str], Tuple[str]]] = None,
    *args,
    **kwargs,
) -> list[Path] | list:
    results = []
    if is_list(path):
        paths = [Path(x) for x in path if validate_path(x, expected_dir="path")]
        if not paths:
            return results
        [results.extend(get_files(_path, extensions=extensions)) for _path in paths]
        return list(sorted(results))
    else:
        if not validate_path(path, expected_dir="path"):
            return results
        if is_array(extensions):
            [
                results.extend(
                    scan_dir(
                        path,
                        pattern=_get_files_ext_set(extension),
                        expected_dir="file",
                    )
                )
                for extension in extensions
            ]
        elif is_string(extensions):
            results.extend(
                scan_dir(
                    path,
                    pattern=_get_files_ext_set(extensions),
                    expected_dir="file",
                )
            )
        return list(sorted(results))


def path_to_string(path: Path):
    assert isinstance(path, (Path, str, bytes)), "Invalid Path format"
    return str(Path(path)).replace("\\", "/")


def mkdir(
    *paths: Union[Path, str],
):
    Path(*[x for x in paths if isinstance(x, (bytes, str, Path))]).mkdir(
        parents=True, exist_ok=True
    )


def setup_path(
    *paths: Union[str, Path],
    mkdir_path: bool = False,
    return_original: bool = False,
    **kwargs,
) -> Union[str, Path]:
    """
    The function `setup_path` takes in multiple paths as arguments, creates directories if specified,
    and returns the path as a string with forward slashes.

    Args:
      paths (str | Path): The paths that are to be managed.
      mkdir_path (bool): Create the directory specified in the path if it does not already exist. If `mkdir_path` is set to `True` and the directory does not exist, the function will create the directory. Defaults to False
      return_original (bool): Determines whether the function should return the type of the path (as a `Path` object) instead of the path as a string. If `return_original` is set to `True`, the function. Defaults to False

    Returns:
      The function `setup_path` returns a string representation of the path with backslashes replaced by forward slashes or as a `Path` object if `return_original` is set to True.
    """
    path = Path(*[x for x in paths if isinstance(x, (bytes, str, Path))])
    if mkdir_path and not path.exists():
        mkdir(m_path=path.parent if "." in path.name else path)
    if return_original:
        return path
    return str(path).replace("\\", "/")


def load_json(
    path: Union[str, Path],
    default_value: Optional[Any] = None,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    *args,
    **kwargs,
) -> list | dict | None:
    """
    Load JSON/JSONL data from a file.

    Args:
        path (Union[str, Path]): The path to the JSON file.

    Returns:
        Union[list, dict, None]: The loaded JSON data as a list, dictionary, or None if any error occurs.
    """

    if not validate_path(path, expected_dir="file"):
        if default_value is None:
            raise FileNotFoundError(f"Invalid path '{path}'")
        return default_value
    path = Path(path)
    file = path.read_text(encoding=encoding, errors=errors)
    if path.name.endswith(".jsonl"):
        results = []
        for line in file.splitlines():
            try:
                results.append(json.loads(line))
            except Exception as e:
                pass
        return results
    try:
        return json.loads(file)
    except:
        return default_value


def save_json(
    path: Union[str, Path],
    content: Union[list, dict, tuple, map, str, bytes],
    indent: int = 4,
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    **kwargs,
) -> None:
    """
    Save JSON data to a file.

    Args:
        path (Union[str, Path]): The path to save the JSON file.
        content (Union[list, dict]): The content to be saved as JSON.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".
        indent (int, optional): The indentation level in the saved JSON file. Defaults to 4.
    """

    if not is_string(path):
        path = current_time() + ".json"
    path = Path(path)
    if not path.name.endswith((".json", ".jsonl")):
        path = Path(path.parent, f"{path.name}.json")
    mkdir(Path(path).parent)
    if path.name.endswith(".jsonl"):
        if not isinstance(content, (str, bytes)):
            content = json.dumps(content)
        if path.exists():
            older_content = path.read_text(encoding=encoding, errors=errors)
            content = older_content.rstrip() + "\n" + content
    else:
        content = json.dumps(content, indent=indent)
    path.write_text(content, encoding=encoding, errors=errors)


def load_text(
    path: Union[Path, str],
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    default_value: Optional[Any] = None,
    **kwargs,
) -> str:
    if not validate_path(path, expected_dir="file"):
        if default_value is None:
            raise FileNotFoundError(f"Invalid path '{path}'")
        return default_value
    return Path(path).read_text(encoding, errors=errors)


def save_text(
    path: Union[Path, str],
    content: str,
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    **kwargs,
) -> None:
    """Save a text file to the provided path."""
    path = Path(path)
    mkdir(Path(path).parent)
    path.write_text(content, encoding=encoding, errors=errors)


def load_yaml(
    path: Union[Path, str],
    *,
    default_value: Any | None = None,
    safe_loader: bool = False,
    **kwargs,
) -> Optional[Union[List[Any], Dict[str, Any]]]:
    """
    Loads YAML content from a file.

    Args:
        path (Union[Path, str]): The path to the file.
        default_value (Any | None): If something goes wrong, this value will be returned instead.
        safe_loader (bool): If True, it will use the safe_load instead.

    Returns:
        Optional[Union[List[Any], Dict[str, Any]]]: The loaded YAML data.
    """
    if not validate_path(path, expected_dir="file"):
        if default_value is None:
            raise FileNotFoundError(f"Invalid path '{path}'")
        return default_value
    loader = yaml.safe_load if safe_loader else yaml.unsafe_load
    try:
        return loader(Path(path).read_bytes())
    except Exception as e:
        print(f"YAML load error: {e}")
        print("----------------------")
        raise e


def save_yaml(
    path: Union[Path, str],
    content: Union[List[Any], Tuple[Any, Any], Dict[Any, Any]],
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    safe_dump: bool = False,
    **kwargs,
) -> None:
    """Saves a YAML file to the provided path.

    Args:
        path (Union[Path, str]): The path where the file will be saved.
        content (Union[List[Any], Tuple[Any, Any], Dict[Any, Any]]): The data that will be written into the file.
        encoding (str, optional): The encoding of the output. Default is 'utf-8'. Defaults to "utf-8".
        safe_dump (bool, optional): If True, it uses the safe_dump method instead. Defaults to False.
    """
    mkdir(Path(path).parent)
    save_func = yaml.safe_dump if safe_dump else yaml.dump
    try:
        with open(path, "w", encoding=encoding, errors=errors) as file:
            save_func(data=content, stream=file, encoding=encoding)
    except Exception as e:
        print(f"An exception occurred while saving {path}. Exception: {e}")
        traceback.print_exc()


def move(
    source: Union[str, Path],
    destination: Union[str, Path],
    *args,
    **kwargs,
):
    """
    Moves a file or directory from one location to another.

    Args:
        source_path (Union[str, Path]): The path of the file/directory to be moved.
        destination_path (Union[str, Path]): The new location for the file/directory.

    Raises:
        AssertionError: If the source path does not exist or is invalid
    """
    assert str(source).strip() and Path(source).exists(), "Source path does not exists!"
    source = Path(source)
    assert validate_path(source), "Source path does not exists!"
    mkdir(destination)
    shutil.move(str(source), str(destination))


def delete(
    files: Union[str, Path, Sequence[Union[str, Path]]],
    verbose: bool = False,
    *args,
    **kwargs,
):
    if is_string(files) and Path(files).exists():
        files = Path(files)
        if files.is_dir():
            shutil.rmtree(str(files))
        else:
            os.rmdir(str(files))
        if verbose:
            files = path_to_string(files)
            print(f"'{files}' deleted")
    elif is_array(files):
        [delete(path) for path in filter_list(flatten_list(files), (str, Path))]


__all__ = [
    "get_folders",
    "get_files",
    "validate_path",
    "mkdir",
    "load_json",
    "save_json",
    "load_text",
    "save_text",
    "load_yaml",
    "save_yaml",
    "move",
    "delete",
    "setup_path",
    "scan_dir",
]
