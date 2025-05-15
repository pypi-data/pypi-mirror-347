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

from playwright.sync_api import Locator, Page
from tests.utils.constants import RECORDINGS_ON_COMPUTER_URL


class RecordingsOnComputerPage:
    URL: str = RECORDINGS_ON_COMPUTER_URL

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.grid_data: Locator = page.get_by_role("grid")
        self.request_mps_button: Locator = page.get_by_role(
            "button", name="Request MPS"
        )
        self.add_to_group_button: Locator = page.get_by_role(
            "button", name="Add to a Group"
        )
        self.select_all_button: Locator = page.get_by_role("button", name="Select All")
        self.slam_checkbox: Locator = page.get_by_label("SLAM")
        self.eye_gaze_checkbox: Locator = page.get_by_label("Eye Gaze")
        self.hand_tracking_checkbox: Locator = page.get_by_label("Hand Tracking")
        self.reprocess_completed_checkbox: Locator = page.get_by_label(
            "Re-process completed"
        )
        self.done_button: Locator = page.get_by_role("button", name="Done")
        self.top_alert: Locator = page.get_by_role("alert").first
        self.add_recordings_button: Locator = page.get_by_role(
            "button", name="Add recordings"
        )

    def navigate(self, url: str = URL) -> None:
        self.page.goto(url)

    def mock_api(self) -> None:
        self.page.route(
            "**/local/files",
            lambda route: route.fulfill(path="mock_data/rec_on_computer_files.json"),
        )
        # abort all image requests
        self.page.route(
            "**/local/thumbnail_jpeg?file_path=*",
            lambda route: route.abort(),
        )
        self.page.route(
            "**/mps-status/",
            lambda route: route.abort(),
        )
        self.page.route(
            "**/mps/request-single/",
            lambda route: route.fulfill(
                status=202,
                path="mock_data/single_mps_response.json",
            ),
        )
        self.page.route(
            "**/mps/check-processing-status/",
            lambda route: route.abort(),
        )
        self.page.route(
            "**/group/list",
            lambda route: route.fulfill(
                status=200,
                path="mock_data/group_data.json",
            ),
        )
        self.page.route(
            "**/group/add_files",
            lambda route: route.fulfill(
                status=200,
            ),
        )

    def select_file_by_click(self, file_name: str) -> None:
        self.page.get_by_text(file_name).click()

    def request_mps_for_selected_files(self) -> None:
        self.request_mps_button.click()
        self.slam_checkbox.check()
        self.eye_gaze_checkbox.check()
        self.hand_tracking_checkbox.check()
        self.reprocess_completed_checkbox.check()
        self.done_button.click()

    def select_group(self, group_name: str) -> None:
        self.page.get_by_role("cell", name=group_name).click()
