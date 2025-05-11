def value_to_bool(value: str | bool | int | None) -> bool:
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.

    Also handles the case the value is a bool or None

    Raises ValueError if 'val' is anything else.
    """
    if value is None or value == "":
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        value = str(value)

    value = value.lower()
    if value in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (value,))
