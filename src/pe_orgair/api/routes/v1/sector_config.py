from fastapi import APIRouter, HTTPException
from pe_orgair.services.sector_config import sector_service

router = APIRouter(prefix="/sectors", tags=["sectors"])

@router.get("/{focus_group_id}")
async def get_sector_config(focus_group_id: str):
    cfg = await sector_service.get_config(focus_group_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Unknown focus_group_id")
    return {
        "focus_group_id": cfg.focus_group_id,
        "group_name": cfg.group_name,
        "group_code": cfg.group_code,
        "dimension_weights": {k: str(v) for k, v in cfg.dimension_weights.items()},
        "calibrations": {k: str(v) for k, v in cfg.calibrations.items()},
        "weights_sum_ok": cfg.validate_weights_sum(),
    }