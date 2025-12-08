# core/utils.py
import uuid
import re

def normalize_str(val):
    """Normaliza string: lower, strip, espaços"""
    if val is None:
        return ""
    if not isinstance(val, str):
        val = str(val)
    val = val.strip().lower()
    val = re.sub(r"\s+", " ", val)
    return val

def normalize_uuid(val):
    """Garante que UUIDs estão no formato padrão, ou None se inválido"""
    if not val:
        return None
    if isinstance(val, uuid.UUID):
        return str(val)
    try:
        return str(uuid.UUID(str(val)))
    except ValueError:
        return None
