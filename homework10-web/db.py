import typing as tp
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import Engine
from sqlalchemy.orm import Query, Session, sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///news.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


class BaseNote(BaseModel):
    text: str


class ShareWith(BaseModel):
    user: str


class Note(Base):  # type: ignore
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    author = Column(String)
    time_created = Column(String)
    shared_with = Column(String)


class User(Base):  # type:ignore
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String(130))


@tp.no_type_check
def get_session(engine: Engine) -> Session:
    SessionLocal.configure(bind=engine)
    return SessionLocal()


def execute_all_users(session: Session) -> tp.Dict[str, tp.Dict[str, str]]:
    users = session.query(User).all()
    json_users: tp.Dict[str, str] = {}
    for user in users:
        json_users[user.username] = {"username": user.username, "hashed_password": user.password}
    return json_users


def add_user(session: Session, username: str, password: str) -> None:
    new_user = User(username=username, password=password + "fakehash")
    session.add(new_user)
    session.commit()


def add_note(session: Session, note: BaseNote, username: str) -> None:
    new_note = Note(
        text=note.text,
        author=username,
        time_created=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    session.add(new_note)
    session.commit()


def update_note(session: Session, id: int, new_text: str) -> None:
    entry = session.query(Note).get(id)
    if entry is not None:
        entry.text = new_text
        session.commit()


def delete_note(session: Session, id: int, username: str) -> None:
    note = session.query(Note).filter_by(id=id, author=username).delete()
    session.commit()


def share_note(session: Session, id: int, username: str, share_with: str) -> None:
    note = session.query(Note).get(id)
    if note.author != username or note is None:
        return None
    note.shared_with = share_with
    session.commit()


def extract_note(
    session: Session, id: int, username: str
) -> tp.Optional[tp.Dict[int, tp.Dict[str, tp.Union[str, int]]]]:
    note = session.query(Note).filter_by(id=id, author=username).one()
    if note is not None:
        return {"text": note.text, "author": note.author, "created": note.time_created, "shared_with": note.shared_with}
    return None


def extract_all_notes(
    session: Session, username: str
) -> tp.Dict[int, tp.Dict[int, tp.Dict[str, tp.Union[str, int]]]]:
    created_entries = session.query(Note).filter(Note.author == username).all()
    shared_entries = session.query(Note).filter(Note.shared_with == username).all()

    json_entries: tp.Dict[int, tp.Dict[str, tp.Union[str, int]]] = {}
    for entry in set(created_entries + shared_entries):
        json_entries[entry.id] = {
            "text": entry.text,
            "author": entry.author,
            "created": entry.time_created,
            "shared_with": entry.shared_with
        }
    return json_entries  # type: ignore


Base.metadata.create_all(bind=engine)
