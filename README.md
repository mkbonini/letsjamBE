# Let's Jam - BE
The RESTful API for Let's Jam 

## Local Setup
Assuming you have a mac/unix machine with `postgres 14.5`, `python 3.10.8` and `pip 22.2.2` installed:
- run `pip3 install virtualenv` then `python3 -m venv env` to create a local environment for the project
- run `source env/bin/activate` to connect to your local environment
- `pip3 install -r requirements.txt` to install the required packages
- `python3 run.py` to start up the server. By default it will run on `http://localhost:8000`
- You're all set to start making some requests! 

<details>
  <summary><b> Database Schema </b></summary>
  <img width="667" alt="Database Schema" src="https://user-images.githubusercontent.com/16493270/197594695-d068d702-9a1b-472c-ab79-708b37f13686.png">
</details>

## Endpoints
<details>
  <summary><b> Show User </b> </summary>
  
```shell
Get https://letusjam.herokuapp.com/api/v1/users/1/
```
---
```
{
    "data": {
        "type": "user",
        "id": "1",
        "attributes": {
            "name": "Cory",
            "display_email": "test@test.com",
            "about": "All about me",
            "zipcode": "00001",
            "picture_url": "picture.jpg",
            "instruments": [
                {
                    "id": "1",
                    "name": "piano"
                },
                {
                    "id": "2",
                    "name": "guitar"
                }
            ],
            "needs_instruments": [
                {
                    "id": "1",
                    "name": "piano"
                },
                {
                    "id": "2",
                    "name": "guitar"
                }
            ],
            "genres": [
                {
                    "id": "1",
                    "name": "rock"
                },
                {
                    "id": "2",
                    "name": "jazz"
                }
            ]
        }
    }
}
```
  
</details>

<details>
  <summary><b>User Connections</b></summary>
  
```shell
GET https://letusjam.herokuapp.com/api/v1/users/2/connections
```
```
{
    "data": {
        "type": "user",
        "id": "2",
        "attributes": {
            "connections_pending": [
                {
                    "id": "3",
                    "name": "333CoryUpdate",
                    "about": "333All about me babyyy",
                    "picture_url": "333asjdlaj.jpg",
                    "instruments": [
                        {
                            "name": "guitar",
                            "id": "2"
                        }
                    ],
                    "needs_instruments": [],
                    "genres": [
                        {
                            "name": "rock",
                            "id": "1"
                        }
                    ]
                }
            ],
            "requests_pending": [],
            "connections": [
                {
                    "id": "1",
                    "name": "333CoryUpdate",
                    "display_email": "333test@test.com",
                    "about": "333All about me babyyy",
                    "zipcode": "00001 edit",
                    "picture_url": "333asjdlaj.jpg",
                    "instruments": [
                        {
                            "name": "piano",
                            "id": "1"
                        },
                        {
                            "name": "guitar",
                            "id": "2"
                        }
                    ],
                    "needs_instruments": [
                        {
                            "name": "piano",
                            "id": "1"
                        },
                        {
                            "name": "guitar",
                            "id": "2"
                        }
                    ],
                    "genres": [
                        {
                            "name": "rock",
                            "id": "1"
                        },
                        {
                            "name": "jazz",
                            "id": "2"
                        }
                    ]
                }
            ]
        }
    }
}
```

</details>

<details>
  <summary><b>Edit User</b></summary>
  
```shell
PATCH https://letusjam.herokuapp.com/api/v1/users/1/
Content-Type: application/json
Accept: application/json
body:
{
    "name": "Cory",
    "display_email": "email2@email.com",
    "picture_url": "anotherurl.com",
    "about": "about cory",
    "zipcode": "12345"
}
```
```
User updated
```

</details>

<details>
  <summary><b>Create User Connections</b></summary>
  
```shell
POST https://letusjam.herokuapp.com/api/v1/users/<user id>/connections/<friend id>
```
```
connection added
```

</details>

<details>
  <summary><b>Edit User Connections</b></summary>
  
```shell
PATCH https://letusjam.herokuapp.com/api/v1/users/<user id>/connections/<friend id>
Content-Type: application/json
Accept: application/json
body:
{
    "status": ["APPROVED", "REJECTED"]
}
```
```
connection updated
```

</details>



## Backend Team
  - **Michael Bonini** - *Turing Student* - [GitHub Profile](https://github.com/mkbonini) - [LinkedIn](https://www.linkedin.com/in/michael-bonini-187157131/)
  - **Cory Berthune** - *Turing Student* - [GitHub Profile](https://github.com/CoryBethune) - [LinkedIn](https://www.linkedin.com/in/cory-b-711b79178/)
  - **Gwendolyn Ruiz** - *Turing Student* - [GitHub Profile](https://github.com/gwen-marina) - [LinkedIn](https://www.linkedin.com/in/gwendolyn-ruiz-329064238/)
  - **Jared Hardinger** - *Turing Student* - [GitHub Profile](https://github.com/jaredhardinger) - [LinkedIn](https://www.linkedin.com/in/hardinger/)

  ## Frontend Team
  - **Maya Kappen** - *Turing Student* - [GitHub Profile](https://github.com/mayakappen) - [LinkedIn](https://www.linkedin.com/in/maya-kappen-64b97123b/)
  - **Ana Bennett** - *Turing Student* - [GitHub Profile](https://github.com/AnaBennett11) - [LinkedIn](https://www.linkedin.com/in/ana-bennett/)
  - **Emma Russell** - *Turing Student* - [GitHub Profile](https://github.com/nairnairnair) - [LinkedIn](https://www.linkedin.com/in/emma-mm-russell/)
