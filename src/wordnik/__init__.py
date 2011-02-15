#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Thin wrapper around the restful API from wordnik.com

This module presents a thin wrapper around the wordnik API.
"""
BASE_HOST = u"api.wordnik.com"

import sys
try:
    import json
except ImportError:
    import simplejson as json
import httplib
import urllib
from optparse import OptionParser
from xml.etree import ElementTree
from pprint import pprint

class RestfulError(Exception):
    pass

class InvalidRelationType(Exception):
    pass

PARTS_OF_SPEECH = ['noun', 'verb', 'adjective', 'adverb', 'idiom', 'article', 'abbreviation', 'preposition', 'prefix', 'interjection','suffix', 'conjunction', 'adjective_and_adverb', 'noun_and_adjective',  'noun_and_verb_transitive', 'noun_and_verb', 'past_participle', 'imperative', 'noun_plural', 'proper_noun_plural', 'verb_intransitive', 'proper_noun', 'adjective_and_noun',   'imperative_and_past_participle', 'pronoun', 'verb_transitive', 'noun_and_verb_intransitive', 'adverb_and_preposition','proper_noun_posessive','noun_posessive']


FORMAT_JSON = "json"
FORMAT_XML = "xml"

class Wordnik(object):
    """ Wordnik API object """


    def __init__(self, api_key, default_format=FORMAT_JSON):
        self.api_key = api_key
        self.format = default_format
        self.formatters = {
               FORMAT_JSON: json.loads,
               FORMAT_XML: ElementTree.fromstring
			  }

    def _format_url_args(self, path, **kws):
        if kws:
            path += "?%s" % urllib.urlencode(kws)
        return path

    def _get(self, request_uri, additional_headers={}, format=None):
        """ make a GET request to the wordnik server """
        return self._make_request(request_uri, additional_headers, format, "GET")

    def _make_request(self, request_uri, additional_headers={}, format=None, method="GET"):
        """ make a request to the wordnik server """

        format = format or self.format
        con = httplib.HTTPConnection(BASE_HOST)
        headers = {"api_key": self.api_key}
        headers.update(additional_headers)
        con.request(method, request_uri % format, headers=headers)
        result = con.getresponse()

        retval = self.formatters[format](result.read())
        if result.status != httplib.OK:
            try:
                raise RestfulError(retval["message"])
            except (TypeError, ), error:
                raise RestfulError(retval.find("message").text)

        return retval 

    def multi(self, calls, format=None):
        """
        Interface to the Wordnik batch API.

        Sample Response:
            {u'responseItems':
              [
                {u'responseName':
                   u'dog/definitions',
                 u'responsePosition':
                   1,
                 u'responseContent':
                  [
                    {u'text':
                       u'A domesticated carnivorous mammal ...',
                     u'word':
                       u'dog',
                     u'partOfSpeech':
                       u'noun',
                     u'sequence':
                       u'0'}
                  ]
                }
              ]
            }
        Params:
            calls : list of tuples:
                [ (word, resource, limit), (word, resource, limit) ... ]
        e.g. Wordnik.multi( [ ('dog', 'definitions', 1) ] )
        """

        request_uri = "/v4/word.%s?multi=true"
        callsMade = 0
        for call in calls:
            word = call[0]
            resource = call[1]
            if len(call) < 3:
                limit = None
            else:
                limit = call[2]
            request_uri += "&resource.%s=%s/%s&limit.%s=%s" % (callsMade, word, resource, callsMade, limit)
            callsMade += 1

        return self._get(request_uri, format=format)

        # /word.json?multi=true&resource.0=cat/definitions&limit.0=1&resource.1=cat/examples&limit.1=1&resource.2=dog/definitions&limit.2=1&resource.3=dog/examples&limit.3=1

    def word(self, word, format=None):
        """Returns a word from wordnik if it is in the corpus.

        Sample Response::

            <wordObject>
               <word>clover</word>
               <canonicalForm>clover</canonicalForm>
            </wordObject>

        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/v4/word.%%s/%s" % word
        return self._get(request_uri, format=format)

    def definitions(self, word, count=None, partOfSpeech=None, format=None):
        """Returns the definitions from wordnik if the requested word is in the corpus.

        Sample Response::

            <definitions>
               <definition sequence="0">
                  <text>Any of various herbs of the genus Trifolium in the pea family, having trifoliolate leaves and dense heads of small flowers and including species grown for forage, for erosion control, and as a source of nectar for honeybees.</text>
                  <partOfSpeech>noun</partOfSpeech>
                  <word>clover</word>
               </definition>
               <definition sequence="1">
                  <text>Any of several other plants in the pea family, such as bush clover and sweet clover.</text>
                  <partOfSpeech>noun</partOfSpeech>
                  <word>clover</word>
               </definition>
               ...
            </definitions>

        Params:
            word : str
                The requested word
        Returns:
            The JSON or XML response from wordnik
        """

        request_uri = "/v4/word.%%s/%s/definitions" % (word )
        request_uri = self._format_url_args(request_uri, count=count, partOfSpeech=partOfSpeech)
        return self._get(request_uri, format=format)

    def frequency(self, word, format=None):
        """Returns the usage frequency of a word in the wordnik corpus.

        Sample Response::

            <frequencySummary>
               <frequency>
                  <count>99</count>
                  <year>1800</year>
               </frequency>
               <frequency>
                  <count>14</count>
                  <year>1801</year>
               </frequency>
               ...
               <totalCount>135115637</totalCount>
                  <unknownYearCount>0</unknownYearCount>
                  <word>clover</word>
            </frequencySummary>
            
        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/v4/word.%%s/%s/frequency" % (word, )
        return self._get(request_uri, format=format)

    def examples(self, word, format=None):
        """Returns example usages of a word in the wordnik corpus.

        Sample Response::

            <exampleSearchResults>
               <examples>
                  <example>
                     <text>I am not familiar with Virginia soils but I can tell you in the midwest clover is a Deer dream plot.</text>
                     <documentId>30642987</documentId>
                     <exampleId>735059704</exampleId>
                     <provider>
                        <id>711</id>
                        <name>wordnik</name>
                     </provider>
                     <rating>444.0</rating>
                     <title>Food Plots For Virginia</title>
                     <url>http://www.fieldandstream.com/forums/hunting/deer-hunting/food-plots-virginia</url>
                     <word>clover</word>
                     <year>2010</year>
                  </example>
                  ...
               </examples>
               <totalResults>0</totalResults>
             </exampleSearchResults>

        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/v4/word.%%s/%s/examples" % ( word, )
        return self._get(request_uri, format=format)

    def suggest(self, fragment, count=1, start_at=0, format=None):
        """Returns a word from wordnik if it is in the corpus.

        Sample Response::

            <searchResult>
                <matches>23</matches>
                <more>7</more>
                <searchTerm>
                    <count>9446</count>
                    <wordstring>clover</wordstring>
                </searchTerm>
                <match>
                    <count>9446</count>
                    <wordstring>clover</wordstring>
                </match>
                <match>
                    <count>7362</count>
                    <wordstring>Clover</wordstring>
                </match>
                ...
                <style/>
            </searchResult>

        Params:
            word : str
                The requested word
            count : int
                How many suggestions to return at most (default: 1)
            start_at : int
                From where in the word index the suggestions should start
                (default: 0 - the beginning)

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/v4/suggest.%%s/%s" % (fragment)
        request_uri = self._format_url_args(request_uri, count=count, startAt=start_at)
        return self._get(request_uri, format=format)

    def word_of_the_day(self, format=None):
        """Fetches the *word of the day* from wordnik

        Sample Response::

            <WordOfTheDay>
               <contentProvider>
                  <id>711</id>
                  <name>wordnik</name>
               </contentProvider>
               <definitions>
                  <definition>
                     <note/>
                     <partOfSpeech name="noun" typeId="200"/>
                     <source>century</source>
                     <text>(adj) Fearful; terrible.</text>
                  </definition>
                  <definition>
                     <note/>
                     <partOfSpeech name="noun" typeId="200"/>
                     <source>century</source>
                     <text>(adj) Unexpected; sudden.</text>
                  </definition>
                </definitions>
                <examples>
                      <example>
                         <text>The Earl laughed: 'Many a ferly fares to the fair-eyed,' quoth he; 'and also I will tell thee in thine ear that this Lady may not be so great as her name is great.'</text>
                         <id>454330288</id>
                         <title>Child Christopher and Goldilind the Fair</title>
                         <url>http://fiction.eserver.org/novels/child_christopher.html/view</url>
                      </example>
                </examples>
                <id>4320</id>
                <note>'Ferly' comes from the Old English, 'faerlic,' meaning unexpected.</note>
                <publishDate>2010-11-01T02:00:00Z</publishDate>
                <word>ferly</word>
            </WordOfTheDay>
                


        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/v4/words.%s/wordOfTheDay"
        return self._get(request_uri, format=format)

    def random_word(self, has_definition=False, format=None):
        """Fetch a random word from the Alpha Corpus.

        <wordObject>
           <word>teld</word>
        </wordObject>
        """
        request_uri = "/v4/words.%%s/randomWord?hasDictionaryDef=%s" % ( has_definition, )
        return self._get(request_uri, format=format)

    def phrases(self, word, count=10, format=None):
        """Fetch bi-gram phrases containing a word.

        Sample Response:

          <bigrams>
             <bigram>
                <count>1</count>
                <mi>16.952889207360002</mi>
                <wlmi>16.952889207360002</wlmi>
                <gram1>gravy</gram1>
                <gram2>clover</gram2>
             </bigram>
             <bigram>
                <count>1</count>
                <mi>14.656102547020637</mi>
                <wlmi>14.656102547020637</wlmi>
                <gram1>clover</gram1>
                <gram2>rolls</gram2>
             </bigram>
          </bigrams>
        """
        request_uri = "/v4/word.%%s/%s/phrases" % (word)
        request_uri = self._format_url_args(request_uri, count=count)
        return self._get(request_uri, format=format)

    def related(self, word, type=None, format=None):
        """Fetch related words for this word

        Sample Response:

        <relateds>
           <related relationshipType="hyponym">
              <words>
                 <word>alpine clover</word>
                 <word>trifolium repens</word>
                 <word>Dutch clover</word>
                 ...
              </words>
           </related>
        </relateds>

        """
        all_types = [None, "synonym", "antonym", "form", "equivalent", "hyponym", "variant", "same-context"]
        if type in all_types:
            request_uri = "/v4/word.%%s/%s/related?type=%s" % (word, type, )
            return self._get(request_uri, format=format)
        else:
            raise InvalidRelationType()

    def punctuation(self, word, format=None):
        """Fetch a word's punctuation factor.

          Sample Response:
            <punctuationFactor>
               <exclamationPointCount>9486</exclamationPointCount>
               <periodCount>12454</periodCount>
               <questionMarkCount>52</questionMarkCount>
               <totalCount>39832</totalCount>
               <wordId>567925</wordId>
               <style/>
            </punctuationFactor>
        """
        request_uri = "/v4/word.%%s/%s/punctuationFactor" % (word, )
        return self._get(request_uri, format=format)

    def text_pronunciation(self, word, format=None):
        """Fetch a word’s text pronunciation from the Wornik corpus, in arpabet and/or gcide-diacritical format.

        Sample response:
        <textProns>
            <textPron seq="0">
                <id>0</id>
                <raw>(klōˈvər)</raw>
                <rawType>ahd-legacy</rawType>
            </textPron>
            <style/>
        </textProns>
        """
        request_uri = "/v4/word.%%s/%s/pronunciations" % (word, )
        return self._get(request_uri, format=format)

    def audio(self, word, format=None, useCanonical=None, limit=None):
        """Fetch an audio pronunciation of a word (an expiring link is returned

        Sample response:

        [
          {
            "id": 9904,
            "word": "cat",
            "createdAt": "2009-03-15T15:32:01.000+0000",
            "commentCount": 0,
            "createdBy": "ahd",
            "fileUrl": "http://api.wordnik.com/v4/audioFile.mp3/81402c8700312eb232bef08ffc45ef997df561a2aa44f0b4e13101b5aacad223"
          }
        ]

        """
        request_uri = "/v4/word.%%s/%s/audio" % (word, )
        return self._get(request_uri, format=format)

def main(args):

    parser = OptionParser()
    parser.add_option("-f", "--format", dest="format", type="string", action="store", metavar="FORMAT")
    parser.add_option("-a", "--api-key", dest="api_key", type="string", action="store", metavar="API_KEY")
    parser.add_option("-c", "--choice", dest="choice",
                      choices=("word",
                               "definitions",
                               "frequency",
                               "examples",
                               "suggest",
                               "word_of_the_day", 
                               "random_word",
                               "phrases",
                               "related",
                               "punctuation",
                               ),
                      action="store",
                      metavar="CHOICE"
                      )

    parser.set_defaults(format=FORMAT_JSON)
    parser.set_defaults(api_key=u"")

    options, args = parser.parse_args(args[1:])

    try:
        wordnik = Wordnik(api_key=options.api_key, default_format=options.format)
    except (NameError, ), error:
        print error
    for arg in args:
        pprint(getattr(wordnik, options.choice)(arg))

if __name__ == "__main__":
    main(sys.argv)

__docformat__ = u"restructuredtext en"
__author__ = u"Altay Guvench"
