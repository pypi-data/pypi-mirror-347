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
from tests.utils.constants import PAST_MPS_REQUESTS_URL


class PastMpsRequestsPage:
    URL: str = PAST_MPS_REQUESTS_URL

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.grid_data: Locator = page.get_by_role("grid")

    def navigate(self, url: str = URL) -> None:
        self.page.goto(url)

    def mock_api(self):
        self.page.route(
            "**/mps/get-all-requests/",
            lambda route: route.fulfill(path="mock_data/past_mps_data.json"),
        )
        self.page.route(
            "**/auth/is-logged-in",
            lambda route: route.fulfill(status=200, json=[{"logged_in": True}]),
        )
