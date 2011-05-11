Wordnik Python Driver
---------------------------------

### Synopsis ###

This is the Python driver for the Wordnik API. All the documentation and method names are taken straight from the api's endpoint descriptions (e.g. http://api.wordnik.com/v4/word.json ). The module uses introspection to build methods at runtime, so the source code does not provide help on individual methods. To get help on the methods themselves, please use ```help(Wordnik) ``` from inside the Python REPL.

Below you'll find some simple usage examples and basic API documentation.

Thanks,
The Wordnik Pythonistas

### Usage ###

``` python

#!/usr/bin/env python

from wordnik import Wordnik
from pprint import pprint

w = Wordnik(api_key="deadb33f")
output = w.word_get_definitions("beef")
pprint(output)
"""and then we get..."""
[{u'partOfSpeech': u'noun',
  u'score': 0.0,
  u'sequence': u'0',
  u'sourceDictionary': u'ahd-legacy',
  u'text': u'A full-grown steer, bull, ox, or cow, especially one intended for use as meat.',
  u'word': u'beef'},
 {u'partOfSpeech': u'noun',
  u'score': 0.0,
  u'sequence': u'1',
  u'sourceDictionary': u'ahd-legacy',
  u'text': u'The flesh of a slaughtered full-grown steer, bull, ox, or cow.',
  u'word': u'beef'},
 {u'partOfSpeech': u'noun',
  u'score': 0.0,
  u'sequence': u'2',
  u'sourceDictionary': u'ahd-legacy',
  u'text': u'Informal   Human muscle; brawn.',
  u'word': u'beef'},
 {u'partOfSpeech': u'noun',
  u'score': 0.0,
  u'sequence': u'3',
  u'sourceDictionary': u'ahd-legacy',
  u'text': u'Slang   A complaint.',
  u'word': u'beef'},
 {u'partOfSpeech': u'verb-intransitive',
  u'score': 0.0,
  u'sequence': u'4',
  u'sourceDictionary': u'ahd-legacy',
  u'text': u'Slang   To complain.',
  u'word': u'beef'},
 {u'partOfSpeech': u'phrasal-verb',
  u'score': 0.0,
  u'sequence': u'5',
  u'sourceDictionary': u'ahd-legacy',
  u'text': u'beef up  Informal   To make or become greater or stronger:  beef up the defense budget. ',
  u'word': u'beef'}]


```

### Classes ###

``` python 
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
    
    
    def __init__(self, api_key=None, username=None, password=None, beta=False):
        """
        Initialize a Wordnik object. You must pass in an API key when
        you make a new Wordnik. We don't validate the API key until the
        first call against the API is made, at which point you'll find
        out if it's good.
        
        If you also pass in a username and password, we will try to get an
        auth token so you can use the Wordnik authenticated methods.
        Alternatively, you can call Wordnik.authenticate(user, pass)
        """

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

    def authenticate(self, username, password):
        """A convenience method to get an auth token in case the object was 
        not instantiated with a username and a password.
        """

    
```
### Exceptions ###

``` python

class RestfulError(Exception):
    """Raised when response from REST API indicates an error has occurred."""

class NoAPIKey(Exception):
    """Raised if we don't get an API key."""

class MissingParameters(Exception):
    """Raised if we try to call an API method with required parameters missing"""

```
