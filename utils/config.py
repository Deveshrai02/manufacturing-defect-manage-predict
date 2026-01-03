import os

def _load_yaml():
    try:
        import yaml
    except Exception as e:
        raise RuntimeError("PyYAML is required to load configuration. Install with: pip install pyyaml")

    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "rules.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)


_CONFIG = None

def get_config():
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _load_yaml() or {}
    return _CONFIG


def get_validations():
    cfg = get_config()
    return cfg.get("validations", {})


def get_columns():
    cfg = get_config()
    return cfg.get("columns", {})
