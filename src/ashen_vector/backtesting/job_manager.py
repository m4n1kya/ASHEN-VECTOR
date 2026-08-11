"""
Background execution manager for CPU-heavy ML backtests.
Provides QUEUED -> RUNNING -> COMPLETED state machine.
"""

import uuid
import time
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

class JobManager:
    """Manages background backtest jobs using a thread pool."""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.jobs: Dict[str, Dict[str, Any]] = {}
        
    def submit_job(self, func, *args, **kwargs) -> str:
        """Submit a job and return its ID."""
        job_id = str(uuid.uuid4())
        
        self.jobs[job_id] = {
            "id": job_id,
            "status": "QUEUED",
            "submitted_at": time.time(),
            "result": None,
            "error": None
        }
        
        # Submit to pool
        self.executor.submit(self._run_job_wrapper, job_id, func, *args, **kwargs)
        return job_id
        
    def _run_job_wrapper(self, job_id: str, func, *args, **kwargs):
        """Wrapper to update status upon completion or failure."""
        self.jobs[job_id]["status"] = "RUNNING"
        self.jobs[job_id]["started_at"] = time.time()
        
        try:
            result = func(*args, **kwargs)
            self.jobs[job_id]["status"] = "COMPLETED"
            self.jobs[job_id]["result"] = result
        except Exception as e:
            import traceback
            self.jobs[job_id]["status"] = "FAILED"
            self.jobs[job_id]["error"] = str(e)
            self.jobs[job_id]["traceback"] = traceback.format_exc()
        finally:
            self.jobs[job_id]["completed_at"] = time.time()
            
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve job status and metadata."""
        return self.jobs.get(job_id)
        
    def get_job_result(self, job_id: str) -> Optional[Any]:
        """Retrieve final job result if completed."""
        job = self.jobs.get(job_id)
        if job and job["status"] == "COMPLETED":
            return job["result"]
        return None

# Global instance for FastAPI dependency injection
job_manager = JobManager()
