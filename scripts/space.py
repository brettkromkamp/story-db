"""
Space Colony: procedural narrative definition script. Part of the StoryTechnologies project.

October 09, 2020
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


import configparser
import os

from storydb.core.models.event import Event
from storydb.core.models.participant import Participant
from storydb.core.models.place import Place
from storydb.core.models.resource import Resource
from storydb.core.models.thing import Thing
from storydb.core.store.storystore import StoryStore

MAP_IDENTIFIER = 11
USER_IDENTIFIER = 1
SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "../settings.ini")
RESOURCES_SOURCE_DIRECTORY = "/home/brettk/Source/story-technologies/resources/space-colony"
RESOURCES_DESTINATION_DIRECTORY = "/home/brettk/Source/story-technologies/resources/space-colony"

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

# ========== PARTICIPANTS ==========

participant1 = Participant(
    "engineer",
    "The Engineer",
    description="A person who designs, builds, or maintains engines, machines or structures.",
)
participant1.add_resource(Resource("3d-scene", reference="engineer.glb"))
participant1.add_tag("colonist")

participant2 = Participant(
    "foreman",
    "The Site Foreman",
    description="A supervisor, or also known as foreman, overseer, facilitator, monitor, area coordinator, or sometimes gaffer, is the job title of a low level management position that is primarily based on authority over a worker or charge of a workplace.",
)
participant2.add_resource(Resource("3d-scene", reference="foreman.glb"))
participant2.add_tag("colonist")

participant3 = Participant(
    "pilot",
    "The Pilot",
    description="An aircraft pilot or aviator is a person who controls the flight of an aircraft by operating its directional flight controls. Some other aircrew members, such as navigators or flight engineers, are also considered aviators, because they are involved in operating the aircraft's navigation and engine systems.",
)
participant3.add_resource(Resource("3d-scene", reference="pilot.glb"))
participant3.add_tag("colonist")

participant4 = Participant(
    "scientist",
    "The Scientist",
    description="A person who is studying or has expert knowledge of one or more of the natural or physical sciences.",
)
participant4.add_resource(Resource("3d-scene", reference="scientist.glb"))
participant4.add_tag("colonist")

# ========== THINGS ==========

thing1 = Thing(
    "airplane-1",
    "Reconnaissance aircraft",
    description="A reconnaissance aircraft is a military aircraft designed or adapted to perform aerial reconnaissance with roles including collection of imagery intelligence (including using photography), signals intelligence, as well as measurement and signature intelligence. Modern technology has also enabled some aircraft and UAVs to carry out real-time surveillance in addition to general intelligence gathering.",
)
thing1.add_resource(Resource("3d-scene", reference="airplane-1.glb"))
thing1.add_tag("transportation")

thing2 = Thing(
    "airplane-2",
    "Airplane",
    description="An airplane (informally plane) is a powered, fixed-wing aircraft that is propelled forward by thrust from a jet engine, propeller or rocket engine.",
)
thing2.add_resource(Resource("3d-scene", reference="airplane-2.glb"))
thing2.add_tag("transportation")

thing3 = Thing(
    "monorail",
    "Monorail",
    description="A monorail is a railway system in which the track consists of a single rail, typically elevated and with the trains suspended from it.",
)
thing3.add_resource(Resource("3d-scene", reference="monorail.glb"))
thing3.add_tag("transportation")

thing4 = Thing(
    "building-1",
    "Geology Building",
    description="A structure with a roof and walls, such as a house or factory.",
)
thing4.add_resource(Resource("3d-scene", reference="building-1.glb"))
thing4.add_tag("building")

thing5 = Thing(
    "building-2",
    "Processing Facilities",
    description="A structure with a roof and walls, such as a house or factory.",
)
thing5.add_resource(Resource("3d-scene", reference="building-2.glb"))
thing5.add_tag("building")

thing6 = Thing(
    "building-3",
    "Personnel Office",
    description="A structure with a roof and walls, such as a house or factory.",
)
thing6.add_resource(Resource("3d-scene", reference="building-3.glb"))
thing6.add_tag("building")

thing7 = Thing(
    "building-4",
    "Control and Monitoring",
    description="A structure with a roof and walls, such as a house or factory.",
)
thing7.add_resource(Resource("3d-scene", reference="building-4.glb"))
thing7.add_tag("building")

thing8 = Thing(
    "building-5",
    "Rocket Assembly Facility",
    description="A structure with a roof and walls, such as a house or factory.",
)
thing8.add_resource(Resource("3d-scene", reference="building-5.glb"))
thing8.add_tag("building")

thing9 = Thing(
    "building-6",
    "Employee Housing",
    description="A structure with a roof and walls, such as a house or factory.",
)
thing9.add_resource(Resource("3d-scene", reference="building-6.glb"))
thing9.add_tag("building")

thing10 = Thing(
    "air-defense-system",
    "Air Defense System",
    description='Anti-aircraft warfare or counter-air defence is the battlespace response to aerial warfare, defined by NATO as "all measures designed to nullify or reduce the effectiveness of hostile air action.',
)
thing10.add_resource(Resource("3d-scene", reference="air-defense-system.glb"))

thing11 = Thing(
    "communication-link",
    "Communication Link",
    description="A communications link is the communications channel that connects two or more communicating devices. This link may be an actual physical link or it may be a logical link that uses one or more actual physical links.",
)
thing11.add_resource(Resource("3d-scene", reference="communication-link.glb"))

thing12 = Thing(
    "rocket-assembly",
    "Rocket Assembly Operations",
    description="A multistage rocket, or step rocket, is a launch vehicle that uses two or more rocket stages, each of which contains its own engines and propellant. A tandem or serial stage is mounted on top of another stage; a parallel stage is attached alongside another stage. The result is effectively two or more rockets stacked on top of or attached next to each other. Two-stage rockets are quite common, but rockets with as many as five separate stages have been successfully launched.",
)
thing12.add_resource(Resource("3d-scene", reference="rocket-assembly.glb"))

thing13 = Thing(
    "rover",
    "Rover Vehicle",
    description="A rover is a motor vehicle that travels across the surface of the planet. Rovers have several advantages over stationary landers: they examine more territory, they can be directed to interesting features, they can place themselves in sunny positions to weather winter months, and they can advance the knowledge of how to perform very remote robotic vehicle control.",
)
thing13.add_resource(Resource("3d-scene", reference="rover.glb"))

# ========== PLACES ==========

place1 = Place(
    "industrial-sector-place",
    "The Industrial Sector",
    description="An industrial sector (also known as industrial park, industrial estate or trading estate) is an area zoned and planned for the purpose of industrial development.",
)
place1.add_resource(Resource("3d-scene", reference="industrial-sector.glb"))

place2 = Place(
    "research-sector-place",
    "The Research Sector",
    description='A science or research park (also called a "university research park", "technology park" or a "science and technology park" (STP)) is defined as being a property-based development that accommodates and fosters the growth of tenant firms and that is affiliated with a university (or a government and private research bodies) based on proximity, ownership, and/or governance.',
)
place2.add_resource(Resource("3d-scene", reference="research-sector.glb"))

place3 = Place(
    "colony-place",
    "The Colony",
    description="A colony is a territory under the immediate complete political control and occupied by settlers of a state, distinct from the home territory of the sovereign. For colonies in antiquity, city-states would often found their own colonies.",
)
place3.add_resource(Resource("3d-scene", reference="colony.glb"))
place3.auto_rotate = True
place3.view_labels = True

# ========== EVENTS ==========

event10 = Event("industrial-sector", "Construction and manufacturing", rank=10, name="The Industrial Sector")
event10.description = "The industrial area of the colony."
event10.add_participant(participant1)  # Engineer
event10.add_participant(participant2)  # Foreman
event10.add_thing(thing1)  # Airplane 1
event10.add_thing(thing3)  # Monorail
event10.add_thing(thing4)  # Building 1
event10.add_thing(thing5)  # Building 2
event10.add_thing(thing6)  # Building 3
event10.add_thing(thing7)  # Building 4
event10.where = place1
story_store.set_event(MAP_IDENTIFIER, event10)

event20 = Event(
    "research-sector", "Research and technological development", rank=20, name="The Research and Tech Sector"
)
event20.description = "The research and technology area of the colony."
event20.add_participant(participant3)  # Pilot
event20.add_participant(participant4)  # Scientist
event20.add_thing(thing2)  # Airplane 2
event20.add_thing(thing8)  # Building 5
event20.add_thing(thing9)  # Building 6
event20.add_thing(thing10)  # Air Defense System
event20.add_thing(thing11)  # Communication Link
event20.add_thing(thing12)  # Rocket Assembly Operations
event20.add_thing(thing13)  # Rover Vehicle
event20.where = place2

# ----- SUB-EVENTS -----
event21 = Event(
    "research-sector-rocket-assembly",
    "Rocket Assembly Operations in the Research Sector",
    rank=21,
    name="Rocket Assembly Operations",
)
event21.description = "A rocket is being assembled in the Research sector."
event21.add_thing(thing12)  # Rocket Assembly Operations
event20.add_event(event21)

story_store.set_event(MAP_IDENTIFIER, event20)

event30 = Event("colony", "The colonial settlement", rank=30, name="The Colony")
event30.description = "The colonial settlement."
event30.add_participant(participant1)  # Engineer
event30.add_participant(participant2)  # Foreman
event30.add_participant(participant3)  # Pilot
event30.add_participant(participant4)  # Scientist
event30.add_thing(thing1)  # Airplane 1
event30.add_thing(thing3)  # Monorail
event30.add_thing(thing4)  # Building 1
event30.add_thing(thing5)  # Building 2
event30.add_thing(thing6)  # Building 3
event30.add_thing(thing7)  # Building 4
event30.add_thing(thing2)  # Airplane 2
event30.add_thing(thing8)  # Building 5
event30.add_thing(thing9)  # Building 6
event30.add_thing(thing10)  # Air Defense System
event30.add_thing(thing11)  # Communication Link
event30.add_thing(thing12)  # Rocket Assembly Operations
event30.add_thing(thing13)  # Rover Vehicle
event30.where = place3
story_store.set_event(MAP_IDENTIFIER, event30)

# ========== CONNECTIONS ==========

story_store.set_temporal_connection(MAP_IDENTIFIER, "industrial-sector", "research-sector")
story_store.set_temporal_connection(MAP_IDENTIFIER, "research-sector", "colony")

story_store.set_spatial_connection(MAP_IDENTIFIER, "industrial-sector-place", "research-sector", "vehicle-1")
story_store.set_spatial_connection(MAP_IDENTIFIER, "research-sector-place", "industrial-sector", "vehicle-1")
story_store.set_spatial_connection(MAP_IDENTIFIER, "research-sector-place", "colony", "vehicle-2")
story_store.set_spatial_connection(MAP_IDENTIFIER, "colony-place", "research-sector", "vehicle-1")

# Clean-up resources
story_store.close()
