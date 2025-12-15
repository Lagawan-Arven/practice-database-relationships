from api.database.database import mysession

def get_session():
    session = mysession()
    try:
        yield session
    finally:
        session.close()