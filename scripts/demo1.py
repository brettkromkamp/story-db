"""
Demo 1: procedural narrative definition script. Part of the StoryTechnologies project.

August 18, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)

Narrative structure

    Events
        Weigh Station (event 1)
            Participants
                Foreman (participant 1)
            Things
                Merchandise (thing 1)
        Warehouse (event 2)
            Participants
                Foreman (participant 1)
            Things
                Merchandise (thing 1)
        Docks
            Participants
                Foreman (participant 1)
                Captain (participant 2)
            Things
                Coffee Beans Merchandise (thing 1)
                Electronics Merchandise (thing 2)

    Temporal
        Weigh Station (cause) -> Warehouse (effect)
        Warehouse (cause) -> Docks (effect)

    Spatial
        Weigh Station [sign 1] -> Warehouse
        Warehouse [sign 1] -> Weigh Station
        Warehouse [sign 2] -> Docks
        Docks [sign 1] -> Warehouse
"""

import configparser
import os

from storydb.core.models.event import Event
from storydb.core.models.participant import Participant
from storydb.core.models.place import Place
from storydb.core.models.resource import Resource
from storydb.core.models.thing import Thing
from storydb.core.store.storystore import StoryStore

MAP_IDENTIFIER = 4
USER_IDENTIFIER = 1
SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "../settings.ini")
RESOURCES_SOURCE_DIRECTORY = "/home/brettk/Source/story-technologies/resources"
RESOURCES_DESTINATION_DIRECTORY = "/home/brettk/Source/story-technologies/resources"

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

database_username = config["DATABASE"]["Username"]
database_password = config["DATABASE"]["Password"]
database_name = config["DATABASE"]["Database"]

# Instantiate and open the story store
story_store = StoryStore(database_username, database_password, dbname=database_name)
story_store.source_directory = RESOURCES_SOURCE_DIRECTORY
story_store.destination_directory = RESOURCES_DESTINATION_DIRECTORY
story_store.open()

story_store.initialise(MAP_IDENTIFIER, USER_IDENTIFIER)

# ========== PARTICIPANTS AND THINGS ==========

participant1 = Participant(
    "foreman",
    "The Foreman",
    description="A supervisor, or also known as foreman, overseer, facilitator, monitor, area coordinator, or sometimes gaffer, is the job title of a low level management position that is primarily based on authority over a worker or charge of a workplace.",
)
participant1.add_resource(Resource("3d-scene", reference="foreman.glb"))

thing1 = Thing(
    "merchandise-1",
    "Coffee Beans",
    description="A coffee bean is a seed of the coffee plant and the source for coffee. It is the pit inside the red or purple fruit often referred to as a cherry.",
)
thing1.add_resource(Resource("3d-scene", reference="merchandise.glb"))
thing1.add_resource(Resource("image", reference="coffee-beans.jpg"))
thing1.add_tag("merchandise")

participant2 = Participant(
    "captain",
    "The Captain",
    description="A sea captain, ship's captain, captain, master, or shipmaster, is a high-grade licensed mariner who holds ultimate command and responsibility of a merchant vessel.",
)
participant2.add_resource(Resource("3d-scene", reference="captain.glb"))

thing2 = Thing(
    "merchandise-2",
    "Electronics",
    description="Electronics comprises the physics, engineering, technology and applications that deal with the emission, flow and control of electrons in vacuum and matter.",
)
thing2.add_resource(Resource("3d-scene", reference="merchandise.glb"))
thing2.add_tag("merchandise")

# ========== PLACES ==========

place1 = Place(
    "weigh-station-place",
    "The Weigh Station",
    description="A weigh station is a checkpoint ...",
)
place1.add_resource(Resource("3d-scene", reference="weigh-station-place.glb"))
place1.add_resource(Resource("audio", reference="suspense.ogg"))

place2 = Place(
    "warehouse-place",
    "The Warehouse",
    description="A warehouse is a building for storing goods ...",
)
place2.add_resource(Resource("3d-scene", reference="warehouse-place.glb"))

place3 = Place(
    "docks-place",
    "The Docks",
    description="A dock is the area of water between or next to one or a group of human-made structures that are involved in the handling of boats or ships or such structures themselves.",
)
place3.add_resource(Resource("3d-scene", reference="docks-place.glb"))
place3.auto_rotate = True
place3.view_labels = True

# ========== EVENTS ==========

event10 = Event("weigh-station", "Weighing", rank=10, name="Weigh-Station")
event10.description = "The weighing of goods ..."
event10.add_participant(participant1)
event10.add_thing(thing1)
event10.where = place1

# ----- SUB-EVENTS -----
event11 = Event(
    "weigh-station-participant", "Participant at the Weigh-Station", rank=11, name="Weigh-Station Participant"
)
event11.description = "A participant is present at the Weight-Station event ..."
event11.add_participant(participant1)

event12 = Event("weigh-station-thing", "Thing at the Weigh-Station", rank=12, name="Weigh-Station Thing")
event12.description = "A thing is present at the Weight-Station event ..."
event12.add_thing(thing1)
# ----- SUB-EVENTS -----

event10.add_event(event11)
event10.add_event(event12)

story_store.set_event(MAP_IDENTIFIER, event10)

event20 = Event("warehouse", "Storing", rank=20, name="Warehouse")
event20.description = "The storing of goods ..."
event20.add_participant(participant1)
event20.add_thing(thing1)
event20.where = place2
story_store.set_event(MAP_IDENTIFIER, event20)

event30 = Event("docks", "Shipping", rank=30, name="Docks")
event30.description = "The shipping of goods ..."
event30.add_participant(participant1)
event30.add_participant(participant2)
event30.add_thing(thing1)
event30.add_thing(thing2)
event30.where = place3
story_store.set_event(MAP_IDENTIFIER, event30)

# ========== CONNECTIONS ==========

story_store.set_temporal_connection(MAP_IDENTIFIER, "weigh-station", "warehouse")
story_store.set_temporal_connection(MAP_IDENTIFIER, "warehouse", "docks")

story_store.set_spatial_connection(MAP_IDENTIFIER, "weigh-station-place", "warehouse", "sign-1")
story_store.set_spatial_connection(MAP_IDENTIFIER, "warehouse-place", "weigh-station", "sign-1")
story_store.set_spatial_connection(MAP_IDENTIFIER, "warehouse-place", "docks", "sign-2")
story_store.set_spatial_connection(MAP_IDENTIFIER, "docks-place", "warehouse", "sign-1")

# Clean-up resources
story_store.close()
