from magicpush import app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), pool_size=15, max_overflow=0,
                       isolation_level="AUTOCOMMIT")

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
