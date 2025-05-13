# API

## V1

Types:

```python
from samplehc.types.api import V1CreateAuditLogResponse, V1CreateSqlResponse
```

Methods:

- <code title="post /api/v1/audit-logs">client.api.v1.<a href="./src/samplehc/resources/api/v1.py">create_audit_log</a>(\*\*<a href="src/samplehc/types/api/v1_create_audit_log_params.py">params</a>) -> <a href="./src/samplehc/types/api/v1_create_audit_log_response.py">V1CreateAuditLogResponse</a></code>
- <code title="post /api/v1/sql">client.api.v1.<a href="./src/samplehc/resources/api/v1.py">create_sql</a>(\*\*<a href="src/samplehc/types/api/v1_create_sql_params.py">params</a>) -> <a href="./src/samplehc/types/api/v1_create_sql_response.py">V1CreateSqlResponse</a></code>

## V2

Methods:

- <code title="get /api/v2/async-result/{asyncResultId}">client.api.v2.<a href="./src/samplehc/resources/api/v2/v2.py">get_async_result</a>(async_result_id) -> None</code>

### WorkflowRun

Types:

```python
from samplehc.types.api.v2 import WorkflowRunRetrieveStartDataResponse
```

Methods:

- <code title="post /api/v2/workflow-run/resume-when-complete">client.api.v2.workflow_run.<a href="./src/samplehc/resources/api/v2/workflow_run/workflow_run.py">resume_when_complete</a>(\*\*<a href="src/samplehc/types/api/v2/workflow_run_resume_when_complete_params.py">params</a>) -> None</code>
- <code title="get /api/v2/workflow-run/start-data">client.api.v2.workflow_run.<a href="./src/samplehc/resources/api/v2/workflow_run/workflow_run.py">retrieve_start_data</a>() -> <a href="./src/samplehc/types/api/v2/workflow_run_retrieve_start_data_response.py">WorkflowRunRetrieveStartDataResponse</a></code>

#### Step

Methods:

- <code title="get /api/v2/workflow-run/step/{stepId}/output">client.api.v2.workflow_run.step.<a href="./src/samplehc/resources/api/v2/workflow_run/step.py">output</a>(step_id) -> None</code>

### Task

Types:

```python
from samplehc.types.api.v2 import TaskCompleteResponse, TaskGetSuspendedPayloadResponse
```

Methods:

