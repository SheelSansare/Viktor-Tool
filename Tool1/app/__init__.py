"""
This file is the entry point for your application and is used to:

    - Define all entity-types that are part of the app, and
    - Create 1 or more initial entities (of above type(s)), which are generated upon starting the app

For more information about this file, see: https://docs.viktor.ai/docs/guides/fundamentals/app-init-file
"""

# Creates an entity-type MyFolder and imports the Controller from my_folder -> controller.py
from .my_folder.controller import Controller as MyFolder

# Creates an entity-type MyEntityType and imports the Controller from my_entity_type -> controller.py
from .my_entity_type.controller import Controller as MyEntityType

# Import the InitialEntity object to create initial entities
from viktor import InitialEntity

# Create the initial entities. At least 1 top folder must be created as a starting point for the user.
# In this case also a 'Demo' is initialized as a child under 'My Folder'. Note that "children = ['MyEntityType']" 
# is defined on MyFolder Controller to enable this.
initial_entities = [
    InitialEntity('MyFolder', name='My Folder', children=[
        InitialEntity('MyEntityType', name='Demo', params='my_entity.json')  # predefined entity properties from a .json file.
    ])
]
