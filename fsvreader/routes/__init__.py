from fastapi import APIRouter

from fsvreader.routes import dirs, lookup, reader, statics

router = APIRouter()

router.include_router(dirs.router)
router.include_router(reader.router)
router.include_router(statics.router)
router.include_router(lookup.router)
