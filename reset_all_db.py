import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-core'))

from app.database.session import SessionLocal
from app.models.pipeline import Pipeline, FailureAnalysis, Fix

db = SessionLocal()

# Delete all data
print("Deleting all data from database...")

# Delete all fixes
fix_count = db.query(Fix).delete()
print(f"Deleted {fix_count} fixes")

# Delete all analyses
analysis_count = db.query(FailureAnalysis).delete()
print(f"Deleted {analysis_count} analyses")

# Delete all pipelines
pipeline_count = db.query(Pipeline).delete()
print(f"Deleted {pipeline_count} pipelines")

db.commit()
print("\nDatabase reset complete!")
db.close()
