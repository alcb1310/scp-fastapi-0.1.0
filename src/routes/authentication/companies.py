import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from src import models, schemas, utils, oauth2
from src.database import get_db

router = APIRouter(
    prefix="/api/v1.0/companies",
    tags=["Companies"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.CompanyResponse])
async def get_all_companies(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Returns a list of all the companies registered
    """
    companies = db.query(models.Company).all()

    return companies


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CompanyResponse)
async def new_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """
    Creates a new company
    """
    uuid_entry = str(uuid.uuid4())
    company_dict = company.dict()
    company_dict["uuid"] = uuid_entry

    created_company = models.Company(
        uuid=company_dict["uuid"],
        ruc=company_dict["ruc"],
        name=company_dict["name"],
        employees=company_dict["employees"]
    )
    try:
        db.add(created_company)
        db.commit()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")

    uuid_entry = str(uuid.uuid4())
    user_dict = company.dict()
    user_dict["uuid"] = uuid_entry
    user_dict["company_id"] = company_dict["uuid"]
    user_dict["password"] = utils.hash_password(user_dict["password"])
    created_user = models.User(
        uuid=user_dict["uuid"],
        email=user_dict["email"],
        company_id=company_dict["uuid"],
        password=user_dict["password"],
        name=user_dict["username"]
    )

    try:
        db.add(created_user)
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    db.refresh(created_company)
    return created_company


@router.put("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.CompanyResponse)
async def update_company(
        uuid_str: str,
        company: schemas.CompanyBase,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    """
    When the user sends an updated company values, it updates the database
    """
    company_query = db.query(models.Company).filter(models.Company.uuid == uuid_str)
    company_to_update = company_query.one_or_none()
    if not company_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with uuid: {uuid_str} not found")

    company_query.update(company.dict())
    db.commit()

    return company_query.one_or_none()
