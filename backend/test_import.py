import sys
import traceback

try:
    from app.db.database import Base, engine
    from app.models.content import Content
    from app.models.analysis import AnalysisResult
    from app.models.review import Review
except Exception as e:
    with open("error_dump.txt", "w") as f:
        traceback.print_exc(file=f)
    print("Error dumped to file")
