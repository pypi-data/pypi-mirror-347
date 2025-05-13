import uvicorn
import os
import logging.config
from autologging import logged
from fastapi import FastAPI, Request, HTTPException, Form
from adxp_sdk.serves.utils import (
    custom_openapi,
    load_environment,
)
from adxp_sdk.serves.graphapp_manager import set_up_graph_routes, create_graph_app


## Graph Server
@logged
def run_server(
    host: str,
    port: int,
    graph_path: str,
    env_file: str | None = None,
) -> None:
    """Run Graph as a API Server"""
    load_environment(env_file)
    app = create_graph_app(graph_path)

    uvicorn.run(app, host=host, port=port)


def get_server(
    graph_path: str,
    env_file: str | None = None,
) -> FastAPI:
    """Get API Server to Execute Graph"""
    if env_file:
        load_environment(env_file)
    app = create_graph_app(graph_path)
    return app


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=18080)
    