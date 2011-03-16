#!/usr/bin/env python
# -*- coding: utf-8 -*-

## all the methods you see called (as if by magic) are in here.
from helpers import *

"""Python wrapper for the Wordnik API. 

This API implements all the methods described at http://developer.wordnik.com/docs

maintainer: Robin Walsh (robin@wordnik.com)
"""

import json, urllib, urllib2
from optparse import OptionParser
from xml.etree import ElementTree
from pprint import pprint

DEFAULT_HOST   = "api.wordnik.com"
DEFAULT_URI    = "/v4"
DEFAULT_URL    = "http://" + DEFAULT_HOST + DEFAULT_URI
DEFAULT_FORMAT = "json"

class RestfulError(Exception):
    """Raised when response from REST API indicates an error has occurred."""

class InvalidRelationType(Exception):
    """Raised if Wordnik.related method is passed invalid relation type."""

class NoAPIKey(Exception):
    """Raised if we don't get an API key."""

class MissingParameters(Exception):
    """Raised if we try to call an API method with required parameters missing"""
    
class Wordnik(object):
    
    """
    A generic Wordnik object. Use me to interact with the Wordnik API.
    
    All of my methods can be called in multiple ways. All positional
    arguments passed into one of my methods (with the exception of "format")
    will be substituted for the correponding path parameter, if possible.
    For example, consider the "get_word_examples" method. The URI path is:
    
    /word.{format}/{word}/examples
    
    So we can skip format (default format is JSON) and infer that the first
    positional argument is the word we want examples for. Hence:
    
    Wordnik.word_get_examples('cat')
    
    All other (non-path) arguments are keyword arguments. The "format"
    paramater can be passed in this way as well. Hence:
    
    Wordnik.word_get_examples('cat', format='xml', limit=500)
    
    In the case where you're making a POST, you will need a "body" keyword:
    
    Wordnik.word_list_put(wordListId=1234, body="Some HTTP body")    
    """
    
    
    def __init__(self, api_key=None):
        """
        Initialize a Wordnik object. You must pass in an API key when
        you make a new Wordnik. We don't validate the API key until the
        first call against the API is made, at which point you'll find
        out if it's good."""
        
        if api_key is None:
            raise NoAPIKey("No API key passed to our constructor")
        
        self._api_key = api_key
        
        
    @classmethod
    def _populate_methods(klass):
        """This will create all the methods we need to interact with
        the Wordnik API"""
        
        import _methods
        resources = _methods.api_methods.keys()
        for resource in resources:
            Wordnik._create_methods(_methods.api_methods[resource])
    
    @classmethod
    def _create_methods(klass, jsn):
        """A helper method that will populate this module's namespace
        with methods (parsed directlly from the Wordnik API's output)
        """
        endpoints = jsn['endPoints']
    
        for method in endpoints:
            path = method['path']
            for op in method['operations']:
                summary = op['summary']
                httpmethod = op['httpMethod'].lower()
                params = op['parameters']
                response = op['response']
    
                ## a path like: /user.{format}/{username}/wordOfTheDayList/{permalink} (GET)
                ## will get translated into method: user_get_word_of_the_day_list
                methodName = normalize(path, httpmethod)
                        
                docs = generate_docs(params, response, summary, path)
                m = create_method(methodName, docs, dictify(params), path)
                setattr( Wordnik, methodName, m )
    
    def _run_command(self, command_name, *args, **kwargs):
        if 'api_key' not in kwargs:
            kwargs.update( {"api_key": self._api_key} )
        command = getattr(self, command_name)
        (path, headers, body) = process_args(command._path, command._params, args, kwargs)
        return _do_http(path, headers, body)
    
    def multi(self, calls, **kwargs):
        """Multiple calls, batched. This is a "special case" method
        in that it's not automatically generated from the API documentation.
        That's because, well, it's undocumented. Here's how you use it:
        
        Wordnik.multi( [call1, call2, call3 ], **kwargs)
        
        where each "call" is (word, resource, {param1: value1, ...} )
        So we could form a batch call like so:
        
        calls = [("dog","examples"),("cat","definitions",{"limit":500})]
        
        Wordnik.multi(calls, format="xml")
        
        """
        
        path = "/word.%s?multi=true" % (kwargs.get('format') or DEFAULT_FORMAT,)
        
        callsMade = 0
        for call in calls:
            word = call[0]
            resource = call[1]
            if len(call) >= 3:
                otherParams = call[2]
            else:
                otherParams = {}
            path += "&resource.{0}={1}/{2}".format(callsMade,word,resource)
            for key,val in otherParams.items():
                path += "&{0}.{1}={2}".format(key, callsMade, val)
            callsMade += 1
        
        headers = { "api_key": self._api_key }
        return _do_http(path, headers)
        
Wordnik._populate_methods()