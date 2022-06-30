from fastapi import APIRouter, status, Depends, HTTPException

import database,schema,model,auth

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs//asset.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


db = next(database.get_db())
router = APIRouter(tags=['Assets'], prefix='/asset')


@router.post('/post_assets')
def post_assets(user: schema.PostAssets, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_201_CREATED):
    logger.info("Entered post_assets")
    user_assets = model.AssetsModel(
        laptop_id=user.laptop_id,
        phone_id=user.phone_id,
        sim_number=user.sim_number,
        benefits=user.benefits,
        email_id=user.email_id,
        created_by=current_user,
        updated_by=current_user
    )
    db_sim = db.query(model.AssetsModel).filter(
        model.AssetsModel.sim_number == user.sim_number).first()
    db_laptop = db.query(model.AssetsModel).filter(
        model.AssetsModel.laptop_id == user.laptop_id).first()
    db_phone = db.query(model.AssetsModel).filter(
        model.AssetsModel.phone_id == user.phone_id).first()
    if db_sim != None or db_laptop != None or db_phone != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="already exists.")

    db.add(user_assets)
    db.commit()
    logger.debug(f"Stored new asset of user {user_assets.email_id}")
    db.refresh(user_assets)
    return user_assets


@router.get('/get_assets_by_id/{email_id}')
def get_asset_by_id(email_id: str, current_user: schema.Login = Depends(auth.get_current_user)):
    logger.info("Entered get_assets_by_id")
    logger.debug(f"Input email:{email_id}")
    req_asset = db.query(model.AssetsModel).filter(
        model.AssetsModel.email_id == email_id).all()
    logger.debug(f"Returning query object asset{req_asset[0]}")
    return (req_asset)


@router.get('/get_all_assets')
def get_all_assets(current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_200_OK):
    logger.info("Entered get_all_assets")
    all_assets = db.query(model.AssetsModel).all()
    logger.debug(f"Returning query object - all available asset objects: {len(all_assets)}")
    return (all_assets)
