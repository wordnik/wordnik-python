#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Thin wrapper around the restful API from wordnik.com

This module currently presents a thin wrapper around the wordnik API.
"""


import sys
try:
    import simplejson as json
except ImportError:
    import json
import httplib
from optparse import OptionParser
from xml.etree import ElementTree
from pprint import pprint


class RestfulError(Exception):
    """Raised when response from REST API indicates an error has occurred."""

class InvalidRelationType(Exception):
    """Raised if Wordnik.related method is passed invalid relation type."""

BASE_HOST = u"api.wordnik.com"

PARTS_OF_SPEECH = set(['noun', 'verb', 'adjective', 'adverb', 'idiom', 
                  'article', 'abbreviation', 'preposition', 'prefix', 
                  'interjection', 'suffix', 'conjunction', 
                  'adjective-and-adverb', 'noun-and-adjective',  
                  'noun-and-verb-transitive', 'noun-and-verb', 
                  'past-participle', 'imperative', 'noun-plural', 
                  'proper-noun-plural', 'verb-intransitive', 'proper-noun', 
                  'adjective-and-noun',   'imperative-and-past-participle', 
                  'pronoun', 'verb-transitive', 'noun-and-verb-intransitive', 
                  'adverb-and-preposition','proper-noun-posessive',
                  'noun-posessive']) 


class Wordnik(object):
    """ Wordnik API object """

    FORMAT_JSON = "json"
    FORMAT_XML = "xml"

    def __init__(self, api_key, default_format=FORMAT_JSON):
        self.api_key = api_key
        self.default_format = default_format
        self.formatters = {
               Wordnik.FORMAT_JSON: json.loads,
               Wordnik.FORMAT_XML: ElementTree.fromstring
			  }

    @staticmethod
    def _format_url_args(path, **kws):
        """Convert KWargs to URL parameters without altering spaces etc."""
        if kws:
            args = ['%s=%s' % (arg, val) for (arg, val) in kws.items() 
                    if val is not None]
            path += '?%s' % '&'.join(args)
        return path

    def _get(self, request_uri, additional_headers=None, format_=None):
        """ make a GET request to the wordnik server """
        return self._make_request(request_uri, additional_headers, format_)

    def _make_request(self, request_uri, additional_headers=None, format_=None, 
                      method="GET"):
        """ make a request to the wordnik server """

        format_ = format_ or self.default_format
        con = httplib.HTTPConnection(BASE_HOST)
        headers = {"api_key": self.api_key}
        if additional_headers is not None:
            headers.update(additional_headers)
        con.request(method, request_uri % format_, headers=headers)
        result = con.getresponse()

        retval = self.formatters[format_](result.read())
        if result.status != httplib.OK:
            try:
                raise RestfulError(retval["message"])
            except TypeError:
                raise RestfulError(retval.find("message").text)

        return retval 

    def api_usage(self, format_=None):
        """Return information about the user's API key usage."""
        request_uri = "/api/account.%s/apiTokenStatus"
        return self._get(request_uri, format_=format_)


    def word(self, word, format_=None):
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
        request_uri = "/api/word.%%s/%s" % word
        return self._get(request_uri, format_=format_)

    def phrases(self, word, count=10, format_=None):
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
        request_uri = "/api/word.%%s/%s/phrases" % (word)
        request_uri = self._format_url_args(request_uri, count=count)
        return self._get(request_uri, format_=format_)

    def definitions(self, word, count=None, part_of_speech=None, format_=None):
        """Return the definitions if the requested word is in the corpus.

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

        request_uri = "/api/word.%%s/%s/definitions" % (word )
        request_uri = self._format_url_args(request_uri, count=count, 
                                            partOfSpeech=part_of_speech)
        return self._get(request_uri, format_=format_)

    def examples(self, word, format_=None):
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
        request_uri = "/api/word.%%s/%s/examples" % ( word, )
        return self._get(request_uri, format_=format_)

    def related(self, word, type_=None, format_=None):
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
        all_types = [None, "synonym", "antonym", "form", "equivalent", 
                     "hyponym", "variant"]
        if type_ in all_types:
            request_uri = "/api/word.%%s/%s/related?type=%s" % (word, type_)
            return self._get(request_uri, format_=format_)
        else:
            raise InvalidRelationType()

    def frequency(self, word, format_=None):
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
        request_uri = "/api/word.%%s/%s/frequency" % (word, )
        return self._get(request_uri, format_=format_)

    def punctuation(self, word, format_=None):
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
        request_uri = "/api/word.%%s/%s/punctuationFactor" % (word, )
        return self._get(request_uri, format_=format_)

    def text_pronunciation(self, word, format_=None):
        """Fetch a word's pronunciation in arpabet or gcide-diacritical format.

        Sample response:
        <textProns>
          <textPron seq="0">
            <id>0</id>
            <raw>(kŏm*pūt"ẽr)</raw>
            <rawType>gcide-diacritical</rawType>
          </textPron>
          <textPron seq="0">
            <id>0</id>
            <raw>K AH0 M P Y UW1 T ER0</raw>
            <rawType>arpabet</rawType>
          </textPron>
        </textProns>
        """
        request_uri = "/api/word.%%s/%s/pronunciations" % (word, )
        return self._get(request_uri, format_=format_)

    def suggest(self, fragment, count=1, start_at=0, format_=None):
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
        request_uri = "/api/suggest.%%s/%s" % (fragment)
        request_uri = self._format_url_args(request_uri, count=count, 
                                            startAt=start_at)
        return self._get(request_uri, format_=format_)

    def word_search(self, query, include_pos=None, exclude_pos=None, 
                    min_corpus_count=None, max_corpus_count=None, 
                    min_dictionary_count=None, max_dictionary_count=None, 
                    min_length=None, max_length=None, skip=None, limit=None,
                    format_=None):
        """Fetch words matching `query` and other optional constraints."""
        if include_pos is not None:
            if not isinstance(include_pos, basestring):
                include_pos = ','.join(include_pos)
        if exclude_pos is not None:
            if not isinstance(exclude_pos, basestring):
                exclude_pos = ','.join(exclude_pos)

        request_uri = self._format_url_args('/api/words.%s/search', query=query,
            includePartOfSpeech=include_pos, excludePartOfSpeech=exclude_pos, 
            minCorpusCount=min_corpus_count, maxCorpusCount=max_corpus_count, 
            minDictionaryCount=min_dictionary_count, 
            maxDictionaryCount=max_dictionary_count, minLength=min_length, 
            maxLength=max_length, skip=skip, limit=limit)

        try:
            ret = self._get(request_uri, format_=format_)
        except RestfulError:
            ret = []
        return ret

    def word_of_the_day(self, format_=None):
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
        request_uri = "/api/wordoftheday.%s"
        return self._get(request_uri, format_=format_)

    def random_word(self, has_definition=False, format_=None):
        """Fetch a random word from the Alpha Corpus.

        >>> import wordnik
        >>> k = "..."
        >>> w = wordnik.Wordnik(api_key=k)
        >>> w.random_word()
        {'word': 'smatch', 'id': 96660}
        >>>
        """
        request_uri = "/api/words.%%s/randomWord?hasDictionaryDef=%s" % \
                      ( has_definition, )
        return self._get(request_uri, format_=format_)

def main(args):
    """Basic command-line interface to Wordnik's API.

    Request information from Wordnik's corpora is printed to stdout as either
    JSON or XML. Use the --help option to get a list of available resources.

    Example Usage:
        # Print out Wordnik's Word of the Day.
        python wordnik.py -a <YOUR_API_KEY> -c word_of_the_day

        # Print out a random word.
        python wordnik.py -a <YOUR_API_KEY> -c random_word

        # Print out definitions for the word "amphibian".
        python wordnik.py -a <YOUR_API_KEY> -c word amphibian

    """

    usage = """%prog -a <API_KEY> -c word_of_the_day
       %prog -a <API_KEY> -c random_word

       # Choices requiring one or more words as arguments:
       %prog -a <API_KEY> -c definitions amphibian mammals
       %prog -a <API_KEY> -c frequency amphibian mammals
       %prog -a <API_KEY> -c examples amphibian mammals
       %prog -a <API_KEY> -c suggest amphibian mammals
       %prog -a <API_KEY> -c phrases amphibian mammals
       %prog -a <API_KEY> -c related amphibian mammals
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--format", dest="format_", action="store", 
                      choices=(Wordnik.FORMAT_JSON, Wordnik.FORMAT_XML),
                      default=Wordnik.FORMAT_JSON, metavar="<FORMAT>")
    parser.add_option("-a", "--api-key", dest="api_key", type="string", 
                      action="store", metavar="<API_KEY>")
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
                      metavar="<CHOICE>"
                      )

    options, args = parser.parse_args(args)

    if not options.api_key:
        parser.error('api_key must be specified.')

    wordnik = Wordnik(api_key=options.api_key, default_format=options.format_)

    if options.choice == 'word_of_the_day':
        pprint(wordnik.word_of_the_day())

    elif options.choice == 'random_word':
        pprint(wordnik.random_word())

    else:
        for arg in args:
            pprint(getattr(wordnik, options.choice)(arg))

if __name__ == "__main__":
    exit(main(sys.argv[1:]))

