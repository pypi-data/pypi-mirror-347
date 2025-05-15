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
from tests.pages.sidebar import Sidebar


def test_device_information(page: Page) -> None:
    # Tests the glasses information rendereing in sidebar

    # Given: the user is logged in
    login_page = LoginPage(page)
    login_page.mock_api()
    login_page.login_user()

    # Do: mock glasses connection
    sidebar = Sidebar(page)
    sidebar.mock_api()
    # Verify: the glasses details are correct
    with open("mock_data/glasses_data.json", "r") as f:
        data = json.load(f)

    expect(sidebar.serial_number).to_contain_text(data["serial_number"])
    expect(sidebar.wifi_battery).to_contain_text(data["wifi_ssid"])
    expect(sidebar.wifi_battery).to_contain_text(str(data["battery_level"]))


def test_glasses_not_connected(page: Page) -> None:
    # Tests the glasses information rendereing in sidebar when glasses are not connected

    # Given: the user is logged in
    login_page = LoginPage(page)
    login_page.mock_api()
    login_page.login_user()

    # Do: Do not mock glasses connection
    sidebar = Sidebar(page)

    # Verify: device not connected is shown
    expect(sidebar.device_not_connected).to_contain_text("Device Not Connected")
