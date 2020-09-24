[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# User Segmentation Service (Under Development)

### Introduction
 
The project provides a central repository for the microservice
which'll be used for segmenting user to segmatation groups based on predefined rules.
The project is written in Python, with MongoDB as the backbone database and
JSON as interim data layer.

### Setup

Since the project is entirely written in Python, you can use a virtual
environment to keep the dependencies same as the other fellow
developers. A virtual environment can be created/used as follows:

- Using `pip`; install `virtualenv` globally:

        $ sudo pip install virtualenv

- Once `virtualenv` is installed, create a new environment (named
    `user_segmentation`) here:

        $ virtualenv --python=python3 user_segmentation
 
- You can manually activate the environment using the following command:

        $ source user_segmentation/bin/acivate

- You can exit the environment by simply executing the `deactivate` command:

        $ deactivate



### Deployment

Once you've activated your virtual environment, you no longer need to
use `sudo` to install any dependencies. Simply use the environment's
local copy of `pip` and install all the required packages using the
`requirements.txt` file bundled along with the project:

    $ pip install -r requirements.txt

The above command shall read the dependencies from the
`requirements.txt` file line-by-line, and install the same version as
mentioned in the file. If you're using a new module for your project,
and want to add that to the `requirements.txt` list, simply use a
`freeze` command, and redirect the output to the file.

    $ pip freeze > requirements.txt

Simply run:

    $ python run_service.py
    
The service runs on port 7070


### Data Objects:

- UserObject:
```
{
    "_id": 10010,
    "name": "Asha1",
    "gender": "M",
    "preferences": {
        "meat": "redmeat"
    }
    "age": 20
}
```
- SementationObject:
```
{
    "segment_name": "segment_11",
    "segment_rule": {
        "or": [{
                "or": [{
                        "gender": {
                            "value": "F",
                            "op": "eq"
                        }
                    },
                    {
                        "gender": {
                            "value": "M",
                            "op": "eq"
                        }
                    }
                ]
            },
            {
                "or": [{
                        "and": [{
                                "gender": {
                                    "value": "F",
                                    "op": "eq"
                                }
                            },
                            {
                                "gender": {
                                    "value": "F",
                                    "op": "eq"
                                }
                            }
                        ]
                    },
                    {
                        "age": {
                            "value": 15,
                            "op": "eq"
                        }
                    }
                ]
            }
        ]
    }
}
```

### Allowed Operators:
- "lt": LessThan()
- "lte": LessThanEqualTo()
- "gt": GreaterThan()
- "gte": GreaterThanEqualTo()
- "eq": EqualTo()
- "neq": NotEqualTo()

Other Operators can be added in utils/operators.py


### Allowed Conjunctors for combining results of evaluated expressions

- or
- and

Other Conjunctors can be added in utils/conjunctor_config.py


### Allowed Parameters for user fields to set rules on:

- "order_count"
- "creation_date"
- "user_type"
- "preference.food"
- "preference.price"
- "city"
- "user_category"
- "age"
- "gender"

The List can be extended in service/allowed_rule_params.yaml file

### APIs for interacting

#### User Related

- POST-  /user/
   - Used for Creating a new user
   - Payload
 ```
JSON 
  {
    "_id": 10010,
    "name": "Asha1",
    "gender": "M",
    "preferences": {
        "meat": "redmeat"
    }
    "age": 20
}
```

- GET - /user/{user_id}
  For Fetching user info from user_id

#### Segment Related

- POST - /segment/
    - For creating a new segment_rule
    - Payload:
```
JSON
{
    "segment_name": "segment_12",
    "segment_rule": {
        "or": [{
                "or": [{
                        "gender": {
                            "value": "F",
                            "op": "eq"
                        }
                    },
                    {
                        "gender": {
                            "value": "M",
                            "op": "eq"
                        }
                    }
                ]
            },
            {
                "or": [{
                        "and": [{
                                "gender": {
                                    "value": "F",
                                    "op": "eq"
                                }
                            },
                            {
                                "gender": {
                                    "value": "F",
                                    "op": "eq"
                                }
                            }
                        ]
                    },
                    {
                        "age": {
                            "value": 15,
                            "op": "eq"
                        }
                    }
                ]
            }
        ]
    }
}

```

- GET - /segment/{segment_id}/
    - For Getting the segment rule details corresponding to segment_id
    
#### Validation Related

- POST - /validate
    - To identify segments for a user_id corresponding to list of segment_ids ( with rules  stored in db )
    - Request Body:
  
  ```
  List - [user_id, [segment_ids]]
  ```



## Known Issues:

Following Functionalities still don't exist:

- Update in Existing User / Segmentation Rule
- Deleting Segmentation Rule/ User
- user json validation

