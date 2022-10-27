![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Let's Jam - BE
The RESTful API for Let's Jam 

[Visit the frontend repo](https://github.com/Let-s-Jam/letsjamFE)

[Deployed Site](https://letsjam.vercel.app/)

***

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

<details>
  <summary><b> Create, Drop, and Seed the Database </b></summary>

After Local Setup is complete:

- type `flask dbcreate` to create the database
- type `flask dbdrop` to drop the database
- type `flask dbseed` to seed the database
</details>

<details>
  <summary><b> Testing </b></summary>

After Local Setup is complete:

- type `pytest` to run tests
- type `coverage run -m pytest` to generate % coverage
- type `coverage report` to print the coverage report
</details>

***

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

<details>
  <summary><b> Search </b> </summary>
  
```shell
Get https://letusjam.herokuapp.com/api/v1/users/1/search?radius=50&instrument=theremin
Optional Query Params: radius, name, instrument, genre
```
---
```
{
    "data": [
        {
            "type": "user",
            "id": "9",
            "attributes": {
                "name": "Bory Cethune",
                "about": "!!!MOAR COWBELL!!!",
                "picture_url": "https://user-images.githubusercontent.com/98188684/197365266-ac37398a-f168-4768-8476-5e36b9a068aa.png",
                "instruments": [
                    {
                        "name": "Piano",
                        "id": "2"
                    },
                    {
                        "name": "Theremin",
                        "id": "9"
                    }
                ],
                "needs_instruments": [],
                "genres": [
                    {
                        "name": "Rock",
                        "id": "2"
                    }
                ],
                "distance": 0.0,
                "connection_status": "nun"
            }
        },
        {
            "type": "user",
            "id": "8",
            "attributes": {
                "name": "Hared Jardinger",
                "about": "Classically trained baroque pianist who is baroque. :') I need some gigs y'all. ",
                "picture_url": "https://user-images.githubusercontent.com/98188684/197365099-0e35cd61-7448-4e62-9005-087404014c99.png",
                "instruments": [
                    {
                        "name": "Guitar",
                        "id": "1"
                    },
                    {
                        "name": "Piano",
                        "id": "2"
                    },
                    {
                        "name": "Drums",
                        "id": "3"
                    },
                    {
                        "name": "Flute",
                        "id": "4"
                    },
                    {
                        "name": "Clarinet",
                        "id": "5"
                    },
                    {
                        "name": "Bass",
                        "id": "6"
                    },
                    {
                        "name": "Triangle",
                        "id": "7"
                    },
                    {
                        "name": "Cowbell",
                        "id": "8"
                    },
                    {
                        "name": "Theremin",
                        "id": "9"
                    },
                    {
                        "name": "Saxophone",
                        "id": "10"
                    }
                ],
                "needs_instruments": [],
                "genres": [
                    {
                        "name": "Rock",
                        "id": "2"
                    },
                    {
                        "name": "Jazz",
                        "id": "10"
                    }
                ],
                "distance": 13.54047013081921,
                "connection_status": "pending"
            }
        },
        {
            "type": "user",
            "id": "7",
            "attributes": {
                "name": "Bichael Monini",
                "about": "Music is my life </3",
                "picture_url": "https://user-images.githubusercontent.com/98188684/197365068-74fc732a-eb69-4a45-826c-6ff39a0af77d.png",
                "instruments": [
                    {
                        "name": "Theremin",
                        "id": "9"
                    }
                ],
                "needs_instruments": [],
                "genres": [
                    {
                        "name": "Pop",
                        "id": "1"
                    },
                    {
                        "name": "Rock",
                        "id": "2"
                    },
                    {
                        "name": "Blues",
                        "id": "3"
                    },
                    {
                        "name": "Electronic",
                        "id": "4"
                    },
                    {
                        "name": "Jam",
                        "id": "5"
                    },
                    {
                        "name": "Rap",
                        "id": "6"
                    },
                    {
                        "name": "Indie",
                        "id": "7"
                    },
                    {
                        "name": "Americana",
                        "id": "8"
                    },
                    {
                        "name": "Folk",
                        "id": "9"
                    },
                    {
                        "name": "Jazz",
                        "id": "10"
                    }
                ],
                "distance": 15.563325869097204,
                "connection_status": "nun"
            }
        },
        {
            "type": "user",
            "id": "1",
            "attributes": {
                "name": "Bna Aennett",
                "about": "I love Angular!",
                "picture_url": "https://user-images.githubusercontent.com/98188684/197364951-4468b500-d855-4436-adad-5f46ccf363f0.png",
                "instruments": [
                    {
                        "name": "Theremin",
                        "id": "9"
                    }
                ],
                "needs_instruments": [],
                "genres": [
                    {
                        "name": "Rock",
                        "id": "2"
                    }
                ],
                "distance": 22.93208462415554,
                "connection_status": "nun"
            }
        }
    ]
}
```
  </details>

***

## Backend Team
  - **Michael Bonini** - *Turing Student* - [GitHub Profile](https://github.com/mkbonini) - [LinkedIn](https://www.linkedin.com/in/michael-bonini-187157131/)
  - **Cory Berthune** - *Turing Student* - [GitHub Profile](https://github.com/CoryBethune) - [LinkedIn](https://www.linkedin.com/in/cory-b-711b79178/)
  - **Gwendolyn Ruiz** - *Turing Student* - [GitHub Profile](https://github.com/gwen-marina) - [LinkedIn](https://www.linkedin.com/in/gwendolyn-ruiz-329064238/)
  - **Jared Hardinger** - *Turing Student* - [GitHub Profile](https://github.com/jaredhardinger) - [LinkedIn](https://www.linkedin.com/in/hardinger/)

  ## Frontend Team
  - **Maya Kappen** - *Turing Student* - [GitHub Profile](https://github.com/mayakappen) - [LinkedIn](https://www.linkedin.com/in/maya-kappen-64b97123b/)
  - **Ana Bennett** - *Turing Student* - [GitHub Profile](https://github.com/AnaBennett11) - [LinkedIn](https://www.linkedin.com/in/ana-bennett/)
  - **Emma Russell** - *Turing Student* - [GitHub Profile](https://github.com/nairnairnair) - [LinkedIn](https://www.linkedin.com/in/emma-mm-russell/)
