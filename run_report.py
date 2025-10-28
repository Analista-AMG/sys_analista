#!/usr/bin/env python3
import sys
import os
import json
import traceback
import importlib
import importlib.util

root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)

# Añadir rutas alternativas (con y sin tilde) si existen
possible_dirs = ["Campañas", "Campanas"]
for d in possible_dirs:
    p = os.path.join(root, d)
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

def load_module_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def import_report_functions():
    try:
        return importlib.import_module("report_functions")
    except Exception:
        rf_path = os.path.join(root, "report_functions.py")
        if os.path.exists(rf_path):
            return load_module_by_path("report_functions", rf_path)
        raise

def main():
    try:
        if len(sys.argv) < 2:
            raise ValueError("Uso: run_report.py FunctionName [arg1 arg2 ...]")

        func_name = sys.argv[1]
        args = sys.argv[2:]

        rf = import_report_functions()

        if not hasattr(rf, func_name):
            raise AttributeError(f"report_functions no tiene la función '{func_name}'")

        func = getattr(rf, func_name)

        result = func(*args)
        print(json.dumps({"ok": True, "result": result}, ensure_ascii=False))
        return 0

    except Exception as exc:
        tb = traceback.format_exc()
        print(json.dumps({"ok": False, "error": str(exc), "traceback": tb}, ensure_ascii=False))
        sys.stderr.write(tb)
        return 1

if __name__ == "__main__":
    sys.exit(main())    