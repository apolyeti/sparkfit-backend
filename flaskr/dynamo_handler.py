import boto3
import os
from classes import SparkFitImage, SparkFitUser
from typing import List

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY_ID')
REGION = os.getenv('AWS_REGION')

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

dynamodb = session.resource('dynamodb')


def add_user(user: SparkFitUser):
    table = dynamodb.Table('users')
    response = table.put_item(
        Item={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'clothes': user.clothes
        }
    )
    return response

def get_user(email: str):
    table = dynamodb.Table('users')
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response['Item']

def add_clothes(email: str, clothes: List[SparkFitImage]):
    for cloth in clothes:
        if not cloth.photo_id:
            raise ValueError('photo_id is required for each clothing item')

    clothes_list = [item.to_dict() for item in clothes]

    table = dynamodb.Table('users')
    response = table.update_item(
        Key={
            'email': email
        },
        UpdateExpression='SET clothes = list_append(if_not_exists(clothes, :empty_list), :c)',
        ExpressionAttributeValues={
            ':c': clothes_list,
            ':empty_list': []
        },
        ReturnValues="UPDATED_NEW"
    )

    return response

def delete_clothes(email: str, clothes: SparkFitImage):
    table = dynamodb.Table('users')
    response = table.update_item(
        Key={
            'email': email
        },
        UpdateExpression='REMOVE clothes[:c]',
        ExpressionAttributeValues={
            ':c': clothes
        }
    )
    return response

def get_clothes(email: str):
    table = dynamodb.Table('users')
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response['Item']['clothes']

# if __name__ == '__main__':
#     user = SparkFitUser(
#         first_name='John',
#         last_name='Doe',
#         email='example@example.com',
#         clothes=[]
#     )

#     print('user added')

#     clothes = [
#         SparkFitImage(
#             photo_id='1',
#             predicted_classes=['t-shirt', 'jeans'],
#             file_name='test.jpg',
#             data='data:image/jpeg;base64,encoded_image',
#             fabric='cotton',
#             color='blue',
#             fit='slim'
#         ),
#         SparkFitImage(
#             photo_id='2',
#             predicted_classes=['t-shirt', 'jeans'],
#             file_name='test.jpg',
#             data='data:image/jpeg;base64,encoded_image',
#             fabric='cotton',
#             color='blue',
#             fit='slim'
#         )
#     ]

#     try:
#         add_clothes(user.email, clothes)
#         print('clothes added')
#     except Exception as e:
#         print(e)
#         print('clothes not added')
    
#     print(get_clothes(user.email))
    







