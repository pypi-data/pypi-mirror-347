from __future__ import annotations

from typing import Any
from typing import Literal

import cloudscraper
from pydantic import BaseModel
from pydantic import Field


# https://www.tripplus.cc/api/awardplus/query/?ori=TPE&dst=KIX&cabin=c&type=rt&programs=ALL
class RedemptionRequest(BaseModel):
    ori: str = Field(..., description="Origin airport code")
    dst: str = Field(..., description="Destination airport code")
    cabin: Literal["y", "c", "f"] = Field(default="y", description="Cabin class, y: economy, c: business, f: first")
    type: Literal["ow", "rt"] = Field(default="ow", description="Redemption type, ow: one way, rt: round trip")
    programs: str = "ALL"

    def do(self) -> RedemptionResponse:
        url = "https://www.tripplus.cc/api/awardplus/query/"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
        resp = cloudscraper.create_scraper().get(url, headers=headers, params=self.model_dump())
        resp.raise_for_status()

        return RedemptionResponse.model_validate(resp.json())


class ReferralProduct(BaseModel):
    code: str
    program_codes: list[str]


class Meta(BaseModel):
    count: int
    referral_products: list[ReferralProduct]


class Tag(BaseModel):
    type: str
    text: str
    status: bool | None = None
    description: str | None = None


class Resources(BaseModel):
    type: str
    items: list[str]


class Route(BaseModel):
    miles_desc: str
    origin: str
    stop: str | None
    destination: str
    operating_program_code: str
    operating_program_name: str


class Item(BaseModel):
    origin: str
    destination: str
    type: str
    cabin: str
    bookmark_id: Any
    bookmarked: bool
    route_stop_desc: list[str]
    tags: list[Tag]
    resources: Resources
    miles: int
    miles_desc: str
    program_code: str
    program_name: str
    program_link: str | None
    program_link_desc: str | None
    program_tel: str | None
    program_email: Any
    program_expiration_desc: str | None
    operating_program_code: str | None
    operating_program_name: str
    level: str
    systems: list[str]
    routes: list[Route]


class RedemptionResponse(BaseModel):
    meta: Meta
    items: list[Item]
