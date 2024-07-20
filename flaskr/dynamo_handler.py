import boto3
import os

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY_ID')
REGION = os.getenv('AWS_REGION')

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

dynamodb = session.resource('dynamodb')


def get_table(table_name):
    return dynamodb.Table(table_name)

def delete_table(table_name):
    table = get_table(table_name)
    table.delete()
    table.wait_until_not_exists()

def create_example_table():
    table = dynamodb.create_table(
        TableName='example',
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

    print(f"Table {table.table_name} created successfully with item count: {table.item_count}")



def set_example_user():
    table = get_table('example')
    table.put_item(
        Item={
            'username': 'example_user',
            'password': 'example_password',
            'email': 'example@example.com'
        }
    )


def get_example_user():
    table = get_table('example')
    key = {'email': 'example@example.com'}
    response = table.get_item(
        Key=key
    )

    item = response.get('Item')
    if item:
        print(f"User found: {item}")
    else:
        print("User not found")

if __name__ == '__main__':
    delete_table('example')
    create_example_table()
    set_example_user()
    get_example_user()






