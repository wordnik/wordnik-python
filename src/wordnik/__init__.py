#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Thin wrapper around the restful API from wordnik.com

This currently module presents a thin wrapper around the wordnik API.
"""
BASE_HOST = u"api.wordnik.com"

import sys
try:
    import json
except ImportError:
    import simplejson as json
import httplib
import cmd
from optparse import OptionParser
from xml.etree import ElementTree
from pprint import pprint

class RestfulError(Exception):
    pass

class InvalidRelationType(Exception):
    pass

class Wordnik(object):

    FORMAT_JSON = "json"
    FORMAT_XML = "xml"

    def __init__(self, api_key, format=FORMAT_JSON):
        self.api_key = api_key
        self.format = format

    def _make_request(self, request_uri, additional_headers={}):
        con = httplib.HTTPConnection(BASE_HOST)
        headers = {"api_key": self.api_key}
        headers.update(additional_headers)
        con.request("GET", request_uri, headers=headers)
        result = con.getresponse()
        result_string = result.read()
        if self.format == Wordnik.FORMAT_JSON:
            retval = json.loads(result_string)
        elif self.format == Wordnik.FORMAT_XML:
            retval = ElementTree.fromstring(result_string)
        if result.status != httplib.OK:
            try:
                raise RestfulError(retval["message"])
            except (TypeError, ), error:
                raise RestfulError(retval.find("message").text)
        return retval

    def word(self, word):
        """Returns a word from wordnik if it is in the corpus.

        Sample Response::

            <word>
                <id>27568</id>
                <word>cat</word>
            </word>

        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/api/word.%s/%s" % (self.format, word, )
        return self._make_request(request_uri)

    def definitions(self, word):
        """Returns the definitions from wordnik if the requested word is in the corpus.

        Sample Response::

            <definitions>
               <definition id="343222" headerId="295572">
                  <headword>cat</headword>
                  <headwordId>27568</headwordId>
                  <partOfSpeech>n.</partOfSpeech>
                  <pos>0</pos>
                  <defTxtSummary>
                     A domesticated carnivorous quadruped of the family Felidæ and genus
                     Felis, F. domestica.
                  </defTxtSummary>
                  <defTxtExtended>
                     It is uncertain whether any animal now existing in a wild state is
                     the ancestor of the domestic cat; probably it is descended from a
                     cat originally domesticated in Egypt, though some regard the wildcat of Europe,
                     <em>F. catus</em>, as the feral stock. The wildcat is much larger than the
                     domestic cat, strong and ferocious, and very destructive to poultry, lambs, etc.
                  </defTxtExtended>
               </definition>
               ...
            </definitions>

        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/api/word.%s/%s/definitions" % (self.format, word, )
        return self._make_request(request_uri)

    def frequency(self, word):
        """Returns the usage frequency of a word in the wordnik corpus.

        Sample Response::

            <frequencySummary>
                <frequency>
                    <count>18773</count>
                    <year>1846</year>
                </frequency>
                <frequency>
                    <count>23742</count>
                    <year>1847</year>
                </frequency>
                ...
            </frequencySummary>

        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/api/word.%s/%s/frequency" % (self.format, word, )
        return self._make_request(request_uri)

    def examples(self, word):
        """Returns example usages of a word in the wordnik corpus.

        Sample Response::

            <examples>
                <example>
                    <display>
                    When there was room on the ledge outside of the pots and
                    boxes for a cat, the cat was there--in sunny weather--stretched
                    at full length, asleep and blissful, with her furry belly to the
                    sun and a paw curved over her nose.
                    </display>
                    <documentId>726554</documentId>
                    <exampleId>212090080</exampleId>
                    <id>212090080</id>
                    <rating>75</rating>
                    <title>The Tragedy of Pudd'nhead Wilson</title>
                    <url>http://www.gutenberg.org/dirs/1/0/102/102.txt</url>
                    <year>1872</year>
                </example>
                ...
            </examples>

        Params:
            word : str
                The requested word

        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/api/word.%s/%s/examples" % (self.format, word, )
        return self._make_request(request_uri)

    def suggest(self, fragment, count=1, start_at=0):
        """Returns a word from wordnik if it is in the corpus.

        Sample Response::

            <searchResult>
                <matches>12385</matches>
                <more>12370</more>
                <searchTerm>
                    <word>ca</word>
                    <frequency>37</frequency>
                </searchTerm>
                <match>
                    <word>ca</word>
                    <frequency>37</frequency>
                </match>
                <match>
                    <word>caused</word>
                    <frequency>99797</frequency>
                </match>
                ...
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
        request_uri = "/api/suggest.%s/%s" % (self.format, fragment, )
        headers = {
            "api_key": self.api_key,
            "count": count,
            "startAt": start_at
            }
        return self._make_request(request_uri, headers)

    def word_of_the_day(self):
        """Fetches the *word of the day* from wordnik

        Sample Response::

            <wotd publishDate="2009-10-21T04:00:00Z" id="51">
               <word>doke</word>
               <definition>
                  <text>
                     noun, a deep dint or furrow, a contusion, or a flaw in a marble.
                  </text>
               </definition>
               <example>
                  <text>
                     He knew his garnet cats-eye with the sparkly doke would be taken by the tough kid in the next game.
                  </text>
               </example>
               <note>A rare word.</note>
            </wotd>


        Returns:
            The JSON or XML response from wordnik
        """
        request_uri = "/api/wordoftheday.%s" % (self.format, )
        return self._make_request(request_uri)

    def random_word(self, has_definition=False):
        """Fetch a random word from the Alpha Corpus.

        >>> import wordnik
        >>> k = "..."
        >>> w = wordnik.Wordnik(api_key=k)
        >>> w.random_word()
        {'word': 'smatch', 'id': 96660}
        >>>
        """
        request_uri = "/api/words.%s/randomWord?hasDictionaryDef=%s" % (self.format, has_definition, )
        return self._make_request(request_uri)

    def phrases(self, word, count=10):
        """Fetch bi-gram phrases containing a word.

        Sample Response:

          <bigrams>
             <bigram>
                <mi>12.414364902158674</mi>
                <wlmi>20.877889275429855</wlmi>
                <gram1>Christmas</gram1>
                <gram2>Eve</gram2>
             </bigram>
          </bigrams>
        """
        request_uri = "/api/word.%s/%s/phrases?count=%s" % (self.format, word, count, )
        return self._make_request(request_uri)

    def related(self, word, type=None):
        """Fetch related words for this word

        Sample Response:

          <words>
             <word>
                <id>18773</count>
                <wordstring>simpleton</year>
             </word>
             < word>
                <id>23742</id>
                <wordstring>boor</wordstring>
             </word>
          ...
          </words>
        """
        all_types = [None, "synonym", "antonym", "form", "equivalent", "hyponym", "variant"]
        if type in all_types:
            request_uri = "/api/word.%s/%s/related?type=%s" % (self.format, word, type, )
            return self._make_request(request_uri)
        else:
            raise InvalidRelationType()

    def punctuation(self, word):
        """Fetch a word's punctuation factor.

          Sample Response:
            <punctuationFactor>
               <exclamationPointCount>9486</exclamationPointCount>
               <periodCount>12454</periodCount>
               <questionMarkCount>52</questionMarkCount>
               <totalCount>39832</totalCount>
               <wordId>567925</wordId>
            </punctuationFactor>
        """
        request_uri = "/api/word.%s/%s/punctuationFactor" % (self.format, word, )
        return self._make_request(request_uri)

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

    parser.set_defaults(format=Wordnik.FORMAT_JSON)
    parser.set_defaults(api_key=u"")

    options, args = parser.parse_args(args[1:])

    try:
        wordnik = Wordnik(api_key=options.api_key, format=options.format)
    except (NameError, ), error:
        print error
    for arg in args:
        pprint(getattr(wordnik, options.choice)(arg))

if __name__ == "__main__":
    main(sys.argv)

__docformat__ = u"restructuredtext en"
__author__ = u"Martin Marcher"
