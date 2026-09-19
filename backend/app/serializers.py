from decimal import Decimal

from app.models.grind_pass import GrindPass
from app.models.mill import Mill
from app.models.user import User
from app.models.viscosity_sample import ViscositySample
from app.models.workshop import Workshop
from app.utils import dt_to_json


def _num(value: Decimal | float | int | None) -> float | None:
    if value is None:
        return None
    return float(value)


def user_json(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "displayName": user.display_name,
        "role": user.role,
    }


def workshop_json(row: Workshop) -> dict:
    return {
        "id": row.id,
        "name": row.name,
        "site": row.site,
        "notes": row.notes,
    }


def mill_json(row: Mill) -> dict:
    return {
        "id": row.id,
        "workshopId": row.workshop_id,
        "millCode": row.mill_code,
        "pigmentBase": row.pigment_base,
        "bowlLiters": _num(row.bowl_liters) or 0,
        "status": row.status,
    }


def viscosity_sample_json(row: ViscositySample) -> dict:
    return {
        "id": row.id,
        "millId": row.mill_id,
        "millCode": row.mill.mill_code,
        "sampledAt": dt_to_json(row.sampled_at),
        "viscosityPaS": _num(row.viscosity_pa_s) or 0,
        "tempC": _num(row.temp_c),
        "notes": row.notes,
    }


def grind_pass_json(row: GrindPass) -> dict:
    return {
        "id": row.id,
        "millId": row.mill_id,
        "millCode": row.mill.mill_code,
        "startedAt": dt_to_json(row.started_at),
        "passNo": row.pass_no,
        "durationMin": _num(row.duration_min) or 0,
        "mediaType": row.media_type,
        "operatorName": row.operator_name,
    }
