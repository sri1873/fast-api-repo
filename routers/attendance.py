from fastapi import APIRouter, status, Depends, HTTPException
from datetime import datetime
import database, schema, model, auth

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs//attendance.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

db = next(database.get_db())

router = APIRouter(
    tags=['Attendance'],
    prefix='/attendance'
)


# ------------------------------------------------------Attendance


@router.post('/add')
def post_attendance(user: schema.PostAttendance, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_201_CREATED):
    days_present = db.query(model.AttendanceModel).filter(
        model.AttendanceModel.email_id == current_user).count()
    logger.debug(f"Entered add()--num days present:{days_present}")
    if user.in_time:
        gen_in_time = datetime.utcnow()
    today = model.AttendanceModel(
        in_time=gen_in_time,
        percentage=(days_present/22)*100,
        email_id=current_user
    )
    db.add(today)
    db.commit()
    db.refresh(today)
    logger.debug(f"Entered attendance timestamp:{today.in_time}")
    return today


@router.get('/get_attendance')
def get_attendance(current_user: schema.Login = Depends(auth.get_current_user)):
    logger.info("Executing get_attendance()")
    attendance_sheet = db.query(model.AttendanceModel).all()
    logger.debug(f"Returning query object - all available asset objects: {len(attendance_sheet)}")
    return attendance_sheet


@router.post('/get_attendance_by_id/{email_id}')
def get_attendance_by_id(email_id: str, current_user: schema.Login = Depends(auth.get_current_user)):
    logger.info(f"Entered get_attendance_by_id----user input: {email_id}")
    attendance = db.query(model.AttendanceModel).filter(
        model.AttendanceModel.email_id == email_id).all()
    logger.debug(
        f"Returning query object - all available attendance objects for given email: {len(attendance)}")
    return attendance


@router.post('/get/{date}')
def get_attendance_of_a_date(date: str, current_user: schema.Login = Depends(auth.get_current_user)):
    logger.info(f"Entered get----user input: {date}")
    attendance_sheet = db.query(model.AttendanceModel).filter(
        model.AttendanceModel.current_date == date).all()
    logger.debug(
        f"Returning query object - all available asset objects: {len(attendance_sheet)}")
    return(attendance_sheet)
