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


class Sidebar:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.glasses_page_button: Locator = page.get_by_role(
            "button", name="Recordings on glasses"
        )
        self.rec_on_computer_page_button: Locator = page.get_by_role(
            "button", name="Recordings on computer"
        )
        self.past_mps_requests_button: Locator = page.get_by_role(
            "button", name="Past MPS requests"
        )
        self.groups_button: Locator = page.get_by_role("button", name="Groups")
        self.logout_button: Locator = page.get_by_role("button", name="Log out")
        self.serial_number: Locator = page.locator("#root")
        self.wifi_battery: Locator = page.get_by_test_id("content").locator("div")
        self.device_not_connected = page.get_by_test_id("content").get_by_role(
            "paragraph"
        )

    def click_logout_button(self) -> None:
        self.logout_button.click()

    def mock_api(self):
        self.page.route(
            "**/device/status",
            lambda route: route.fulfill(path="mock_data/glasses_data.json"),
        )
        self.page.route(
            "**/auth/logout",
            lambda route: route.fulfill(status=200, json=[{"message": "LO200"}]),
        )
