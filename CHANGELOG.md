# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2025-10-28

### 🎉 Added
- Initial release of AutoEdu with support for UDISE Student Import Module
- Core automation pipeline for student data ingestion and status reporting
- Basic fallback logic for PEN retrieval and import validation

---

### 🐞 Known Issues
- 🐛 **#51**: UI stuck during student import causes buggy execution and blocks workflow
- 🐛 **#70**: UDISE Import ignores class mismatch for active students in the same school
- 🐛 **#74**: ER1028 (PEN belongs to other state) not handled properly in UDISE Student Import

---

### 🚀 Feature Requests
- 🚀 **#20**: Add serial number and timestamp to report entries
- 🚀 **#57**: Student Aadhaar availability check in UDISE module
- 📊 **#67**: Add summary of remarks to status report sheet

---

### 🔄 Refactor Proposals
- 🔄 **#46**: Dictionary-driven conditional imports for `MODULE` and `TASK`
- 🔄 **#53**: Resilient execution strategy for AutoEdu via error detection and recovery

---

### 🚨 Exception Handling Enhancements
- 🚨 **#52**: Custom exceptions for UI hang and task failures

---

### 📌 Notes
This release lays the foundation for AutoEdu’s modular automation framework. While core functionality is stable, several edge cases and enhancements have been identified for future milestones. See [Milestone: AutoEdu v1.1.1](https://github.com/AshishNamdev/AutoEdu/milestone/7) for targeted fixes and onboarding improvements.


### Notes
- Initial release of AutoEdu (Automation in Education) project.


