#!python
"""Print a log of completed Todoist tasks for one day.

:author: Shay Hill
:created: 2023-01-20
"""


import itertools
import json

import requests
from pydantic import BaseModel
from requests.structures import CaseInsensitiveDict

from todoist_log_exe.user_entry import get_api_args


def _new_headers(api_token: str) -> CaseInsensitiveDict[str]:
    """Create a new headers dictionary for requests to the Todoist sync API.

    :param api_token: The API token for the Todoist account.
    :return: A dictionary of headers for requests to the Todoist sync API.
    """
    headers: CaseInsensitiveDict[str] = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + api_token
    return headers


class _Note(BaseModel):
    content: str


class _Task(BaseModel):
    completed_at: str
    project_id: str | None
    section_id: str | None
    content: str
    notes: list[_Note]


class _Project(BaseModel):
    name: str


class _Section(BaseModel):
    name: str


class _Response(BaseModel):
    projects: dict[str, _Project]
    sections: dict[str, _Section]
    items: list[_Task]

    def get_project(self, project_id: str | None) -> str:
        """Get the name of the project with the given ID.

        :param project_id: The ID of the project.
        :return: The name of the project.
        """
        if project_id is None:
            return ""
        return self.projects[project_id].name

    def get_section(self, section_id: str | None) -> str:
        """Get the name of the section with the given ID.

        :param section_id: The ID of the section.
        :return: The name of the section.
        """
        if section_id is None:
            return ""
        return self.sections[section_id].name


def _condense_notes(notes: list[_Note]) -> str:
    """Create a string from note contents.

    :param notes: A list of notes from the Todoist API.
    :return: A string of note contents.
    """
    contents = [note.content for note in notes]
    contents = [f'"{x}"' for x in contents if x]
    return ", ".join(contents)


def _filter_task_data(resp_json: _Response, task: _Task) -> list[str]:
    """Create a list of task data for a completed task.

    :param resp_json: The JSON response from the Todoist sync API.
    :param task: A task from the Todoist API.
    :return: A list of task data for a completed task.
    """
    completed_at = task.completed_at
    project = resp_json.get_project(task.project_id)
    section = resp_json.get_section(task.section_id)
    content = str(task.content)
    notes = _condense_notes(task.notes)
    return [completed_at, project, section, content, notes]


def _list_completed_tasks(api_token: str, since: str, until: str) -> list[list[str]]:
    """Create [completed_at project section task notes] for each completed task.

    :param api_token: The API token for the Todoist account.
    :param since: Timestamp in format YYYY-MM-DDTHH:MM:SS to use as beginning of time
    :param until: Timestamp in format YYYY-MM-DDTHH:MM:SS to use as end of time
    :return: a list of data fields for each completed task
    """
    task_lines: list[list[str]] = []
    headers = _new_headers(api_token)

    data_constants = {"since": since, "until": until, "annotate_notes": True}

    for offset in (x * 200 for x in itertools.count()):
        data = json.dumps({**data_constants, "offset": offset})
        try:
            resp = requests.post(
                "https://api.todoist.com/sync/v9/completed/get_all",
                headers=headers,
                data=data,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            if "403 Client Error: Forbidden" in str(e):
                print("Invalid API token")
                return []
            print(f"Failed to reach Todoist: {e}")
            return []

        resp_json = _Response(**resp.json())
        if not resp_json.items:
            break
        for task in resp_json.items:
            task_lines.append(_filter_task_data(resp_json, task))

    if task_lines:
        return sorted(task_lines)
    print("No completed tasks found in date range.")
    return []


def _write_tasks_to_file() -> None:
    """Write completed tasks to a file.

    :effects: Writes a file with the completed tasks.
    """
    api_args = get_api_args()
    print("communicating with Todoist server...")
    tasks = _list_completed_tasks(*api_args)

    if tasks:
        filename = f"todoist_{api_args.since}_{api_args.until}.TXT".replace(":", "-")
        task_lines = ["\t".join(t) for t in tasks]
        with open(filename, "w", encoding="utf-8") as f:
            _ = f.write("\n".join(task_lines))
        print(f"completed tasks written to '{filename}'")

    _ = input("press Enter to close...")


if __name__ == "__main__":
    _write_tasks_to_file()
