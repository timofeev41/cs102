from fastapi import Depends, FastAPI, Response
from fastapi.security import OAuth2PasswordRequestForm

from db import (
    BaseNote,
    ShareWith,
    add_note,
    add_user,
    delete_note,
    engine,
    execute_all_users,
    extract_all_notes,
    extract_note,
    get_session,
    update_note,
    share_note,
)
from security import User, UserInDB, get_current_active_user, get_current_user, oauth2_scheme

app = FastAPI()
db_session = get_session(engine)


@app.get("/")
def read_root():
    return {"status": "working"}


@app.get("/users")
async def read_users():
    users = execute_all_users(db_session)
    return users


@app.get("/notes")
async def read_notes(token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    notes = extract_all_notes(db_session, user.username)
    return notes


@app.get("/notes/{id}")
async def read_concrete_note(id: int, token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    note = extract_note(db_session, id, user.username)
    if note is None:
        return Response(content="note not found", status_code=404)
    return note


@app.delete("/notes/{id}")
async def delete_note_from_list(id: int, token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    try:
        delete_note(db_session, id, user.username)
        return Response("note was deleted")
    except Exception:
        return Response("note not found", status_code=404)


@app.patch("/notes/{id}")
async def edit_concrete_note(id: int, item: BaseNote):
    update_note(db_session, id, item.text)
    return {"status": "edited"}


@app.post("/notes")
async def add_notes(note: BaseNote, token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    add_note(db_session, note, user.username)
    return {"status": True}


@app.post("/notes/{id}/share")
async def share_concrete_note(id: int, share: ShareWith, token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    share_note(db_session, id, user.username, share.user)
    return {"status": "shared ok"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = execute_all_users(db_session)
    print(users)
    user_dict = users.get(form_data.username)
    if not user_dict:
        return {"error": "incorrect pass or login"}
    user = UserInDB(**user_dict)
    hashed_password = form_data.password + "fakehash"
    if not hashed_password == user.hashed_password:
        return {"error": "incorrect pass or login"}

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/add")
async def add_users(item: UserInDB):
    """это чисто для теста чтоб юзера добавить"""
    add_user(db_session, item.username, item.hashed_password)
    return {"status": "added"}
