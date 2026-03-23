from app.db.database import Base, engine
from app.models.content import Content
from app.models.analysis import AnalysisResult
from app.models.review import Review

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
