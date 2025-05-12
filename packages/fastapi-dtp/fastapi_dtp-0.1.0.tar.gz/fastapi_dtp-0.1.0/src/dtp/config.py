#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2025/5/9
# -------------------------------------------------------------------------------
from dynaconf import Dynaconf

from dtp.constants import ENVVAR_PREFIX, ENV_SWITCHER, SETTINGS_FILES, SECRETS_FILES


settings: Dynaconf = Dynaconf(
    environments=True,
    load_dotenv=True,
    envvar_prefix=ENVVAR_PREFIX,
    env_switcher=ENV_SWITCHER,
    settings_files=SETTINGS_FILES,
    secrets=SECRETS_FILES,
)
