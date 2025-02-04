import asyncio
import concurrent.futures

from temporalio.client import Client
from temporalio.worker import Worker

# Import the activity and workflow from our other files
from jobs.activities import embed_file
from jobs.workflows import EmbedFilesWorkflow
from utils.config import get_config


async def main():
    # Create client connected to server at the given address
    client = await Client.connect(get_config().temporal_host)

    # Run the worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue=get_config().temporal_queue,
            workflows=[EmbedFilesWorkflow],
            activities=[embed_file],
            activity_executor=activity_executor,
        )
        print(f"Worker running on queue: {get_config().temporal_queue}")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
