#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2025/5/10
# -------------------------------------------------------------------------------
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

ENVVAR_PREFIX = os.getenv("DTP_ENVVAR_PREFIX", "DTP")
ENV_SWITCHER = f"{ENVVAR_PREFIX}_ENV"

DEFAULT_SETTINGS_FILE = BASE_DIR / "settings.toml"

# Settings files to be loaded by Dynaconf
SETTINGS_FILES = [DEFAULT_SETTINGS_FILE, "settings.toml", "settings.yaml", "settings.json"]
SECRETS_FILES = [".secrets.toml", ".secrets.yaml", ".secrets.json"]
