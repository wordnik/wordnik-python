#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Python wrapper for the Wordnik API. 

This API implements all the methods described at http://developer.wordnik.com/docs

maintainer: Robin Walsh (robin@wordnik.com)
"""

import json, re, sys, urllib, urllib2
from optparse import OptionParser
from xml.etree import ElementTree
from pprint import pprint


class RestfulError(Exception):
    """Raised when response from REST API indicates an error has occurred."""

class InvalidRelationType(Exception):
    """Raised if Wordnik.related method is passed invalid relation type."""

class NoAPIKey(Exception):
    """Raised if we don't get an API key."""

class MissingParameters(Exception):
    """Raised if we try to call an API method with required parameters missing"""
    
DEFAULT_HOST = "api.wordnik.com"
DEFAULT_URI  = "/v4"
DEFAULT_URL  = "http://" + DEFAULT_HOST + DEFAULT_URI

def generate_docs(params):
    docstring = ""
    for param in params:
        name = param.get('name') or 'body'
        summary = param.get('summary')
        paramType = param.get('type')
        required = "required" if param.get('required') else "optional"
        allowable = param.get('allowableValues')
        paramDoc = "{0} ({1}): {2}\n".format(name, required, paramType)
        paramDoc += "{0}\n".format(summary)
        docstring += paramDoc
    return docstring
        
    
class Wordnik(object):
    
    def __init__(self, api_key=None):
        if api_key is None:
            raise NoAPIKey("No API key passed to our constructor")
        
        self.__api_key = api_key
        
        import _methods
        self.populate_methods(_methods.api_methods)
        

    def populate_methods(self, wordnik_api_methods):
        """This will create all the methods we need to interact with the Wordnik API"""
        resources = wordnik_api_methods.keys()
        for resource in resources:
            self._create_methods(wordnik_api_methods[resource])
    
    @staticmethod
    def _convert(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def _normalize(path, method):
        param_re = re.compile('{[\w]+}')
        under_re = re.compile('(^[_]+|[_]+$)')
        un_camel_re = re.compile('[a-z]([A-Z])')
        repeat_under_re = re.compile('[_]+')
        
        p = method + '_' + path.replace('/', '_').replace('.', '_')
        p = param_re.subn('', p)[0]
        p = under_re.subn('', p)[0]
        p = repeat_under_re.subn('_', p)[0]
        return Wordnik._convert(p)
        
    def _create_methods(self, jsn):
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

                methodName = Wordnik._normalize(path, httpmethod)
                ## a path like: /user.{format}/{username}/wordOfTheDayList/{permalink} (GET)
                ## will get translated into method: get_user_word_of_the_day_list

                wm = WordnikMethod(methodName)
                wm.setMethodParams(params)
                wm.setMethodPath(path)
                wm.setApiKey(self.__api_key)
                docs = generate_docs(params)
                wm.__doc__ = docs
                setattr( Wordnik, methodName, wm )
            
     
          
class WordnikMethod(object):
    
    """
    A generic Wordnik HTTP method
    """
    
    positional_args_re = re.compile('{([\w]+)}')
    DEFAULT_FORMAT  = 'json'
    
    def __init__(self, name, key=None):
        self.name    = name
        self.key     = key
        self.params  = dict()
        
        self.path    = None
        self.body    = None
        self.headers = dict()
        
        
    def __call__(self, *args, **kwargs):
        (path, headers, body) = self._processArgs(args, kwargs)
        self.findMissingPathParams(path)
        return self._do_http(path, headers, body, self.key)
        
    def findMissingPathParams(self, path):
        """This will check to make sure there are no un-substituted params
        e.g. /word.json/{word}
        """
        if self.positional_args_re.search(path):
            matches = self.positional_args_re.findall(path)
            missingParams = ", ".join(matches)
            raise MissingParameters("Could not substitute some parameters: {0}".format(missingParams))
        
        
    def setMethodPath(self, path):
        """Set the API path for this method"""
        self.path = path

    def setMethodParams(self, params):
        """Set parameters for this method"""
        for param in params:
            if 'name' in param:
                self.params[param['name']] = param
            else:
                self.params['body'] = param
    
    def setApiKey(self, key):
        """Set the API key"""
        self.key = key
    
    @staticmethod
    def _do_http(uri, headers, body, key):
        """This wraps the HTTP call. This may get factored out in the future."""
        url = DEFAULT_URL + uri
        if 'api_key' not in headers:
            headers.update( {'api_key': key} )
        request = urllib2.Request(url, body, headers)
        return urllib2.urlopen(request).read()
        
        
    def _processArgs(self, args, kwargs):
        """This does all the path substitution and the population of the
        headers and/or body, based on positional and keyword arguments.
        """
        ## get "{format} of of the way first"
        format = kwargs.get('format') or self.DEFAULT_FORMAT
        path = self.path.replace('{format}', format) + "?"
        
        ## substiture the positional arguments, left-to-right
        for arg in args:
            path = self.positional_args_re.sub(arg, path, count=1)
        
        ## now look through the keyword args and do path substitution
        for arg,value in kwargs.items():
            if arg not in path:
                continue
            bracketedString = "{" + arg + "}"
            pathPattern = re.compile(bracketedString)
            path = pathPattern.sub(value, path)
            ## we want to remove this item from kwargs (we already used it!)
            kwargs.pop(arg)
        
        ## if we need to set the HTTP body, we do it in kwargs
        if 'body' in kwargs:
            self.body = urllib.urlencode(kwargs.pop('body'))
            
        ## handle additional query and header args
        for arg in kwargs:
            if arg in self.params and self.params[arg]['paramType'] == 'query':
                path += "{0}={1}&".format(arg, kwargs[arg])
            else:
                self.headers[arg] = kwargs[arg]
        
        ## return a 3-tuple of (<URI path>, <headers>, <body>)
        return (path, self.headers, self.body)
        
        
        
