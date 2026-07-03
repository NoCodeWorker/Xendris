# Phygn v3.6 — Source Availability & Manual Download Task Protocol

## 0. Purpose

This document defines how missing local source files become actionable manual download tasks.

v3.6 must not silently pass over missing files.

---

## 1. Availability statuses

```txt
SOURCE_FILE_AVAILABLE_LOCAL
SOURCE_FILE_MISSING_LOCAL
SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD
SOURCE_FILE_PATH_REGISTERED_BUT_NOT_FOUND
SOURCE_FILE_AVAILABLE_BUT_UNHASHED
SOURCE_FILE_AVAILABLE_AND_HASHED
```

---

## 2. Manual download task schema

```python
class ManualSourceDownloadTask(BaseModel):
    task_id: str
    source_id: str
    title: str
    preferred_filename: str
    target_path: str
    known_identifiers: dict[str, str | None]
    priority: int
    reason: str
    status: str
```

---

## 3. Task statuses

```txt
DOWNLOAD_TASK_CREATED
DOWNLOAD_TASK_COMPLETED
DOWNLOAD_TASK_BLOCKED
DOWNLOAD_TASK_NOT_NEEDED
```

---

## 4. Priority order

Create missing-file tasks in this order:

```txt
1. Hornberger 2003
2. Hackermüller 2004
3. Nimmrichter 2011
4. Schrinski 2020
5. Pedernales 2019
```

---

## 5. Download task output

Create:

```txt
data/real_sources/manual_download_tasks_v3_6.json
```

Report:

```txt
reports/local_source_text/phi_gradient_manual_download_tasks_v3_6.md
```

---

## 6. Next extraction readiness

A source is ready for v3.7 exact extraction only if:

```txt
exists = true
sha256 is not null
local_path is valid
file_type is supported
```

If any priority source is missing, v3.7 may still run partial extraction, but reports must classify:

```txt
PARTIAL_LOCAL_SOURCE_TEXT_READY
```

---

## 7. Final principle

```txt
A missing source is not a dead end.
It is a task with a filename.
```
