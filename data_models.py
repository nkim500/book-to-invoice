from datetime import date
from datetime import datetime
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict
from pytz import timezone


def et_datetime_now():
    eastern = timezone("US/Eastern")
    return datetime.now(tz=eastern)


def et_date_now():
    eastern = timezone("US/Eastern")
    return datetime.now(tz=eastern).date()


def et_date_due():
    eastern = timezone("US/Eastern")
    return datetime.now(tz=eastern).date().replace(day=1)


class WaterUsage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    watermeter_id: int = Field(nullable=False)
    previous_date: date = Field(default_factory=et_date_now)
    current_date: date = Field(default_factory=et_date_now)
    previous_reading: int = Field(default=0)
    current_reading: int = Field(default=0)
    statement_date: date = Field(default_factory=et_date_due)
    inserted_at: datetime = Field(default_factory=et_datetime_now)

    @field_serializer("id")
    def serialize_uuid(self, v: UUID, _info):
        return str(v)

    @field_serializer("previous_date", "current_date", "statement_date", "inserted_at")
    def serialize_date(self, v: date | datetime, _info):
        if isinstance(v, str):
            return v
        else:
            return v.isoformat()

    @model_validator(mode="after")
    def check_property(self):
        if self.current_reading < self.previous_reading:
            raise ValueError("Current reading cannot be less than previous reading")
        return self

    @property
    def water_usage(self):
        return self.current_reading - self.previous_reading

    def water_bill_dollar_amount(self, water_rate: float, service_fee: float):
        return round(self.water_usage * water_rate + service_fee, 2)


class Property(BaseModel):
    property_code: str = Field(default="")
    street_address: str = Field(default="")
    city_state_zip: str = Field(default="")

    model_config = SettingsConfigDict(arbitrary_types_allowed=True)


class InvoiceFileParse(BaseModel):
    A1: str = Field(default="", alias="business_name")
    A2: str = Field(default="", alias="business_address_1")
    A3: str = Field(default="", alias="business_address_2")
    A4: str = Field(default="", alias="business_contact_phone")
    A5: str = Field(default="", alias="business_contact_email")
    B7: str = Field(default="", alias="tenant_name")
    B8: str = Field(default="", alias="tenant_address_1")
    B9: str = Field(default="", alias="tenant_address_2")
    F3: date = Field(default_factory=et_date_now, alias="invoice_date")
    F4: str = Field(default="", alias="invoice_customer_id")
    F5: float = Field(default=0, alias="invoice_total_amount_due")
    F6: date = Field(default_factory=et_date_due, alias="invoice_due_date")
    A13: Optional[date] = Field(default_factory=None, alias="date_today_1")
    A14: Optional[date] = Field(default_factory=None, alias="date_today_2")
    A15: Optional[date] = Field(default_factory=None, alias="date_late")
    A16: Optional[date] = Field(default_factory=None, alias="date_rent")
    A17: Optional[date] = Field(default_factory=None, alias="date_water")
    A18: Optional[date] = Field(default_factory=None, alias="date_storage")
    A19: Optional[date] = Field(default_factory=None, alias="date_other_rent")
    A22: Optional[str] = Field(default=None, alias="detail_other_rent")
    C13: Optional[str] = Field(default=None, alias="desc_prev_month_paid")
    C14: Optional[str] = Field(default=None, alias="desc_prev_month_residual")
    C15: Optional[str] = Field(default=None, alias="desc_late_fee")
    C16: Optional[str] = Field(default=None, alias="desc_curr_rent")
    C17: Optional[str] = Field(default=None, alias="desc_curr_water")
    C18: Optional[str] = Field(default=None, alias="desc_curr_storage")
    C19: Optional[str] = Field(default=None, alias="desc_other_rent")
    C20: Optional[str] = Field(default=None, alias="desc_prev_overdue")
    F13: Optional[float] = Field(default=None, alias="amt_prev_month_paid")
    F14: Optional[float] = Field(default=None, alias="amt_prev_month_residual")
    F15: Optional[float] = Field(default=None, alias="amt_late_fee")
    F16: Optional[float] = Field(default=None, alias="amt_rent")
    F17: Optional[float] = Field(default=None, alias="amt_water")
    F18: Optional[float] = Field(default=None, alias="amt_storage")
    F19: Optional[float] = Field(default=None, alias="amt_other_rent")
    F20: Optional[float] = Field(default=None, alias="amt_overdue")
    F21: Optional[float] = Field(default=None, alias="amt_total_amount_due")
    A27: Optional[int] = Field(default=None, alias="water_meter_id")
    B26: Optional[date] = Field(default=None, alias="water_prev_date")
    B27: Optional[int] = Field(default=None, alias="water_prev_read")
    C26: Optional[date] = Field(default=None, alias="water_curr_date")
    C27: Optional[int] = Field(default=None, alias="water_curr_read")
    D27: Optional[int] = Field(default=None, alias="water_usage_period")
    E27: Optional[float] = Field(default=None, alias="water_bill_period")
    A37: str = Field(default="", alias="business_name_")
    A38: str = Field(default="", alias="business_address_1_")
    A39: str = Field(default="", alias="business_address_2_")
    A43: str = Field(default="", alias="business_contact_email_")
    F36: date = Field(default_factory=et_date_now, alias="invoice_date_")
    F37: str = Field(default="", alias="invoice_customer_id_")
    F39: date = Field(default_factory=et_date_due, alias="invoice_due_date_")
    F40: float = Field(default=0, alias="invoice_total_amount_due_")

    model_config = SettingsConfigDict(populate_by_name=True)


class BookIngest(BaseModel):
    lot_id: int
    tenant_name: str
    starting_balance: float
    monthly_due_last_month: float
    paid_on_time_last_month: float
    paid_past_due_last_month: float
    late_fee_accrued_last_month: float
    total_carried_over_last_month: float
    ending_balance: float
    monthly_rent: float
    monthly_storage: float
    monthly_water: float
    monthly_other: float
    new_charges_this_month: float
    payment_on_time_1: float
    payment_on_time_2: float
    payment_on_time_3: float
    payment_overdue_1: float
    payment_overdue_2: float
    payment_overdue_3: float
    payment_overdue_4: float
    late_fee_this_month: float
    carry_over_to_next_month: float

    @model_validator(mode="after")
    def zero_out_missing_values(self): ...

    @property
    def total_amount_due_for_invoice(self):
        return self.ending_balance + self.new_charges_this_month
