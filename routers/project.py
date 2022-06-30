from fastapi import APIRouter, status, Depends, HTTPException
import database, schema, model, auth
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs//project.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

db = next(database.get_db())
router = APIRouter(
    tags=['Project'],
    prefix='/project'
)


# ------------------------------------------------------Projects


@router.post('/post_project')
def project_details(user: schema.PostProject, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_201_CREATED):
    logger.info("Executing post_project...")
    project = model.Project(
        project_id=user.project_id,
        project_description=user.project_description,
        duration=user.duration,
        start_date=user.start_date,
        end_date=user.end_date,
        posted_by=current_user
    )
    db_project = db.query(model.Project).filter(
        model.Project.project_id == user.project_id).first()
    if db_project != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"project with id {user.project_id} already exists.")
    db.add(project)
    db.commit()
    logger.debug(f"Added a new project of id: {project.project_id}")
    db.refresh(project)
    return project


@router.get('/get_all')
def get_all_projects(current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_200_OK):
    logger.info("Executing get_all()...")
    all_projects = db.query(model.Project).all()
    logger.debug(
        f"Returning query object - all available projects objects: {len(all_projects)}")
    return (all_projects)


@router.post('/create_teams')
def create_teams(user: schema.CreateTeam, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_201_CREATED):
    logger.info("Executing create_teams()...")
    team = model.Teams(
        project_id=user.project_id,
        email_id=user.email_id,
        created_by=current_user
    )
    db.add(team)
    db.commit()
    logger.debug(f"Added a team to database of project id: {team.project_id}")
    db.refresh(team)
    return


@router.post('/get_team_by_id/{project_id}')
def get_team(project_id: int, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_200_OK):
    logger.info(f"Executing get_team_by_id input: {project_id}")
    team = db.query(model.Teams).filter(
        model.Teams.project_id == project_id).all()
    logger.debug(
        f"Returning query object - all available teams on id objects: {len(team)}")
    return(team)


asset_join = db.query(model.UserModel, model.AssetsModel).join(
    model.UserModel)

attendance_join = db.query(model.AttendanceModel, model.UserModel).join(
    model.AttendanceModel)

team_join = db.query(model.UserModel, model.Teams).join(model.UserModel)


@router.post('/get_all/{email_id}')
def get_all(email_id: str, current_user: schema.Login = Depends(auth.get_current_user), status_code=status.HTTP_200_OK):
    x = asset_join.filter(model.UserModel.email_id == email_id).all()
    y = attendance_join.filter(model.UserModel.email_id == email_id).all()
    z = team_join.filter(model.UserModel.email_id == email_id).all()
    return(x[0][1], y, z[0][1])
