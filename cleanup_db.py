import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-core'))

from app.database.session import SessionLocal
from app.models.pipeline import Pipeline, FailureAnalysis, Fix

db = SessionLocal()

# Delete all sample_file_ci_cd related data
pipelines = db.query(Pipeline).filter(Pipeline.repository.like('%sample_file_ci_cd%')).all()

for p in pipelines:
    # Delete fixes
    analyses = db.query(FailureAnalysis).filter_by(pipeline_id=p.id).all()
    for a in analyses:
        db.query(Fix).filter_by(analysis_id=a.id).delete()
    
    # Delete analyses
    db.query(FailureAnalysis).filter_by(pipeline_id=p.id).delete()

# Delete pipelines
db.query(Pipeline).filter(Pipeline.repository.like('%sample_file_ci_cd%')).delete()

db.commit()
print('Deleted all sample_file_ci_cd pipelines, analyses, and fixes')
db.close()
