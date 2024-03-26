from fastapi import APIRouter


def create_route(prefix, tags):
    return APIRouter(
        prefix=f"/{prefix}",
        tags=[f"{tags}"],
    )
