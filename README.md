# user_management_api
REST API to manage users and groups written with Flask and SQLAlchemy.  
The User resource has 3 fields: id, name, and email.  
The Group resource has 3 fields: id, name, and date_created.  
A User can have many Groups and a Group can have many Users.  
## Installation
1. git clone https://github.com/azflin/user_management_api
2. pip install -r requirements.txt  (Use a virtualenv)
3. python run.py --create_database  (Create the SQLite database)
4. python run.py  (Run server locally)  

## API Help
__/users/\<int:id\>__  
* GET: Return details of single user
* DELETE: Delete user
* PUT: Edit existing user. JSON payload must contain 'name' and/or 'email' key(s), ie {"name": "foo"}  

__/users__
* GET: If no query params, return list of users sorted alphabetically by name.
        If the query parameter 'sortByNumGroups=true' is sent, then return list of users and a
        number of groups that users belongs to, sorted by number of groups in ascending order.
* POST: Create a user. JSON payload must contain 'name' and 'email' keys, ie {"name": "foo", "email": "foo@foo.com"}  

__/groups/\<int:id\>__
* GET: Return details of single group
* DELETE: Delete a group
* PUT: Edit existing group. JSON payload must contain 'name', ie {"name": "bar"}  

__/groups__
* GET: If no query params, return list of groups sorted alphabetically by name.
    If the query parameter 'sortByNumUsers=true' is sent, then return list of groups and a
    number of users that group has, sorted by number of users in descending order.
* POST: Create a group. JSON payload must contain 'name' key, ie {"name": "bar"}  

__/users/\<int:id\>/groups__
* GET: Return groups of a single user  

__/groups/\<int:id\>/users__
* GET: Return users of a single group
* POST: Add or remove an existing user from group.
 * Add: Use JSON payload of {"add": \<user_id\>}, ie {"add": 1}
 * Remove: Use JSON payload of {"remove": \<user_id\>}, ie {"remove": 2}