- <code title="post /api/v2/task/{taskId}/complete">client.api.v2.task.<a href="./src/samplehc/resources/api/v2/task.py">complete</a>(task_id, \*\*<a href="src/samplehc/types/api/v2/task_complete_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/task_complete_response.py">TaskCompleteResponse</a></code>
- <code title="get /api/v2/task/{taskId}/suspended-payload">client.api.v2.task.<a href="./src/samplehc/resources/api/v2/task.py">get_suspended_payload</a>(task_id) -> <a href="./src/samplehc/types/api/v2/task_get_suspended_payload_response.py">TaskGetSuspendedPayloadResponse</a></code>

### Workflow

Types:

```python
from samplehc.types.api.v2 import WorkflowStartResponse
```

Methods:

- <code title="post /api/v2/workflow/{workflowId}/deploy">client.api.v2.workflow.<a href="./src/samplehc/resources/api/v2/workflow.py">deploy</a>(workflow_id) -> None</code>
- <code title="post /api/v2/workflow/{workflowSlug}/start">client.api.v2.workflow.<a href="./src/samplehc/resources/api/v2/workflow.py">start</a>(workflow_slug, \*\*<a href="src/samplehc/types/api/v2/workflow_start_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/workflow_start_response.py">WorkflowStartResponse</a></code>

### Document

Types:

```python
from samplehc.types.api.v2 import (
    DocumentRetrieveResponse,
    DocumentClassifyResponse,
    DocumentCreateFromSplitsResponse,
    DocumentExtractResponse,
    DocumentExtractionResponse,
    DocumentGenerateResponse,
    DocumentGenerateCsvResponse,
    DocumentGetCsvContentResponse,
    DocumentGetMetadataResponse,
    DocumentGetPresignedUploadURLResponse,
    DocumentSplitResponse,
)
```

Methods:

- <code title="get /api/v2/document/{documentId}">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">retrieve</a>(document_id) -> <a href="./src/samplehc/types/api/v2/document_retrieve_response.py">DocumentRetrieveResponse</a></code>
- <code title="post /api/v2/document/classify">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">classify</a>(\*\*<a href="src/samplehc/types/api/v2/document_classify_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_classify_response.py">DocumentClassifyResponse</a></code>
- <code title="post /api/v2/document/create-from-splits">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">create_from_splits</a>(\*\*<a href="src/samplehc/types/api/v2/document_create_from_splits_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_create_from_splits_response.py">DocumentCreateFromSplitsResponse</a></code>
- <code title="post /api/v2/document/extract">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">extract</a>(\*\*<a href="src/samplehc/types/api/v2/document_extract_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_extract_response.py">DocumentExtractResponse</a></code>
- <code title="post /api/v2/document/extraction">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">extraction</a>(\*\*<a href="src/samplehc/types/api/v2/document_extraction_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_extraction_response.py">DocumentExtractionResponse</a></code>
- <code title="post /api/v2/document/generate">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">generate</a>(\*\*<a href="src/samplehc/types/api/v2/document_generate_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_generate_response.py">DocumentGenerateResponse</a></code>
- <code title="post /api/v2/document/generate-csv">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">generate_csv</a>(\*\*<a href="src/samplehc/types/api/v2/document_generate_csv_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_generate_csv_response.py">DocumentGenerateCsvResponse</a></code>
- <code title="get /api/v2/document/{documentId}/csv-content">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">get_csv_content</a>(document_id) -> <a href="./src/samplehc/types/api/v2/document_get_csv_content_response.py">DocumentGetCsvContentResponse</a></code>
- <code title="get /api/v2/document/{documentId}/metadata">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">get_metadata</a>(document_id) -> <a href="./src/samplehc/types/api/v2/document_get_metadata_response.py">DocumentGetMetadataResponse</a></code>
- <code title="post /api/v2/document/presigned-upload-url">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">get_presigned_upload_url</a>(\*\*<a href="src/samplehc/types/api/v2/document_get_presigned_upload_url_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_get_presigned_upload_url_response.py">DocumentGetPresignedUploadURLResponse</a></code>
- <code title="post /api/v2/document/search">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">search</a>(\*\*<a href="src/samplehc/types/api/v2/document_search_params.py">params</a>) -> None</code>
- <code title="post /api/v2/document/split">client.api.v2.document.<a href="./src/samplehc/resources/api/v2/document/document.py">split</a>(\*\*<a href="src/samplehc/types/api/v2/document_split_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document_split_response.py">DocumentSplitResponse</a></code>

#### Legacy

Types:

```python
from samplehc.types.api.v2.document import LegacyExtractResponse
```

Methods:

- <code title="post /api/v2/document/legacy/extract">client.api.v2.document.legacy.<a href="./src/samplehc/resources/api/v2/document/legacy.py">extract</a>(\*\*<a href="src/samplehc/types/api/v2/document/legacy_extract_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/document/legacy_extract_response.py">LegacyExtractResponse</a></code>
- <code title="post /api/v2/document/legacy/reason">client.api.v2.document.legacy.<a href="./src/samplehc/resources/api/v2/document/legacy.py">reason</a>(\*\*<a href="src/samplehc/types/api/v2/document/legacy_reason_params.py">params</a>) -> None</code>

### Communication

Types:

```python
from samplehc.types.api.v2 import CommunicationSendEmailResponse
```

Methods:

- <code title="post /api/v2/communication/send-email">client.api.v2.communication.<a href="./src/samplehc/resources/api/v2/communication.py">send_email</a>(\*\*<a href="src/samplehc/types/api/v2/communication_send_email_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/communication_send_email_response.py">object</a></code>

### Claim

Types:

```python
from samplehc.types.api.v2 import ClaimCoordinateBenefitsResponse, ClaimSubmitResponse
```

Methods:

- <code title="post /api/v2/claim/coordination-of-benefits">client.api.v2.claim.<a href="./src/samplehc/resources/api/v2/claim/claim.py">coordinate_benefits</a>(\*\*<a href="src/samplehc/types/api/v2/claim_coordinate_benefits_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/claim_coordinate_benefits_response.py">object</a></code>
- <code title="post /api/v2/claim/submission">client.api.v2.claim.<a href="./src/samplehc/resources/api/v2/claim/claim.py">submit</a>(\*\*<a href="src/samplehc/types/api/v2/claim_submit_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/claim_submit_response.py">ClaimSubmitResponse</a></code>

#### Eligibility

Types:

```python
from samplehc.types.api.v2.claim import EligibilityCheckResponse
```

Methods:

- <code title="post /api/v2/claim/eligibility/check">client.api.v2.claim.eligibility.<a href="./src/samplehc/resources/api/v2/claim/eligibility.py">check</a>(\*\*<a href="src/samplehc/types/api/v2/claim/eligibility_check_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/claim/eligibility_check_response.py">EligibilityCheckResponse</a></code>

### Ledger

Types:

```python
from samplehc.types.api.v2 import LedgerCreateOrderResponse
```

Methods:

- <code title="post /api/v2/ledger/new-order">client.api.v2.ledger.<a href="./src/samplehc/resources/api/v2/ledger.py">create_order</a>(\*\*<a href="src/samplehc/types/api/v2/ledger_create_order_params.py">params</a>) -> <a href="./src/samplehc/types/api/v2/ledger_create_order_response.py">object</a></code>
