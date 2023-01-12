# book-borrow-service
Rest APIs for borrowing books

# Setting up the service
## Setup Virtual Environment & Running the service

```shell
python3 -m venv djangoenv 
source djangoenv/bin/activate
pip install -r requirement.txt
python manage.py makemigrate
python manage.py runserver
```

# Documentation

## Models

### Book
#### This model is used to store details of books
```
book id - Primary Key
book name - CharaterField with max length 255
author - Foreign Key with Author Model
available - Boolean Field
type - Book Type choices from  (Paperbacks,Paperbacks,Handmade)
```
### Author
#### This model is used to store details of authors
```
id - Primary Key
name - Charayer Field with max length 255
```


### BookingHistory
#### This model is used to store details of booking history of books
```
id - Primary Key
book - Foreign Key with Book Model
user - Foreign Key with User Model
issue_time - Date time of issueing the book (Can't Modify after issuing)
return_time - Date time of returning the book
```

## APIs

### /all-books/
```
Request Type - `GET`
We support one params which is `author` which will be used to filter the book by author.
Default Filter - Availability of book
Response Body
[
    {
        id: <unique_id>,
        name: <book_name>,
        author: <author_name>,
        type: <book_type>
    },
    ...
]
Response Status - 200 OK

TestCases - 
1. If author params is not provided or empty string, all books should be returned.
2. Only available books should be returned.
3. If author params is provided then only books with that author should be returned.
4. If author provided is not present then return empty list of books.
```
### /borrow-book/<book-id>
```
Request Type - `PUT`
Response Status - 200 OK
TestCases - 
1. If book is not available then return 400 Bad Request.
2. If book id is not present then return 404 Not Found.
3. If book is available but locked for current user then return 400 Bad Request.
4. If book is available and unlocked then issue the book for logged in user and return 200 OK.
5. If user is try to book after locking time, user should be able to issue the book again.
```
### /return-book/<book-id>
```
Request Type - `PUT`
Response Status - 200 OK
TestCases - 
1. If book id is not present then return 404 Not Found.
2. If book is available then return 400 Bad Request.
3. If book is unavailable but logged in user is differnet than user who 
   issue the book then return 400 Bad request
4. If book is unavailable and logged in user is same as user who issue the book then 
   issue the return of book and return 200 OK.
```
### /next-borrow-time/<book-id>
```
Request Type - `GET`
Response Status - 200 OK
Response Body -
{
    blocked: Boolean,
    unblock_time : <datetime>
}
TestCases - 
1. If book id is not present then return 404 Not Found.
2. If book is booked by another user then return 400 Bad Request
3. If user is not issued given book then user can issue book
3. If book is available for current user then return blocked = False and current time 
4. if book is only unavailable for current user then return unblock time 
```