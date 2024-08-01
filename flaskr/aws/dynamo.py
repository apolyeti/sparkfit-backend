"""
This module contains functions to interact with the DynamoDB table, using the configuration from the `config` module.

Functions:
    add_user: Adds a user to the DynamoDB table.
    get_user: Retrieves a user from the DynamoDB table.
    add_clothes: Adds clothing items to the user's closet in the DynamoDB table.
    get_clothes: Retrieves the clothing items from the user's closet in the DynamoDB table.
    clear_user_closet: Clears the user's closet in the DynamoDB table.
    add_outfit: Adds outfits to the user's outfit list in the DynamoDB table.
    delete_clothing_item: Deletes a clothing item from the user's closet in the DynamoDB table.
    update_clothes: Updates a clothing item in the user's closet in the DynamoDB table.
"""

from datetime import datetime
from typing import List, Dict

from flaskr.aws.config import get_aws_session
from flaskr.utils.classes import SparkFitImage, SparkFitUser
from boto3.dynamodb.conditions import Attr

session = get_aws_session()

dynamodb = session.resource("dynamodb")


def add_user(user: SparkFitUser) -> dict:
    """
    Adds a user to the DynamoDB table. If the user already exists, the function will exit.

    Parameters:
        user (SparkFitUser): The user to add to the table.
    
    Returns:
        dict: The response from the DynamoDB table.
    """
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
            "outfits": [],
        }
    )
    return response


def get_user(email: str) -> dict:
    """
    Retrieves a user from the DynamoDB table.

    Parameters:
        email (str): The email of the user to retrieve.

    Returns:
        dict: The user data retrieved from the DynamoDB table.
    """
    table = dynamodb.Table("users")
    response = table.get_item(Key={"email": email})
    return response["Item"]


def add_clothes(email: str, clothes: List[SparkFitImage]) -> dict:
    """
    Adds clothing items to the user's closet in the DynamoDB table.

    Parameters:
        email (str): The email of the user.
        clothes (List[SparkFitImage]): The list of clothing items to add to the user's closet.

    Returns:
        dict: The response from the DynamoDB table.
    """
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


def delete_clothes(email: str, photo_id: str) -> None:
    """
    Deletes a clothing item from the user's closet in the DynamoDB table.

    Parameters:
        email (str): The email of the user.
        photo_id (str): The photo ID of the clothing item to delete.
    """

    table = dynamodb.Table("users")

    # Retrieve the item
    response = table.get_item(
        Key={"email": email}
    )

    if 'Item' in response:
        user_data = response['Item']
        if 'clothes' in user_data:
            clothes = user_data['clothes']
            
            # Find the index of the item to remove
            index_to_remove = None
            for index, item in enumerate(clothes):
                if item['photo_id'] == photo_id:
                    index_to_remove = index
                    break

            if index_to_remove is not None:
                # Remove the item at the found index
                response = table.update_item(
                    Key={"email": email},
                    UpdateExpression=f"REMOVE clothes[{index_to_remove}]",
                    ConditionExpression=Attr('clothes').size().gt(index_to_remove),
                    ReturnValues="UPDATED_NEW"
                )
                print("Clothes item removed successfully:", response)
            else:
                print("Photo ID not found in clothes list.")
        else:
            print("No clothes found for the user.")
    else:
        print("User not found.")


def get_clothes(email: str) -> List[dict]:
    """
    Retrieves the clothing items from the user's closet in the DynamoDB table.

    Parameters:
        email (str): The email of the user.

    Returns:
        List[dict]: The list of clothing items in the user's closet.
    """
    table = dynamodb.Table("users")
    response = table.get_item(Key={"email": email})
    print(response["Item"]["clothes"])
    return response["Item"]["clothes"]


def clear_user_closet(email: str) -> dict:
    """
    Clears the user's closet in the DynamoDB table.

    Parameters:
        email (str): The email of the user.

    Returns:
        dict: The response from the DynamoDB table.
    """
    table = dynamodb.Table("users")
    response = table.update_item(
        Key={"email": email},
        UpdateExpression="SET clothes = :empty_list",
        ExpressionAttributeValues={":empty_list": []},
        ReturnValues="UPDATED_NEW",
    )
    return response

def add_outfit(email: str, outfits: List[Dict]) -> dict:
    """
    Adds outfits to the user's outfit list in the DynamoDB table.

    Parameters:
        email (str): The email of the user.
        outfits (List[Dict]): The list of outfit dictionaries to add to the user's outfit list.

    Returns:
        dict: The response from the DynamoDB table.
    """
    # Add the current date to each outfit
    current_date = datetime.today().strftime("%m-%d-%Y")
    for outfit in outfits:
        outfit["date"] = current_date

    table = dynamodb.Table("users")
    response = table.update_item(
        Key={"email": email},
        UpdateExpression="SET outfits = list_append(if_not_exists(outfits, :empty_list), :o)",
        ExpressionAttributeValues={":o": outfits, ":empty_list": []},
        ReturnValues="UPDATED_NEW",
    )

    return response

def delete_clothing_item(email, photo_id) -> dict:
    """
    Deletes a clothing item from the user's closet in the DynamoDB table.

    Parameters:
        email (str): The email of the user.
        photo_id (str): The photo ID of the clothing item to delete.

    Returns:
        dict: The response from the DynamoDB table.
    """
    table = dynamodb.Table("users")
    response = table.update_item(
        Key={"email": email},
        UpdateExpression="REMOVE clothes[:c]",
        ExpressionAttributeValues={":c": photo_id},
    )

    return response

def update_clothes(email, cloth) -> None:
    """
    Updates a clothing item in the user's closet in the DynamoDB table.

    Parameters:
        email (str): The email of the user.
        cloth (dict): The updated clothing item.

    Raises:
        ValueError: If the clothing item is not found.
    """
    cloth = {
            "photo_id": cloth["photo_id"],
            "category": cloth["category"],
            "file_name": cloth["file_name"],
            "fabric": cloth["fabric"],
            "color": cloth["color"],
            "fit": cloth["fit"],
        }


    table = dynamodb.Table("users")
    # find which clothing item to update
    response = table.get_item(Key={"email": email})
    clothes = response["Item"]["clothes"]
    index = None
    for i, c in enumerate(clothes):
        if c["photo_id"] == cloth["photo_id"]:
            index = i
            break

    if index is None:
        raise ValueError("Clothing item not found")
    
    response = table.update_item(
        Key={"email": email},
        UpdateExpression=f"SET clothes[{index}] = :c",
        ExpressionAttributeValues={":c": cloth},
        ReturnValues="UPDATED_NEW",
    )