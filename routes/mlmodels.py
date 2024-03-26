from . import create_route
from authentication import get_current_user
from database import get_pd_db
from fastapi import Depends, UploadFile
from schemas import CreateUser
from schemas import CreateML, ShowML
import pandas as pd
from models import Models
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import datetime

router = create_route(
    prefix="mlmodels",
    tags="MLModels",
)


@router.post("/rf")
async def train_and_predict_rf(
    request: CreateML,
    data: pd = Depends(get_pd_db),
    user: CreateUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        request (CreateML): _description_
        data (pd, optional): _description_. Defaults to Depends(get_pd_db).
        user (CreateUser, optional): _description_. Defaults to Depends(get_current_user).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: A schema describing the results of the model which has been utilised
    """

    data["QUARTER"] = pd.to_datetime(data["QUARTER"], format="%Y-%m-%d")

    # Now you can proceed with correlation and feature selection
    selected_features = ["A1", "A32", "A35", "A8"] + list(
        data.corr()["LABEL"].abs().nlargest(10).index[:3]
    )
    X = data[selected_features]
    y = data["LABEL"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    ###############################################################
    ################### RandomForestClassifier ####################
    ###############################################################

    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)

    predictions_rf = rf.predict(X_test)
    accuracy_rf = accuracy_score(y_test, predictions_rf)
    classification_report_rf = classification_report(y_test, predictions_rf)
    confusion_matrix_rf = confusion_matrix(y_test, predictions_rf)

    title = "Logistic Regression prediction"
    description = f"Accuracy score for classification is {accuracy_rf} and classification report is {classification_report_rf} and confusion matrix is {confusion_matrix_rf}"

    model = Models(
        title=title,
        description=description,
        user_id=request.user_id,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
    pass


@router.post("/lg")
async def train_and_predict_lg(
    request: CreateML,
    data: pd = Depends(get_pd_db),
    user: CreateUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        request (CreateML): _description_
        data (pd, optional): _description_. Defaults to Depends(get_pd_db).
        user (CreateUser, optional): _description_. Defaults to Depends(get_current_user).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: A schema describing the results of the model which has been utilised where in this case it is LogisticRegression
    """

    data["QUARTER"] = pd.to_datetime(data["QUARTER"], format="%Y-%m-%d")

    # Now you can proceed with correlation and feature selection
    selected_features = ["A1", "A32", "A35", "A8"] + list(
        data.corr()["LABEL"].abs().nlargest(10).index[:3]
    )
    X = data[selected_features]
    y = data["LABEL"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    ###############################################################
    ################### LogisticRegression ########################
    ###############################################################

    clf = LogisticRegression()
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    classification_report_ = classification_report(y_test, predictions)
    confusion_matrix_ = confusion_matrix(y_test, predictions)

    title = "Logistic Regression prediction"
    description = f"Accuracy score for classification is {accuracy} and classification report is {classification_report_} and confusion matrix is {confusion_matrix_}"

    model = Models(
        title=title,
        description=description,
        user_id=request.user_id,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
    pass


@router.post("/gb")
async def train_and_predict_gb(
    request: CreateML,
    data: pd = Depends(get_pd_db),
    user: CreateUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        request (CreateML): _description_
        data (pd, optional): _description_. Defaults to Depends(get_pd_db).
        user (CreateUser, optional): _description_. Defaults to Depends(get_current_user).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: A schema describing the results of the model which has been utilised where in this case it is GradientBoostingClassifier
    """

    data["QUARTER"] = pd.to_datetime(data["QUARTER"], format="%Y-%m-%d")

    # Now you can proceed with correlation and feature selection
    selected_features = ["A1", "A32", "A35", "A8"] + list(
        data.corr()["LABEL"].abs().nlargest(10).index[:3]
    )
    X = data[selected_features]
    y = data["LABEL"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    ###############################################################
    ################### GradientBoostingClassifier ########################
    ###############################################################

    from sklearn.ensemble import GradientBoostingClassifier

    gbm = GradientBoostingClassifier(random_state=42)
    gbm.fit(X_train, y_train)

    predictions_gbm = gbm.predict(X_test)
    accuracy_gbm = accuracy_score(y_test, predictions_gbm)
    classification_report_gbm = classification_report(y_test, predictions_gbm)
    confusion_matrix_gbm = confusion_matrix(y_test, predictions_gbm)

    title = "Gradient Boosting Classifier prediction"
    description = f"Accuracy score for classification is {accuracy_gbm} and classification report is {classification_report_gbm} and confusion matrix is {confusion_matrix_gbm}"

    model = Models(
        title=title,
        description=description,
        user_id=request.user_id,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
    pass


@router.get("/visualization")
async def serialize_data(
    data: pd = Depends(get_pd_db),
    # user: CreateUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    selected_columns = [
        "ID",
        "QUARTER",
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A16",
        "A17",
        "A18",
        "A19",
        "A20",
        "A21",
        "A22",
        "A23",
        "A24",
        "A25",
        "A26",
        "A27",
        "A28",
        "A29",
        "A30",
        "A31",
        "A32",
        "A33",
        "A34",
        "A35",
        "A36",
        "A37",
        "A38",
        "A39",
        "A40",
        "A41",
        "A42",
        "A43",
        "A44",
        "A45",
        "A46",
        "A47",
        "A48",
        "A49",
        "A50",
        "A51",
        "A52",
        "A53",
        "A54",
        "A55",
        "A56",
        "A57",
        "A58",
        "A59",
        "A60",
        "A61",
        "A62",
        "A63",
        "A64",
        "A65",
        "A66",
        "A67",
        "A68",
        "A69",
        "A70",
        "A71",
        "A72",
        "A73",
        "A74",
        "A75",
        "A76",
        "A77",
        "A78",
        "A79",
        "A80",
        "A81",
        "A82",
        "A83",
        "A84",
    ]

    data = data[selected_columns]

    class DataObject:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    serialized_data = []
    for _, row in data.head(100).iterrows():
        data_object = DataObject(**row.to_dict())
        serialized_data.append(data_object)

    for obj in serialized_data[:5]:
        print(obj.__dict__)

    return serialized_data

    pass


@router.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile,
    user: CreateUser = Depends(get_current_user),
):
    return {
        "message": f"File {file.filename} uploaded successfully",
    }


@router.get("/show", response_model=List[ShowML])
async def method_name(db: Session = Depends(get_db)):
    models = db.query(Models).all()
    return models
    pass
