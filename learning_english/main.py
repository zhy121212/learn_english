"""
分路由
"""

from fastapi import APIRouter
from learning_system import LearningSystem
from sql_connect.sqllite_connect import SessionDep
learning_system = APIRouter()

ls = LearningSystem()

@learning_system.get('/index')
def index():
    ls.menu()

@learning_system.get('/query/by-english')
def query_by_english(session: SessionDep, e_word: str):
    ls.query_word(session, e_word)

@learning_system.post('/save-to-db')
def save_to_db(session: SessionDep, e_word: str, e_translation: str):
    ls.save_to_db(session, e_word, e_translation)

