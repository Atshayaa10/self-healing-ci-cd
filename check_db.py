import sys
import os

# Change to agent-core directory to match backend's working directory
os.chdir(os.path.join(os.path.dirname(__file__), 'agent-core'))
sys.path.insert(0, os.getcwd())

from app.database.session import SessionLocal
from app.models.pipeline import Pipeline

db = SessionLocal()

count = db.query(Pipeline).count()
print(f'Total pipelines in DB: {count}')

pipelines = db.query(Pipeline).filter(Pipeline.repository.like('%sample_file_ci_cd%')).all()
print(f'\nsample_file_ci_cd pipelines: {len(pipelines)}')

for p in pipelines:
    print(f'  ID: {p.id}, Pipeline ID: {p.pipeline_id}, Status: {p.status}')

db.close()
