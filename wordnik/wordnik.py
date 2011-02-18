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

class Wordnik(object):
    
    FUNC_LOOKUP     = {}
    DEFAULT_FORMAT  = 'json'
    FORMATTERS      = {
                        'json': json.loads,
                        'xml':  ElementTree.fromstring,
                      }

    def __init__(self, api_key=None, format=DEFAULT_FORMAT, url=DEFAULT_URL):
        if api_key is None:
            raise NoAPIKey("No API key passed to our constructor")
        
        self.url     = url
        self.api_key = api_key

        import _methods
        self.populate_methods(_methods.api_methods)
        

    def populate_methods(self, wordnik_api_methods):
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
        endpoints = jsn['endPoints']

        for method in endpoints:
            path = method['path']
            for op in method['operations']:
                summary = op['summary']
                httpmethod = op['httpMethod'].lower()
                params = op['parameters']

            methodName = Wordnik._normalize(path, httpmethod)
            #print "{0} :: {1}".format(m, path)

            wm = WordnikMethod(methodName)
            wm.setMethodParams(params)
            wm.setMethodPath(path)
            wm.setApiKey(self.api_key)
            setattr( self, methodName, wm )
            
          
class WordnikMethod(object):
    
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
        if self.positional_args_re.search(path):
            matches = self.positional_args_re.findall(path)
            missingParams = ", ".join(matches)
            #print path
            raise MissingParameters("Could not substitute some parameters: {0}".format(missingParams))
        ## get args
        ## call http_get
        
    def setMethodPath(self, path):
        self.path = path

    def setMethodParams(self, params):
        for param in params:
            if 'name' in param:
                self.params[param['name']] = param
            else:
                self.params['body'] = param
    
    def setApiKey(self, key):
        self.key = key
    
    @staticmethod
    def _do_http(uri, headers, body, key):
        url = DEFAULT_URL + uri
        if 'api_key' not in headers:
            headers.update( {'api_key': key} )
        request = urllib2.Request(url, body, headers)
        return urllib2.urlopen(request).read()
        
        
    def _processArgs(self, args, kwargs):
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
            kwargs.pop(arg)
        
        if 'body' in kwargs:
            self.body = urllib.urlencode(kwargs.pop('body'))
            
        ## handle additional query and header args
        for arg in kwargs:
            if arg in self.params and self.params[arg]['paramType'] == 'query':
                path += "{0}={1}&".format(arg, kwargs[arg])
            else:
                self.headers[arg] = kwargs[arg]
        ## paramType: "body"
        ## paramType: "path"
        # return( path, headers, body )
        return (path, self.headers, self.body)
        
        
        
