# REKRUTER AI - API DOCS

## Base URL: http://localhost:8000

## AUTH
POST /auth/register - Register company
POST /auth/login - Get JWT token
GET /auth/me - Current user

## JOBS
GET /api/jobs - List jobs
POST /api/jobs - Create job
GET /api/jobs/{id} - Job details
PUT /api/jobs/{id} - Update job
DELETE /api/jobs/{id} - Delete job
GET /api/jobs/{id}/stats - Statistics

## CANDIDATES
POST /api/jobs/{id}/upload - Upload CV
GET /api/jobs/{id}/candidates - List candidates
GET /api/candidates/{id} - Candidate details
PUT /api/candidates/{id} - Update status
POST /api/candidates/{id}/notes - Add note

Full docs: http://localhost:8000/docs
