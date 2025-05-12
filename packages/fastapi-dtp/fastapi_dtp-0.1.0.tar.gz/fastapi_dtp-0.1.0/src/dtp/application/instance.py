#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2025/5/9
# -------------------------------------------------------------------------------
from fastapi import FastAPI, Request

from dtp.application.lifespan import lifespan_manager


def create_app() -> FastAPI:
    """
    Create a FastAPI application instance.
    """
    app = FastAPI(
        title="DTP",
        description="A Data Transfer Protocol for data transfer.",
        lifespan=lifespan_manager,
    )

    @app.get("/")
    async def root(request: Request):
        return {
            "message": "Welcome to DTP!",
            "settings": request.state.settings.as_dict(),
        }

    return app