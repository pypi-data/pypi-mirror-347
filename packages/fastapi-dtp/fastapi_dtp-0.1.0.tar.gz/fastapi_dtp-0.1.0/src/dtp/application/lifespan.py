#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2025/5/9
# -------------------------------------------------------------------------------
from contextlib import asynccontextmanager

from fastapi import FastAPI



@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    yield