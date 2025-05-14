class Status:
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    RETRYING = "RETRYING"


class Queue:
    CORE = "core"


class Task:
    SEND_VERSION = "send_version_to_core"
