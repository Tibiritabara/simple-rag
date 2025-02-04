"""
Set of temporal workflows to orchestrate embedding activities.
"""

from datetime import timedelta

from temporalio import workflow

# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from temporalio.common import RetryPolicy

    from jobs.activities import embed_file
    from utils.types import EmbeddingFileWorkflowRequest, EmbeddingResponse


@workflow.defn
class EmbedFilesWorkflow:
    """
    Workflow to embed files.
    """

    @workflow.run
    async def run(self, request: EmbeddingFileWorkflowRequest) -> EmbeddingResponse:
        """
        Run the workflow to embed files.

        Args:
            request (EmbeddingFileWorkflowRequest): The request to embed files.

        Returns:
            (EmbeddingResponse): The response from the workflow.
        """
        result = await workflow.execute_activity(
            embed_file,
            request,
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                maximum_attempts=10,
            ),
        )
        if isinstance(result, EmbeddingResponse):
            return result
        return EmbeddingResponse(
            status="error",
            message="Failed to embed file",
        )
