"""
StoryStore class. Part of the StoryTechnologies project.

August 16, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from __future__ import annotations
from storydb.core.models.narrative import Narrative

import os
import shutil
from datetime import datetime
from typing import Optional, List, Set, Dict

from topicdb.core.models.association import Association  # type: ignore
from topicdb.core.models.attribute import Attribute  # type: ignore
from topicdb.core.models.datatype import DataType  # type: ignore
from topicdb.core.models.occurrence import Occurrence  # type: ignore
from topicdb.core.models.topic import Topic  # type: ignore
from topicdb.core.store.retrievalmode import RetrievalMode  # type: ignore
from topicdb.core.store.taxonomymode import TaxonomyMode  # type: ignore
from topicdb.core.store.topicfield import TopicField  # type: ignore
from topicdb.core.store.topicstore import TopicStore  # type: ignore

from storydb.core.storydberror import StoryDbError
from storydb.core.models.entity import Entity
from storydb.core.models.event import Event
from storydb.core.models.participant import Participant
from storydb.core.models.path import Path
from storydb.core.models.place import Place
from storydb.core.models.resource import Resource
from storydb.core.models.tag import Tag
from storydb.core.models.thing import Thing
from storydb.core.models.timeinterval import TimeInterval
from storydb.core.store.resolvemode import ResolveMode


class StoryStore:
    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "storydb",
        source_directory: str = None,
        destination_directory: str = None,
    ) -> None:
        self.topic_store = TopicStore(username, password, host, port, dbname)
        self.source_directory = source_directory
        self.destination_directory = destination_directory

    def open(self) -> StoryStore:
        self.topic_store.open()
        return self

    def close(self) -> None:
        self.topic_store.close()

    @staticmethod
    def to_boolean(value):
        if isinstance(value, str) and value:
            if value.lower() in ["true", "t", "1"]:
                return True
            elif value.lower() in ["false", "f", "0"]:
                return False
        raise StoryDbError(f"The [{value}] is not recognized as a boolean value")

    # ========== CONTEXT MANAGER ==========

    def __enter__(self) -> StoryStore:
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ========== ENTITY ==========

    # Persist participant, thing, place and event entities
    def set_entity(self, map_identifier: int, entity: Entity, event_identifier: str = None) -> None:
        if (self.source_directory is None) or (self.destination_directory is None):
            raise StoryDbError("Missing resource directories")

        if not self.topic_store.topic_exists(map_identifier, entity.identifier):
            topic = Topic(entity.identifier, entity.instance_of, entity.name)
            timestamp = str(datetime.now())
            modification_attribute = Attribute(
                "modification-timestamp",
                timestamp,
                topic.identifier,
                data_type=DataType.TIMESTAMP,
            )
            self.topic_store.set_topic(map_identifier, topic)
            self.topic_store.set_attribute(map_identifier, modification_attribute)

            if hasattr(entity, "description") and entity.description:
                text_occurrence = Occurrence(
                    instance_of="text",
                    topic_identifier=entity.identifier,
                    resource_data=entity.description,
                )
                self.topic_store.set_occurrence(map_identifier, text_occurrence)
            if hasattr(entity, "animation") and entity.animation:
                entity.add_attribute(
                    Attribute(
                        "animation",
                        entity.animation,
                        entity.identifier,
                        data_type=DataType.STRING,
                    )
                )

            # Create the file directory for this topic map and topic if it doesn't already exist
            file_directory = os.path.join(self.destination_directory, str(map_identifier), entity.identifier)
            if not os.path.isdir(file_directory):
                os.makedirs(file_directory)

            for resource in entity.resources:
                occurrence = Occurrence(
                    instance_of=resource.instance_of,
                    topic_identifier=entity.identifier,
                    resource_ref=resource.reference,
                    resource_data=resource.data,
                )
                title_attribute = Attribute(
                    "title",
                    resource.title,
                    occurrence.identifier,
                    data_type=DataType.STRING,
                )
                self.topic_store.set_occurrence(map_identifier, occurrence)
                self.topic_store.set_attribute(map_identifier, title_attribute)

                # Copy resource file to appropriate (topic) directory
                if occurrence.resource_ref:
                    source_file_path = os.path.join(self.source_directory, occurrence.resource_ref)
                    destination_file_path = os.path.join(
                        self.destination_directory,
                        str(map_identifier),
                        entity.identifier,
                        occurrence.resource_ref,
                    )
                    if not os.path.isfile(destination_file_path):
                        shutil.copy(source_file_path, destination_file_path)

            if hasattr(entity, "tags"):
                self.topic_store.set_tags(map_identifier, entity.identifier, entity.tags)

            self.topic_store.set_attributes(map_identifier, entity.attributes)

        if event_identifier:
            association = Association(
                instance_of=entity.instance_of,
                src_topic_ref=entity.identifier,
                dest_topic_ref=event_identifier,
                src_role_spec="included-in",
                dest_role_spec="includes",
            )
            self.topic_store.set_association(map_identifier, association)

    # ========== PARTICIPANT ==========

    def get_participant(self, map_identifier: int, identifier: str) -> Optional[Participant]:
        result = None
        topic = self.topic_store.get_topic(
            map_identifier,
            identifier,
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
        )
        if topic:
            result = Participant(topic.identifier, topic.first_base_name.name)
            result.description = (
                topic.get_attribute_by_name("description").value if topic.get_attribute_by_name("description") else None
            )
            result.animation = (
                topic.get_attribute_by_name("animation").value if topic.get_attribute_by_name("animation") else None
            )

            occurrences = self.topic_store.get_topic_occurrences(map_identifier, identifier)
            for occurrence in occurrences:
                if occurrence.instance_of == "text":
                    text_data = self.topic_store.get_occurrence_data(map_identifier, occurrence.identifier)
                    result.add_resource(
                        Resource(
                            occurrence.instance_of,
                            reference=occurrence.resource_ref,
                            data=text_data,
                        )
                    )
                else:
                    result.add_resource(Resource(occurrence.instance_of, reference=occurrence.resource_ref))

            attributes = [
                attribute for attribute in topic.attributes if attribute.name not in ("description", "animation")
            ]
            result.add_attributes(attributes)

            result.add_tags(self.topic_store.get_tags(map_identifier, identifier))

        return result

    # ========== THING ==========

    def get_thing(self, map_identifier: int, identifier: str) -> Optional[Thing]:
        result = None
        topic = self.topic_store.get_topic(
            map_identifier,
            identifier,
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
        )
        if topic:
            result = Thing(topic.identifier, topic.first_base_name.name)
            result.description = (
                topic.get_attribute_by_name("description").value if topic.get_attribute_by_name("description") else None
            )
            result.animation = (
                topic.get_attribute_by_name("animation").value if topic.get_attribute_by_name("animation") else None
            )

            occurrences = self.topic_store.get_topic_occurrences(map_identifier, identifier)
            for occurrence in occurrences:
                if occurrence.instance_of == "text":
                    text_data = self.topic_store.get_occurrence_data(map_identifier, occurrence.identifier)
                    result.add_resource(
                        Resource(
                            occurrence.instance_of,
                            reference=occurrence.resource_ref,
                            data=text_data,
                        )
                    )
                else:
                    result.add_resource(Resource(occurrence.instance_of, reference=occurrence.resource_ref))

            attributes = [
                attribute for attribute in topic.attributes if attribute.name not in ("description", "animation")
            ]
            result.add_attributes(attributes)

            result.add_tags(self.topic_store.get_tags(map_identifier, identifier))
        return result

    # ========== PLACE ==========

    def get_place(self, map_identifier: int, identifier: str) -> Optional[Place]:
        result = None
        topic = self.topic_store.get_topic(
            map_identifier,
            identifier,
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
        )
        if topic:
            result = Place(topic.identifier, topic.first_base_name.name)
            result.description = (
                topic.get_attribute_by_name("description").value if topic.get_attribute_by_name("description") else None
            )
            result.animation = (
                topic.get_attribute_by_name("animation").value if topic.get_attribute_by_name("animation") else None
            )
            result.auto_rotate = (
                self.to_boolean(topic.get_attribute_by_name("auto-rotate").value)
                if topic.get_attribute_by_name("auto-rotate")
                else None
            )
            result.view_labels = (
                self.to_boolean(topic.get_attribute_by_name("view-labels").value)
                if topic.get_attribute_by_name("view-labels")
                else None
            )

            associations = self.topic_store.get_topic_associations(
                map_identifier,
                identifier,
                resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
            )

            for association in associations:
                if association.instance_of == "spatial-navigation":
                    destination_identifier = association.get_member_by_role("to").topic_refs[0]
                    if destination_identifier != identifier:
                        description = self.topic_store.get_topic(
                            map_identifier, destination_identifier
                        ).first_base_name.name
                        navigation_identifier = association.get_attribute_by_name("navigation-identifier").value
                        result.add_path(
                            Path(
                                navigation_identifier=navigation_identifier,
                                event_identifier=destination_identifier,
                                description=description,
                            )
                        )

            occurrences = self.topic_store.get_topic_occurrences(map_identifier, identifier)
            for occurrence in occurrences:
                if occurrence.instance_of == "text":
                    text_data = self.topic_store.get_occurrence_data(map_identifier, occurrence.identifier)
                    result.add_resource(
                        Resource(
                            occurrence.instance_of,
                            reference=occurrence.resource_ref,
                            data=text_data,
                        )
                    )
                else:
                    result.add_resource(Resource(occurrence.instance_of, reference=occurrence.resource_ref))

            attributes = [
                attribute
                for attribute in topic.attributes
                if attribute.name not in ("description", "animation", "auto-rotate", "view-labels")
            ]
            result.add_attributes(attributes)
        return result

    def set_place(self, map_identifier: int, place: Place, event_identifier: str = None) -> None:
        place.add_attribute(
            Attribute(
                "auto-rotate",
                place.auto_rotate,
                place.identifier,
                data_type=DataType.BOOLEAN,
            )
        )
        place.add_attribute(
            Attribute(
                "view-labels",
                place.view_labels,
                place.identifier,
                data_type=DataType.BOOLEAN,
            )
        )
        self.set_entity(map_identifier, place, event_identifier)

    # ========== EVENT ==========

    def get_event(
        self,
        map_identifier: int,
        identifier: str,
        resolve_sub_events: ResolveMode = ResolveMode.RESOLVE_SUB_EVENTS,
        resolve_causes: ResolveMode = ResolveMode.RESOLVE_CAUSES,
        resolve_effects: ResolveMode = ResolveMode.RESOLVE_EFFECTS,
        call_level: int = 0,
    ) -> Optional[Event]:
        result = None

        topic = self.topic_store.get_topic(
            map_identifier,
            identifier,
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
            resolve_occurrences=RetrievalMode.RESOLVE_OCCURRENCES,
        )
        if topic:
            rank = topic.get_attribute_by_name("rank").value

            # What?
            action_property = topic.get_attribute_by_name("action-property").value

            result = Event(
                topic.identifier,
                action_property,
                rank=int(rank),
                name=topic.first_base_name.name,
            )

            topic_occurrences = self.topic_store.get_topic_occurrences(
                map_identifier, identifier, inline_resource_data=RetrievalMode.INLINE_RESOURCE_DATA
            )
            for occurrence in topic_occurrences:
                if occurrence.instance_of == "text" and occurrence.resource_data:
                    result.description = occurrence.resource_data.decode()

            associations = self.topic_store.get_topic_associations(map_identifier, identifier)

            # Who, where, what and why?
            groups = self.topic_store.get_association_groups(map_identifier, identifier, associations=associations)
            if len(groups) > 0:
                for instance_of in groups.dict:
                    for role in groups.dict[instance_of]:
                        for topic_ref in groups[instance_of, role]:
                            if topic_ref == identifier:
                                continue
                            elif instance_of == "thing":
                                result.add_thing(self.get_thing(map_identifier, topic_ref))
                            elif instance_of == "participant":
                                result.add_participant(self.get_participant(map_identifier, topic_ref))
                            elif instance_of == "place":
                                result.where = self.get_place(map_identifier, topic_ref)
                            elif (
                                resolve_causes is ResolveMode.RESOLVE_CAUSES
                                and role == "cause"
                                and instance_of == "temporal-navigation"
                            ):
                                if call_level < 1:
                                    # Recursive call
                                    cause = self.get_event(map_identifier, topic_ref, call_level=call_level + 1)
                                    result.add_cause(cause)
                            elif (
                                resolve_effects is ResolveMode.RESOLVE_EFFECTS
                                and role == "effect"
                                and instance_of == "temporal-navigation"
                            ):
                                if call_level < 1:
                                    # Recursive call
                                    effect = self.get_event(map_identifier, topic_ref, call_level=call_level + 1)
                                    result.add_effect(effect)
                            elif (
                                resolve_sub_events is ResolveMode.RESOLVE_SUB_EVENTS
                                and role == "included-in"
                                and instance_of == "event"
                            ):
                                if call_level < 1:
                                    # Recursive call
                                    sub_event = self.get_event(map_identifier, topic_ref, call_level=call_level + 1)
                                    result.events[topic_ref] = sub_event

            # When?
            from_time_point = topic.get_attribute_by_name("from-time-point").value
            to_time_point = topic.get_attribute_by_name("to-time-point").value
            result.when = TimeInterval(from_time_point, to_time_point)

            for occurrence in topic.occurrences:
                if occurrence.instance_of == "text":
                    text_data = self.topic_store.get_occurrence_data(map_identifier, occurrence.identifier)
                    result.add_resource(
                        Resource(
                            occurrence.instance_of,
                            reference=occurrence.resource_ref,
                            data=text_data,
                        )
                    )
                else:
                    result.add_resource(Resource(occurrence.instance_of, reference=occurrence.resource_ref))

            attributes = [attribute for attribute in topic.attributes if attribute.name not in ("description")]
            result.add_attributes(attributes)

            # Tags-to-entities mapping
            result.entities_tags = self.get_entities_tags(map_identifier, identifier, associations=associations)

        return result

    def set_event(self, map_identifier: int, event: Event, parent_event: Event = None) -> None:
        if not self.topic_store.topic_exists(map_identifier, event.identifier):
            event.add_attribute(Attribute("rank", str(event.rank), event.identifier, data_type=DataType.NUMBER))

            # What?
            event.add_attribute(
                Attribute(
                    "action-property",
                    event.action_property,
                    event.identifier,
                    data_type=DataType.STRING,
                )
            )
            # When?
            if event.when is None:
                timestamp = str(datetime.now())
                event.when = TimeInterval(timestamp, timestamp)
            event.add_attribute(
                Attribute(
                    "from-time-point",
                    event.when.from_time_point,
                    event.identifier,
                    data_type=DataType.TIMESTAMP,
                )
            )
            event.add_attribute(
                Attribute(
                    "to-time-point",
                    event.when.to_time_point,
                    event.identifier,
                    data_type=DataType.TIMESTAMP,
                )
            )

            self.set_entity(map_identifier, event)

            # What?
            if parent_event:
                association = Association(
                    instance_of="event",
                    src_topic_ref=event.identifier,
                    dest_topic_ref=parent_event.identifier,
                    src_role_spec="included-in",
                    dest_role_spec="includes",
                )
                self.topic_store.set_association(map_identifier, association)

            for key, value in event.events.items():
                self.set_event(map_identifier, value, event)  # Recursive call

            # Who?
            for key, value in event.participants.items():
                self.set_entity(map_identifier, value, event.identifier)
            for key, value in event.things.items():
                self.set_entity(map_identifier, value, event.identifier)

            # Where?
            if event.where:
                self.set_place(map_identifier, event.where, event.identifier)

    # ========== TAG ==========

    def get_entities_tags(
        self,
        map_identifier: int,
        identifier: str,
        associations: Optional[List[Association]] = None,
    ) -> Dict[str, Set[str]]:
        result: Dict[str, Set[str]] = {}

        # Map from topics with tags to tags with topics. For example, the below topic -> tags mappings:
        # topic1 -> tag1, tag2, tag3
        # topic2 -> tag2, tag4
        # topic3 -> tag3, tag4, tag5
        # topic4 -> tag4, tag5, tag6, tag7
        # topic5 -> tag1, tag8
        #
        # Should become the following tag -> topics mappings:
        # tag1 -> topic1, topic5
        # tag2 -> topic1, topic2
        # tag3 -> topic1, topic3
        # tag4 -> topic2, topic3, topic4
        # tag5 -> topic3, topic4
        # tag6 -> topic4
        # tag7 -> topic4
        # tag8 -> topic5

        topic_tags = {}
        groups = self.topic_store.get_association_groups(map_identifier, identifier, associations=associations)
        if groups:
            for instance_of in groups.dict:
                for role in groups.dict[instance_of]:
                    for topic_ref in groups[instance_of, role]:
                        if topic_ref == identifier:
                            continue
                        if instance_of in ("participant", "thing"):
                            topic_tags[topic_ref] = self.topic_store.get_tags(map_identifier, topic_ref)

            for topic, tags in topic_tags.items():
                for tag in tags:
                    if tag not in result.keys():
                        result[tag] = {
                            topic
                        }  # Topics set. Will guarantee that topic identifiers are unique for each tag.
                    else:
                        result[tag].add(topic)
        return result

    def get_tag(self, map_identifier: int, identifier: str) -> Optional[Tag]:
        result = None

        topic = self.topic_store.get_topic(
            map_identifier,
            identifier,
            resolve_occurrences=RetrievalMode.RESOLVE_OCCURRENCES,
        )
        if topic:
            result = Tag(topic.identifier)
            for occurrence in topic.occurrences:
                if occurrence.instance_of == "text":
                    text_data = self.topic_store.get_occurrence_data(map_identifier, occurrence.identifier)
                    result.description = text_data
        return result

    # ========== TIMELINE ==========

    def get_timeline(self, map_identifier: int, event_identifier: str, timeline: List[Event] = None) -> List[Event]:
        if timeline is None:
            result = []
        else:
            result = timeline
        event = self.get_event(
            map_identifier,
            event_identifier,
            ResolveMode.DONT_RESOLVE_SUB_EVENTS,
            ResolveMode.RESOLVE_CAUSES,
        )
        result.append(event)

        # Recursive call
        for effect_identifier in event.effects.keys():
            self.get_timeline(map_identifier, effect_identifier, result)

        return result

    # ========== NARRATIVE ==========

    def get_narrative(
        self, map_identifier: int, event_identifier: str, description_identifier: str = "home"
    ) -> Optional[Narrative]:
        result = None
        topic = self.topic_store.get_topic(map_identifier, description_identifier)
        if topic:
            topic_occurrences = self.topic_store.get_topic_occurrences(
                map_identifier, description_identifier, inline_resource_data=RetrievalMode.INLINE_RESOURCE_DATA
            )
            description = ""
            for occurrence in topic_occurrences:
                if occurrence.instance_of == "text" and occurrence.resource_data:
                    if occurrence.resource_data:
                        description = occurrence.resource_data.decode()
            result = Narrative(topic.first_base_name.name, description)

            result.timeline = self.get_timeline(map_identifier, event_identifier)
            result.timeline = sorted(result.timeline, key=lambda event: event.rank)
        return result

    # ========== CONNECTION ==========

    def set_spatial_connection(
        self,
        map_identifier: int,
        source_identifier: str,
        destination_identifier: str,
        navigation_identifier: str,
    ) -> None:
        association = Association(
            instance_of="spatial-navigation",
            src_topic_ref=source_identifier,
            dest_topic_ref=destination_identifier,
            src_role_spec="from",
            dest_role_spec="to",
        )
        attribute = Attribute(
            "navigation-identifier",
            navigation_identifier,
            association.identifier,
            data_type=DataType.STRING,
        )
        self.topic_store.set_association(map_identifier, association)
        self.topic_store.set_attribute(map_identifier, attribute)

    def set_temporal_connection(self, map_identifier: int, source_identifier: str, destination_identifier: str) -> None:
        association = Association(
            instance_of="temporal-navigation",
            src_topic_ref=source_identifier,
            dest_topic_ref=destination_identifier,
            src_role_spec="cause",
            dest_role_spec="effect",
        )
        self.topic_store.set_association(map_identifier, association)

    # ========== MISCELLANEOUS ==========

    def initialise(self, map_identifier: int, user_identifier: int) -> None:
        base_topics = {
            ("event", "Event"),
            ("thing", "Thing"),
            ("participant", "Participant"),
            ("place", "Place"),
            ("included-in", "Included In"),
            ("includes", "Includes"),
            ("cause", "Cause"),
            ("effect", "Effect"),
            ("temporal-navigation", "Temporal Navigation"),
            ("spatial-navigation", "Spatial Navigation"),
            ("from", "From"),
            ("to", "To"),
        }

        for item in base_topics:
            topic = Topic(
                identifier=item[TopicField.IDENTIFIER.value],
                name=item[TopicField.BASE_NAME.value],
            )
            self.topic_store.set_topic(map_identifier, topic, TaxonomyMode.LENIENT)

        self.topic_store.initialise_topic_map(map_identifier, user_identifier)
