# service file for user related operations like creating user, fetching user details etc.

from app.models.user import User


def create_user(user_data):
    # logic to create user in database
    user = User(
        username=user_data.username, 
        email=user_data.email, 
        password=user_data.password
    )

    # save user to database and return user details
    return {"message": "User created successfully", "user": user.username}
    
# logic to fetch user details from database using user_id
def get_user_details(user_id):
    # logic to fetch user details from database using user_id
    return {"message": f"User details for user_id: {user_id}"}