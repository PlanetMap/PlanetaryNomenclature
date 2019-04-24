import pytest
from unittest import mock
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Boolean, ForeignKey
from database import (Feature, Target, Continent, PagePart, ApprovalStatus, Ethnicity, FeatureType, 
    FeatureReference, System)

""" DB Function Tests """

@pytest.mark.parametrize("test_pagetype, test_pagename, expected_page", 
                            [('none', 'none', None)])
def test_pagepart_getpage(active_context, test_pagetype, test_pagename, expected_page):
    with active_context:
        assert PagePart.get_page('none', 'none') == expected_page

def test_target_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(Target.get_all()) >= minimum_result 

def test_target_get_approved(active_context):
    minimum_result = 2
    with active_context:
        assert len(Target.get_approved()) >= minimum_result

def test_approvalstatus_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(ApprovalStatus.get_all()) >= minimum_result

@pytest.mark.parametrize("test_input,expected_result", [('none', 0), ('Antarctica', 1)])
def test_continent_get_one(active_context, test_input, expected_result):
    with active_context:
        assert len(Continent.get_one(test_input)) == expected_result

def test_continent_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(Continent.get_all()) > minimum_result

def test_ethnicity_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(Ethnicity.get_all()) > minimum_result

def test_featurereference_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(FeatureReference.get_all()) > minimum_result

def test_featuretype_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(FeatureType.get_all()) > minimum_result

def test_system_get_all(active_context):
    minimum_result = 2
    with active_context:
        assert len(System.get_all()) > minimum_result


