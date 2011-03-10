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
    
def generate_docs(params, response, summary, path):
    docstring   = "{0}\n".format(summary)
    docstring  += "{0}\n".format(path)
    
    pathParams  = [ p for p in params if p['paramType'] == "path" and p.get('name') != "format" ]
    if pathParams:
        docstring += "\nPath Parameters:\n"
    for param in pathParams:
        name      = param.get('name') or 'body'
        paramDoc  = "  {0}\n".format(name)
        docstring += paramDoc
 
    
    otherParams = [ p for p in params if p['paramType'] != "path" ]
    if otherParams:
        docstring += "\nOther Parameters:\n"
    for param in otherParams:
        name      = param.get('name') or 'body'
        paramDoc  = "  {0}\n".format(name)
        docstring += paramDoc

    return docstring

def create_method(name, doc, params, path):
    def _method(self, *args, **kwargs):
        return self._run_command(name, *args, **kwargs)
    
    _method.__doc__  = str(doc)
    _method.__name__ = str(name)
    _method._path    = path
    _method._params  = params
    
    return _method

def process_args(path, params, args, kwargs):
    """This does all the path substitution and the population of the
    headers and/or body, based on positional and keyword arguments.
    """
    
    positional_args_re  = re.compile('{([\w]+)}')
    headers             = {}
    body                = None
    
    ## get "{format} of of the way first"
    format = kwargs.get('format') or DEFAULT_FORMAT
    path = path.replace('{format}', format) + "?"

    ## words with spaces and punctuation XXX
    ## substiture the positional arguments, left-to-right
    for arg in args:
        path = positional_args_re.sub(arg, path, count=1)

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
        body = urllib.urlencode(kwargs.pop('body'))
    
    ## handle additional query and header args
    for arg in kwargs:
        if arg in params and params[arg]['paramType'] == 'query':
            path += "{0}={1}&".format(arg, kwargs[arg])
        else:
            headers[arg] = kwargs[arg]

    ## return a 3-tuple of (<URI path>, <headers>, <body>)
    return (path, headers, body)

def _convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def _normalize(path, method):
    param_re = re.compile('{[\w]+}')
    under_re = re.compile('(^[_]+|[_]+$)')
    un_camel_re = re.compile('[a-z]([A-Z])')
    repeat_under_re = re.compile('[_]+')
    
    p = method + '_' + path.replace('/', '_').replace('.', '_')
    p = param_re.subn('', p)[0]
    p = under_re.subn('', p)[0]
    p = repeat_under_re.subn('_', p)[0]
    return _convert(p)

def dictify(params):
    p = {}
    for param in params:
        if 'name' in param:
            p[param['name']] = param
        else:
            p['body'] = param

    return p

def find_missing_path_params(self, path):
    """This will check to make sure there are no un-substituted params
    e.g. /word.json/{word}
    """
    if self.positional_args_re.search(path):
        matches = self.positional_args_re.findall(path)
        missingParams = ", ".join(matches)
        raise MissingParameters("Could not substitute some parameters: {0}".format(missingParams))


def _do_http(uri, headers, body=None):
    """This wraps the HTTP call. This may get factored out in the future."""
    url = DEFAULT_URL + uri
    request = urllib2.Request(url, body, headers)
    return urllib2.urlopen(request).read()
        
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
    
    Wordnik.get_word_examples('cat')
    
    All other (non-path) arguments are keyword arguments. The "format"
    paramater can be passed in this way as well. Hence:
    
    Wordnik.get_word_examples('cat', format='xml', limit=500)
    
    In the case where you're making a POST, you will need a "body" keyword:
    
    Wordnik.put_word_list(wordListId=1234, body="Some HTTP body")    
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
                ## will get translated into method: get_user_word_of_the_day_list
                methodName = _normalize(path, httpmethod)
                        
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
            path += "&resource.%s=%s/%s" % (callsMade,word,resource)
            for key,val in otherParams.items():
                path += "&%s.%s=%s" % (key, callsMade, val)
            callsMade += 1
        
        headers = { "api_key": self._api_key }
        return _do_http(path, headers)
        
Wordnik._populate_methods()