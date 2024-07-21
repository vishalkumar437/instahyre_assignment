# InstaHire Assignment
REST api to be consumed by a mobile app, which is somewhat similar to various popular apps
which tell you if a number is spam, or allow you to find a person’s name by searching for their phone
number.

# Requirements

For authentication, JWT (JSON Web Token) is utilized, following the REST framework guide. Additionally, other essential Django packages are required for the project's functionality. which can be installed from requirements.txt


# Run 
    ```
    pip install -r requirements.txt
    ```
    ```
    python manage.py makemigrations user
    ```
    ```
    python manage.py makemigrations contact_spam
    ```
    ```
    python manage.py runserver
    ```

# Or Run through docker
    ```
    docker build -t assignment .
    ```
# Run docker image
    ```
    docker run -p 8000:8000 --name assignment_container assignment
    ```

## Main URLs

- **Admin Interface**: Accessible via `/admin/`, this URL is linked to Django's default admin interface.
- **User API**: The base URL for user-related API endpoints is `/api/v1/user/`. It includes further URL configurations from the `user.api.urls`.
- **Contact Spam API**: For handling contact and spam-related requests, the base URL is `/api/v1/contact/`. It includes additional URL configurations from `contact_spam.api.urls`.

## User API URLs (`user.api.urls`)

- **Register**: A user can register by accessing `/register`. This endpoint is connected to the `RegisterUserView`.
- **Login**: For user login, the endpoint `/login` is used, which is linked to the `LoginUserView`.

## Contact Spam API URLs (`contact_spam.api.urls`)

- **Search by Name**: To search contacts by name, the endpoint `/searchByName` is used. It is served by the `ContactSearchByName` view.
- **Report Spam**: Users can report spam by accessing `/reportSpam`. This action is handled by the `ReportSpamByPhone` view.
- **Search by Phone**: For searching contacts by phone number, the endpoint `/searchByPhone/<str:query_param>` is available. It is managed by the `SearchByPhone` view.


