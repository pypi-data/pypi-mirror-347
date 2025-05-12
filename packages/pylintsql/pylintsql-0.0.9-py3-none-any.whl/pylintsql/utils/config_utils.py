from sqlfluff.core.config import FluffConfig
import toml
from pathlib import Path
import pathspec
import os
import logging

logger = logging.getLogger(__name__)

def get_sqlfluff_config(
    search_path: str = None, config_path: str = None, rules: list[str] = None, exclude_rules: list[str] = None
):
    """
    Load the SQLFluff configuration by using a specific config file if provided,
    or searching for the last valid config file in order.

    Args:
        search_path (str): Path to start searching for config files. Defaults to current directory.
        config_path (str): Path to a specific configuration file. If provided, it will be used directly.

    Returns:
        FluffConfig: The instantiated SQLFluff configuration object.
    """

    def _ensure_list_of_str(value):
        """
        Convert a comma‐separated string or a list of strings into a List[str].
        """
        if value is None:
            return []
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            return list(value)
        raise TypeError(f"Expected str or list[str], got {type(value)}")
    
    # 1) Prepare search order for a SQLFluff config file
    config_files = ["setup.cfg", "tox.ini", "pep8.ini", ".sqlfluff", "pyproject.toml"]
    # 2) Find the actual file to read for merging
    cfg_path = None
    if config_path and os.path.exists(config_path):
        cfg_path = config_path
    else:
        base = search_path or os.getcwd()
        for fn in config_files:
            candidate = os.path.join(base, fn)
            if os.path.exists(candidate):
                cfg_path = candidate
                break

    # 3) Read file‐based rules/excludes (for merging only)
    file_rules, file_excludes = [], []
    if cfg_path and cfg_path.endswith(".toml"):
        try:
            data = toml.load(cfg_path)
            core = data.get("tool", {}).get("sqlfluff", {}).get("core", {})
            file_rules    = core.get("rules", [])
            file_excludes = core.get("exclude_rules", [])
        except Exception:
            pass

    # 4) Normalize & merge CLI + file values
    cli_rules    = _ensure_list_of_str(rules)
    cli_excludes = _ensure_list_of_str(exclude_rules)
    file_rules   = _ensure_list_of_str(file_rules)
    file_excludes= _ensure_list_of_str(file_excludes)

    overrides = {}
    merged_rules    = sorted(set(file_rules)    | set(cli_rules))
    merged_excludes = sorted(set(file_excludes) | set(cli_excludes))
    if merged_rules:
        overrides["rules"] = merged_rules
    if merged_excludes:
        overrides["exclude_rules"] = merged_excludes

    # If a specific config file is provided, use it directly
    if config_path:
        if os.path.exists(config_path):
            try:
                config = FluffConfig.from_path(config_path, overrides=overrides)
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration from {config_path}: {e}")
                raise
        else:
            raise FileNotFoundError(f"Specified configuration file not found: {config_path}")
    else:
        # Define the order of config files to search for
        config_files = ["setup.cfg", "tox.ini", "pep8.ini", ".sqlfluff", "pyproject.toml"]

        # Start searching from the provided path or current directory
        search_path = os.getcwd()

        config = None

        # Iterate through the config files in order, overwriting with the last valid one
        for config_file in config_files:
            config_path = os.path.join(search_path, config_file)
            if os.path.exists(config_path):
                try:
                    # Load the configuration from the current file
                    config = FluffConfig.from_path(config_path, overrides=overrides)
                    logger.info(f"Loaded configuration from {config_path}")
                except Exception as e:
                    logger.warning(f"Could not load {config_file}. Error: {e}")

        # If no config file is found, fallback to default configuration
        if not config:
            logger.warning("No configuration file found. Using default config.")
            config = FluffConfig.from_kwargs(
                dialect="ansi"
            )

    return config

def find_project_root(start_path="."):
    """Find the project root by looking for pyproject.toml"""
    path = Path(start_path).resolve()
    while path != path.parent:
        if (path / "pyproject.toml").exists():
            return path
        path = path.parent
    return None

def get_excluded_paths(target_path=".", config_path=None):
    """
    Get gitignore-style pattern matcher from pyproject.toml or specified config file
    
    Args:
        target_path (str): Path to start searching for pyproject.toml
        config_path (str): Path to a specific configuration file
    
    Returns:
        pathspec.PathSpec: Matcher for excluded paths
    """
    # First try to use the specified config file if provided
    if config_path and os.path.exists(config_path):
        try:
            # Check if config_path is a pyproject.toml file
            if config_path.endswith('pyproject.toml'):
                data = toml.load(config_path)
                patterns = data.get("tool", {}).get("pylintsql", {}).get("exclude", [])
                if patterns:
                    logger.info(f"Using exclusion patterns from specified config: {config_path}")
                    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
            else:
                # For non-pyproject.toml files, check if they have the relevant section
                try:
                    data = toml.load(config_path)
                    patterns = data.get("tool", {}).get("pylintsql", {}).get("exclude", [])
                    if patterns:
                        logger.info(f"Using exclusion patterns from specified config: {config_path}")
                        return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
                except toml.TomlDecodeError:
                    # Specific error for TOML parsing failures
                    logger.debug(f"File {config_path} is not a valid TOML file")
                except (AttributeError, KeyError, TypeError) as e:
                    # Handle issues with the TOML structure not being as expected
                    logger.debug(f"Config file {config_path} does not contain valid exclusion patterns: {e}")
        except Exception as e:
            logger.warning(f"Error loading exclusion patterns from {config_path}: {e}")
    
    # If no patterns found in config_path or it wasn't specified, fall back to pyproject.toml
    # First check current working directory (where script is run)
    project_root = find_project_root(os.getcwd())
    
    # If not found, try from target_path as fallback
    if not project_root:
        project_root = find_project_root(target_path)
        
    if not project_root:
        logger.warning("Could not find pyproject.toml. No exclusions will be applied.")
        return pathspec.PathSpec([])
    
    pyproject_file = project_root / "pyproject.toml"
    logger.info(f"Using exclusion patterns from: {pyproject_file}")
    
    try:
        data = toml.load(pyproject_file)
        patterns = data.get("tool", {}).get("pylintsql", {}).get("exclude", [])
        
        # Create a pathspec with gitignore patterns
        return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    except Exception as e:
        logger.warning(f"Error loading exclusion patterns: {e}")
        return pathspec.PathSpec([])