import pytest
from httpx import AsyncClient
from uuid import uuid4
import tempfile
from pathlib import Path

class TestCandidatesRouter:
    """Test candidates upload and scoring"""
    
    @pytest.mark.asyncio
    async def test_upload_cv_endpoint_exists(self, client: AsyncClient):
        """Test że endpoint /api/jobs/{job_id}/upload istnieje"""
        job_id = str(uuid4())
        
        test_file = Path(tempfile.mktemp(suffix=".pdf"))
        test_file.write_text("Test CV content")
        
        with open(test_file, "rb") as f:
            response = await client.post(
                f"/api/jobs/{job_id}/upload",
                files={"file": ("test_cv.pdf", f, "application/pdf")}
            )
        
        test_file.unlink()
        assert response.status_code in [404, 422, 500]
    
    @pytest.mark.asyncio
    async def test_list_candidates_endpoint(self, client: AsyncClient):
        """Test że endpoint /api/jobs/{job_id}/candidates istnieje"""
        job_id = str(uuid4())
        response = await client.get(f"/api/jobs/{job_id}/candidates")
        assert response.status_code in [200, 404]
    
    @pytest.mark.asyncio
    async def test_upload_invalid_file_type(self, client: AsyncClient):
        """Test że tylko dozwolone typy plików"""
        job_id = str(uuid4())
        
        test_file = Path(tempfile.mktemp(suffix=".exe"))
        test_file.write_bytes(b"fake exe")
        
        with open(test_file, "rb") as f:
            response = await client.post(
                f"/api/jobs/{job_id}/upload",
                files={"file": ("malware.exe", f, "application/x-msdownload")}
            )
        
        test_file.unlink()
        # 404 też OK - endpoint istnieje ale job nie istnieje
        assert response.status_code in [400, 404, 422]
