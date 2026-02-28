import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-core'))

from app.database.session import SessionLocal
from app.models.pipeline import Pipeline, FailureAnalysis, Fix, PipelineStatus

db = SessionLocal()

print('Recent failures for sample_file_ci_cd:')
failures = db.query(Pipeline).filter(
    Pipeline.repository.like('%sample_file_ci_cd%'),
    Pipeline.status == PipelineStatus.FAILURE
).order_by(Pipeline.id.desc()).limit(5).all()

for f in failures:
    print(f'\nPipeline ID: {f.id}')
    print(f'  Repo: {f.repository}')
    print(f'  Status: {f.status}')
    print(f'  Pipeline ID: {f.pipeline_id}')
    
    analysis = db.query(FailureAnalysis).filter_by(pipeline_id=f.id).first()
    if analysis:
        print(f'  Analysis ID: {analysis.id}')
        print(f'    Category: {analysis.error_category}')
        print(f'    Files: {analysis.affected_files}')
        
        fix = db.query(Fix).filter_by(analysis_id=analysis.id).first()
        if fix:
            print(f'  Fix ID: {fix.id}')
            print(f'    Status: {fix.status}')
            print(f'    Changes: {fix.changes}')

db.close()
