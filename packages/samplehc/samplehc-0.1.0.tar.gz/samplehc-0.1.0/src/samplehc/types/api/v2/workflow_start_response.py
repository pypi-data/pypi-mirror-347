# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["WorkflowStartResponse"]


class WorkflowStartResponse(BaseModel):
    next_task_id: Optional[str] = FieldInfo(alias="nextTaskId", default=None)
    """
    The ID of the first task in the workflow run, or null if the workflow completes
    synchronously or has no starting task.
    """
