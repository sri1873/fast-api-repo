from fastapi import APIRouter, status, Depends
import database, schema, model, auth, hashing
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs//user.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


db = next(database.get_db())

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(model.UserModel).filter(
        model.UserModel.email_id == form_data.username).first()
    if not(user and hashing.verify_password(form_data.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = auth.create_access_token(
        data={"mail": user.email_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/create')
def create_user(user: schema.CreateUser, status_code=status.HTTP_201_CREATED):
    hashed_password = hashing.get_password_hash(user.password)

    new_user = model.UserModel(
        email_id=user.email_id,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        phone_number=user.phone_number,
        address=user.address,
        city=user.city,
        state=user.state,
        country=user.country,
        created_by='current_user',
        updated_by='current_user'
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return f"Successfully Registered user with Mail-ID: {new_user.email_id}"


@router.put('/update/{user_email_id}', response_model=schema.UserDetails)
def update_user(user_email_id: str, user: schema.UserDetails, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_200_OK):

    user_to_update = db.query(model.UserModel).filter(
        model.UserModel.email_id == user_email_id).first()
    user_to_update.first_name = user.first_name,
    user_to_update.last_name = user.last_name,
    user_to_update.date_ofbirth = user.date_of_birth,
    user_to_update.phone_number = user.phone_number,
    user_to_update.address = user.address,
    user_to_update.city = user.city,
    user_to_update.state = user.state,
    user_to_update.country = user.country,
    user_to_update.updated_by = current_user
    db.commit()
    db.refresh(user_to_update)
    return user_to_update


@router.delete('/remove/{user_email_id}')
def delete_user(user_email_id: str, current_user: schema.Login = Depends(auth.get_current_user)):
    user = db.query(model.UserModel).filter(
        model.UserModel.email_id == user_email_id).delete()
    db.commit()
    return f"{user_email_id} deleted"
