# Changelog

All notable changes to the **Substrate** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.0.1] - 2026-03-18

### Added
- **Project Vision**: Defined the core roadmap for "Substrate" (Idea -> Flow -> Fundamental Mapping).
- **Mono-repo Structure**: Initialized `backend/` and `frontend/` directories.
- **Backend Engine (FastAPI)**: 
  - Implemented core API routes for Idea Vault.
  - Added simulated AI analysis endpoint for idea-to-flow mapping.
  - Integrated `seed` data system to inject domain expertise (8 Categories).
- **Database Architecture (SQLAlchemy)**:
  - Designed professional schemas: `Idea`, `Domain`, `DomainFlow`, `FlowModule`, and `CapabilityRecord`.
  - Switched to persistent storage using SQLite (`learnos.db`).
- **DevOps**: 
  - Configured `.gitignore` for Python environments and database security.
  - Established bilingual `README.md` with professional project board.

### Fixed
- **Git Authentication**: Resolved the 403 Forbidden error using project-level PAT (Personal Access Token) for multi-account isolation.

### Status
- **Phase**: Make it Work (MVP Building)
- **Next Step**: Implement Capability Interview logic and Quiz engine.

---

## [0.0.0] - 2026-03-18
- Initial project conception and repository creation.