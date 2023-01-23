# Test Apartment

## Installation

In order to launch the project, You just need to have docker-compose installed on your computer.
You just need to run the following script :

```bash
  docker-compose up --build
```

It will launch the application with its postgres database.

You will then be able to access the swagger of the API from the following URL : [API URL](http://0.0.0.0:43122)


## Technical choices

For the test I chosed to create a table from the csv file with apartment rent.
I used SQLModel ORM which is an ORM developed by the creator of Fastapi which is wrap of Pydantic and SQLAlchemy.

I have two requirements files, one with all the dependencies needed to run the application, and also one with linter and tests packages.


## Acknowledgements

Thank you for reviewing what I did !