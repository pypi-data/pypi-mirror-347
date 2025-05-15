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
from tests.pages.login import LoginPage
from tests.pages.recordings_on_glasses import RecordingsOnGlassesPage
from tests.pages.sidebar import Sidebar


def test_verify_file_details(page: Page) -> None:
    # Tests the file details of recordings on glasses page

    # Given: the user is logged in and a glasses are connected
    # Initialize the page variables and mock the API responses and login the user
    login_page = LoginPage(page)
    sidebar = Sidebar(page)
    glasses_page = RecordingsOnGlassesPage(page)

    login_page.mock_api()
    sidebar.mock_api()
    glasses_page.mock_api()

    login_page.login_user()
    expect(sidebar.logout_button).to_be_visible()

    # Do : Go to recordings on glasses page and open list view
    sidebar.glasses_page_button.click()
    glasses_page.list_view_button.click()

    # verify file information
    with open("mock_data/glasses_files.json", "r") as f:
        data = json.load(f)
    # Accessing data
    file1 = data["results"][0]
    file2 = data["results"][1]
    file3 = data["results"][2]
    # verify file names are rendered
    expect(glasses_page.grid_data).to_contain_text(file1["file_name"])
    expect(glasses_page.grid_data).to_contain_text(file2["file_name"])
    expect(glasses_page.grid_data).to_contain_text(file3["file_name"])
    # verify profiles are rendered
    expect(glasses_page.grid_data).to_contain_text(file1["recording_profile"])
    expect(glasses_page.grid_data).to_contain_text(file2["recording_profile"])
    expect(glasses_page.grid_data).to_contain_text(file3["recording_profile"])


def test_glasses_not_connected(page: Page) -> None:
    # Tests the details of recordings on glasses page when glasses are not connected

    # Given: the user is logged in and a glasses are not connected
    # Initialize the page variables
    login_page = LoginPage(page)
    sidebar = Sidebar(page)
    glasses_page = RecordingsOnGlassesPage(page)
    # Mock the API responses
    login_page.mock_api()
    # Login the user
    login_page.login_user()
    expect(sidebar.logout_button).to_be_visible()

    # Do : Go to recordings on glasses page and open list view
    sidebar.glasses_page_button.click()

    # verify file information
    expect(glasses_page.device_not_connected_img).to_be_visible


def test_no_files_on_glasses(page: Page) -> None:
    # Tests the details of recordings on glasses page when no files are on glasses and glasses are connected

    # Given: the user is logged in and a glasses are connected
    # Initialize the page variables
    login_page = LoginPage(page)
    sidebar = Sidebar(page)
    glasses_page = RecordingsOnGlassesPage(page)

    # Mock the API responses
    login_page.mock_api()
    sidebar.mock_api()
    glasses_page.mock_no_files_api()
    # Login the user
    login_page.login_user()
    expect(sidebar.logout_button).to_be_visible()

    # Do : Go to recordings on glasses page and open list view
    sidebar.glasses_page_button.click()

    # verify file information
    expect(glasses_page.no_recordings_on_glasses).to_be_visible()
