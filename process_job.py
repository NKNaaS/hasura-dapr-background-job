from cloudevents.sdk.event import v1
from dapr.ext.grpc import App
import logging
from pydantic import BaseModel
import requests
from time import sleep


SET_STATUS_IN_PROGRESS_QUERY = """
mutation SetStatusInProgress($id: bigint!) {
  update_job(where: {id: {_eq: $id}, status: {_eq: "Waiting"}}, _set: {status: "InProgress"}) {
    affected_rows
  }
}
"""


class AlreadyStartedError(Exception):
    pass


def set_status_in_progress(id_: int):
    resp = requests.post(
        "http://localhost:3602/v1.0/invoke/hasura/method/v1/graphql",
        json={
            "query": SET_STATUS_IN_PROGRESS_QUERY,
            "variables": {"id": id_},
            "operationName": "SetStatusInProgress",
        },
    ).json()

    if resp["data"]["update_job"]["affected_rows"] == 0:
        raise AlreadyStartedError


SET_STATUS_DONE_QUERY = """
mutation SetStatusDone($id: bigint!) {
  update_job(where: {id: {_eq: $id}}, _set: {status: "Done"}) {
    affected_rows
  }
}
"""


def set_status_done(id_: str):
    requests.post(
        "http://localhost:3602/v1.0/invoke/hasura/method/v1/graphql",
        json={
            "query": SET_STATUS_DONE_QUERY,
            "variables": {"id": id_},
            "operationName": "SetStatusDone",
        },
    )


class Req(BaseModel):
    id: int
    sleep_num: int


app = App()
logging.basicConfig(level=logging.INFO)

@app.subscribe(pubsub_name="jobpubsub", topic="job")
def process_job(event: v1.Event) -> None:
    req = Req.parse_raw(event.Data())
    logging.info("Job processor received: " + str(req))

    try:
        set_status_in_progress(req.id)
    except AlreadyStartedError:
        logging.info("Job already started: " + str(req))
        return

    sleep(req.sleep_num)

    set_status_done(req.id)
    logging.info("Job processor finished: " + str(req))


app.run(6002)
