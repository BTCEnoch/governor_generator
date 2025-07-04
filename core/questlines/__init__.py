"""
Core Questlines System
Autonomous questline generation by governors

This module provides the infrastructure for governors to create their own
questlines, events, and encounters dynamically.
"""

from .questline_builder import QuestlineBuilder
from .event_generator import EventGenerator
from .encounter_system import EncounterSystem

__all__ = [
    'QuestlineBuilder',
    'EventGenerator', 
    'EncounterSystem'
]

__version__ = '1.0.0'
__author__ = 'Enochian Governor Generation Project'
