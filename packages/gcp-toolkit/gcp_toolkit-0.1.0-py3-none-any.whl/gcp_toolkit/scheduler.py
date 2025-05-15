from google.cloud import scheduler_v1
from google.protobuf import duration_pb2


def create_scheduler_job(
    project_id, location_id, job_id, topic_name, schedule="* * * * *", message="Hello"
):
    """Creates a Cloud Scheduler job to publish a message to a Pub/Sub topic."""
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    topic_path = f"projects/{project_id}/topics/{topic_name}"

    job = {
        "name": f"{parent}/jobs/{job_id}",
        "pubsub_target": {"topic_name": topic_path, "data": message.encode("utf-8")},
        "schedule": schedule,
        "time_zone": "UTC",
    }

    return client.create_job(request={"parent": parent, "job": job})
