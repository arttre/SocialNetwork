from fastapi import FastAPI

from app.routers import users, posts, analytics

app = FastAPI(
    title="Social Network",
    description="StarNavi python developer test task",
    version="1.0.0"
)


app.include_router(
    users.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


app.include_router(
    posts.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


app.include_router(
    analytics.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


@app.get('/')
def health_check():
    return {'status': 'OK'}
