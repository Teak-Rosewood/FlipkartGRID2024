from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def root():
    return {"message": "this is the pipeline router"}

@router.post('/extract_data')
async def root():
    return {"message": "this is the testing router"}