# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from playwright.sync_api import expect, Page
from tests.pages.groups import GroupsPage
from tests.pages.login import LoginPage
from tests.pages.recordings_on_computer import RecordingsOnComputerPage
from tests.pages.sidebar import Sidebar


def test_verify_file_details(page: Page) -> None:
    # Tests the file details of recordings on computer page

    # Given: the user is logged in and a VRS files are present on the computer
    # Initialize the page variables and mock the API responses and login the user
    login_page = LoginPage(page)
    sidebar = Sidebar(page)
    rec_on_computer_page = RecordingsOnComputerPage(page)

    login_page.mock_api()
    sidebar.mock_api()
    rec_on_computer_page.mock_api()

    login_page.login_user()
    expect(sidebar.logout_button).to_be_visible()

    # Do : Go to recordings on computer page
    sidebar.rec_on_computer_page_button.click()

    # verify file information
    with open("mock_data/rec_on_computer_files.json", "r") as f:
        data = json.load(f)
    # Accessing data
    file1 = data["results"][0]
    file2 = data["results"][1]
    file3 = data["results"][2]
    # verify file names are rendered
    expect(rec_on_computer_page.grid_data).to_contain_text(file1["file_name"])
    expect(rec_on_computer_page.grid_data).to_contain_text(file2["file_name"])
    expect(rec_on_computer_page.grid_data).to_contain_text(file3["file_name"])
    # verify profiles are rendered
    expect(rec_on_computer_page.grid_data).to_contain_text(file1["recording_profile"])
    expect(rec_on_computer_page.grid_data).to_contain_text(file2["recording_profile"])
    expect(rec_on_computer_page.grid_data).to_contain_text(file3["recording_profile"])


def test_single_mps_requests(page: Page) -> None:
    # Tests the single mps requests functionality in recordings on computer page

    # Given: the user is logged in and a VRS files are present on the computer
    # Initialize the page variables and mock the API responses and login the user
    login_page = LoginPage(page)
    sidebar = Sidebar(page)
    rec_on_computer_page = RecordingsOnComputerPage(page)

    login_page.mock_api()
    sidebar.mock_api()
    rec_on_computer_page.mock_api()

    login_page.login_user()
    expect(sidebar.logout_button).to_be_visible()

    # Do : Go to recordings on computer page, select all files and request mps
    sidebar.rec_on_computer_page_button.click()
    rec_on_computer_page.select_all_button.click()
    rec_on_computer_page.request_mps_for_selected_files()
    # verify mps request is successful by checking the alert message
    # since alert msg is same as api response, directly using it here
    with open("mock_data/single_mps_response.json", "r") as f:
        data = json.load(f)
    expect(rec_on_computer_page.top_alert).to_contain_text(data["message"])


def test_add_to_group(page: Page) -> None:
    # Tests the add to group functionality in recordings on computer page

    # Given: the user is logged in and a VRS files are present on the computer
    # Initialize the page variables and mock the API responses and login the user
    login_page = LoginPage(page)
    sidebar = Sidebar(page)
    rec_on_computer_page = RecordingsOnComputerPage(page)
    groups_page = GroupsPage(page)

    login_page.mock_api()
    sidebar.mock_api()
    rec_on_computer_page.mock_api()

    login_page.login_user()
    expect(sidebar.logout_button).to_be_visible()

    # Do : Go to recordings on computer page, select all files and add to group
    sidebar.rec_on_computer_page_button.click()
    rec_on_computer_page.select_all_button.click()
    rec_on_computer_page.add_to_group_button.click()
    with open("mock_data/group_data.json", "r") as f:
        data = json.load(f)
    test_group_name = data[0]["name"]
    rec_on_computer_page.select_group(test_group_name)
    rec_on_computer_page.add_recordings_button.click()
    rec_on_computer_page.done_button.click()

    # verify files are added to group by checking the groups page
    groups_page.mock_add_files_to_group_api(test_group_name)
    sidebar.groups_button.click()
    groups_page.expand_row.click()
    with open("mock_data/rec_on_computer_files.json", "r") as f:
        data = json.load(f)
    file_names = [item["file_name"] for item in data["results"]]
    for file_name in file_names:
        expect(groups_page.expand_group_data).to_contain_text(file_name)
