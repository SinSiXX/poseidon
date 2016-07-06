#!/usr/bin/env python
#
#   Copyright (c) 2016 In-Q-Tel, Inc, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
Rest module for PoseidonConfig. Delivers
settings from the poseidon configuration
file.

Created on 17 May 2016
@author: dgrossman, lanhamt
"""
import ConfigParser
import os
import json


config_template_path = '/tmp/poseidon/templates/config.template'


class FullConfig:
    """
    Provides the full configuration file in json dict string
    with sections as keys and their key-value pairs as values.
    """
    def __init__(self):
        self.modName = 'FullConfig'
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(config_template_path))

    def on_get(self, req, resp):
        try:
            ret = {}
            for sec in self.config.sections():
                ret[sec] = self.config.items(sec)
            resp.body = json.dumps(ret)
        except:
            resp.body = json.dumps("Failed to open config file.")


class SectionConfig:
    """
    Given a section name in the config file,
    returns a json list string of all the key-value
    pairs under that section.
    """
    def __init__(self):
        self.modName = 'SectionConfig'
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(config_template_path))

    def on_get(self, req, resp, section):
        try:
            ret_sec = self.config.items(section)
        except:
            ret_sec = "Failed to find section: " + section + " in config file."
        resp.body = json.dumps(ret_sec)


class FieldConfig:
    """
    Given a section and corresponding key in the config
    file, returns the value as a string.
    """
    def __init__(self):
        self.modName = 'FieldConfig'
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(config_template_path))

    def on_get(self, req, resp, section, field):
        """
        Requests should have a section of the config
        file and variable/field in that section to be
        returned in the response body.
        """
        resp.content_type = 'text/text'
        try:
            resp.body = self.config.get(section, field)
        except:
            resp.body = "Failed to find field: " + field + " in section: " + section + "."