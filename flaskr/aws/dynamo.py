import os
from typing import List

from flaskr.aws.config import get_aws_session
from flaskr.utils.classes import SparkFitImage, SparkFitUser

session = get_aws_session()

dynamodb = session.resource("dynamodb")


def add_user(user: SparkFitUser):
    table = dynamodb.Table("users")

    # check if user already exists, if so, exit function
    try:
        get_user(user.email)
        return
    except:
        pass

    response = table.put_item(
        Item={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "clothes": user.clothes,
        }
    )
    return response


def get_user(email: str):
    table = dynamodb.Table("users")
    response = table.get_item(Key={"email": email})
    return response["Item"]


def add_clothes(email: str, clothes: List[SparkFitImage]):
    for cloth in clothes:
        if not cloth.photo_id:
            raise ValueError("photo_id is required for each clothing item")

    clothes_list = []
    for cloth in clothes:
        clothes_list.append(
            {
                "photo_id": cloth.photo_id,
                "category": cloth.category,
                "file_name": cloth.file_name,
                "fabric": cloth.fabric,
                "color": cloth.color,
                "fit": cloth.fit,
            }
        )

    table = dynamodb.Table("users")
    response = table.update_item(
        Key={"email": email},
        UpdateExpression="SET clothes = list_append(if_not_exists(clothes, :empty_list), :c)",
        ExpressionAttributeValues={":c": clothes_list, ":empty_list": []},
        ReturnValues="UPDATED_NEW",
    )

    return response


def delete_clothes(email: str, clothes: SparkFitImage):
    table = dynamodb.Table("users")
    response = table.update_item(
        Key={"email": email},
        UpdateExpression="REMOVE clothes[:c]",
        ExpressionAttributeValues={":c": clothes},
    )
    return response


def get_clothes(email: str):
    table = dynamodb.Table("users")
    response = table.get_item(Key={"email": email})
    print(response["Item"]["clothes"])
    return response["Item"]["clothes"]


def clear_user_closet(email: str):
    table = dynamodb.Table("users")
    response = table.update_item(
        Key={"email": email},
        UpdateExpression="SET clothes = :empty_list",
        ExpressionAttributeValues={":empty_list": []},
        ReturnValues="UPDATED_NEW",
    )
    return response
