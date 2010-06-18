.. Wordnik Documentation documentation master file, created by
   sphinx-quickstart on Tue Nov  3 11:11:13 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Wordnik Documentation's documentation!
=================================================

Contents:

.. toctree::
   :maxdepth: 2

RESTfull API
============

Fetching a Word
---------------

This returns the word you requested, assuming it is found in our corpus.

URL:
        ``http://api.wordnik.com/api/word.{format}/{word}``
Method:
        ``GET``
Header:
        ``api_key={your_key}``

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/cat

Sample XML Response::

	<word>
	   <id>27568</id>
	   <word>cat</word>
	</word>

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/oxymoron

Sample JSON response::

       {'id': 145906, 'word': 'oxymoron'}


Fetching a word's definition
----------------------------

Definitions for words are available from Wordnik’s keying of the Century Dictionary.

URL:
        ``http://api.wordnik.com/api/word.{format}/{word}/definitions``
Method:
        ``GET``
Header:
        ``api_key={your key}``

Parameters:
        * ``count=<X>`` - The number of results returned

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/cat/defintions

Sample XML Response::

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
	         It is uncertain whether any animal now existing in a
	         wild state is the ancestor of the domestic cat;
	         probably it is descended from a cat originally
	         domesticated in Egypt, though some regard the wildcat
	         of Europe,<em>F. catus</em>, as the feral stock. The
	         wildcat is much larger than the domestic cat, strong
	         and ferocious, and very destructive to poultry,
	         lambs, etc.
	      </defTxtExtended>
	   </definition>
	   ...
	</definitions>

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/oxymoron/defintions

Sample JSON response::

	[{'@headerId': 425115,
	  '@id': 495975,
	  'defTxtSummary': 'In rhetoric, a figure consisting in adding to a word an epithet or qualification apparently contradictory; in general, close connection of two words seemingly opposed to each other (as, cruel kindness; to make haste slowly); an expression made epigrammatic or pointed by seeming self-contradictory.',
	  'headword': 'oxymoron',
	  'headwordId': 145906,
	  'partOfSpeech': 'n.',
	  'pos': 0}]


Fetching a word's frequency data
--------------------------------

You can see how common particular words occur in Wordnik’s alpha corpus, ordered  by year.

URL:
        ``http://api.wordnik.com/api/word.{format}/{word}/frequency``
Method:
        ``GET``
Header:
        ``api_key={your key}``

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/{word}/frequency

Sample XML response::

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


Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.json/{word}/frequency

Sample JSON response::

	{'frequency': [{'count': 1, 'year': 1808},
	               {'count': 1, 'year': 2003},
	               {'count': 1, 'year': 2007},
	               {'count': 262, 'year': 2008},
	               {'count': 797, 'year': 2009}],
	 'totalCount': 1075,
	 'unknownYearCount': 13,
	 'wordId': 145906}



Fetching examples for a word
----------------------------

You can retrieve 5 example sentences for a words in Wordnik’s alpha
corpus.  Each example contains the source document and a source URL,
if it exists.

URL:
        ``http://api.wordnik.com/api/word.{format}/{word}/examples``
Method:
        ``GET``
Header:
        ``api_key={your key}``

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/{word}/examples

Sample XML response::

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

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.json/oxymoron/examples

Sample JSON response::

	[{'display': 'If I ever heard an oxymoron, that is it. "',
	  'documentId': 10415532,
	  'exampleId': 490242222,
	  'id': 490242222,
	  'rating': 75,
	  'title': 'news | SJ | http://www.goupstate.com',
	  'url': 'http://www.goupstate.com/article/20090405/COLUMNISTS/904051083/1130?Title=Smoke-that',
	  'year': 2009},
	 {'display': 'These are two opposites - so you could say the word oxymoron is an oxymoron!',
	  'documentId': 11821026,
	  'exampleId': 533271992,
	  'id': 533271992,
	  'rating': 75,
	  'title': 'LearnHub Activities',
	  'url': 'http://english.learnhub.com/lesson/page/4686-oxymorons',
	  'year': 2008},
	 {'display': 'Thus the word oxymoron is itself an oxymoron.',
	  'documentId': 16193218,
	  'exampleId': 679754777,
	  'id': 679754777,
	  'rating': 75,
	  'title': "Feeds4all documents in category 'SEO'",
	  'url': 'http://www.feeds4all.com/i.aspx?ItemID=18493211',
	  'year': 2008},
	 {'display': 'i like when people think that the word oxymoron is an insult when they all CAPS the moron part.',
	  'documentId': 9188249,
	  'exampleId': 453054848,
	  'id': 453054848,
	  'rating': 55,
	  'title': 'The Pensblog',
	  'url': 'http://thepensblog.blogspot.com/2009/01/big-alex-news.html',
	  'year': 2009},
	 {'display': 'Talibs, the then external affairs minister Jaswant Singh had called this an "oxymoron" - and most of the world, the West certainly, would have agreed.',
	  'documentId': 10692746,
	  'exampleId': 498941972,
	  'id': 498941972,
	  'rating': 55,
	  'title': 'The Times of India',
	  'url': 'http://timesofindia.indiatimes.com/In-search-of-good-Taliban/rssarticleshow/4226199.cms',
	  'year': 2009}]



Calling the autocomplete service
--------------------------------

The autocomplete service gives you the opportunity to take a word
fragment (start of a word) and show what other words start with the
same letters.  The results are based on corpus frequency, not static
word lists, so you have access to more dynamic words in the language.

URL:
        ``http://api.wordnik.com/api/suggest.{format}/{word fragment}``
Method:
        ``GET``
Header:
        ``api_key={your key}``

Parameters:
        * ``count=X`` - The number of results to return
        * ``startAt=Y`` - You can also specify the starting index for
          the results returned.  This allows you to paginate through the
          matching values.

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/suggest.xml/ca

Sample XML response::

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

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/suggest.json/ca

Sample JSON response::

	{'match': [{'frequency': 37, 'word': 'ca'},
	           {'frequency': 99797, 'word': 'caused'},
	           {'frequency': 77139, 'word': 'candidates'},
	           {'frequency': 51557, 'word': 'causes'},
	           {'frequency': 41125, 'word': 'carriers'},
	           {'frequency': 39317, 'word': 'capabilities'},
	           {'frequency': 39189, 'word': 'cameras'},
	           {'frequency': 37275, 'word': "Canada's"},
	           {'frequency': 32769, 'word': 'captured'},
	           {'frequency': 29039, 'word': "Can't"},
	           {'frequency': 26786, 'word': 'carries'},
	           {'frequency': 22124, 'word': 'Cardinals'},
	           {'frequency': 21906, 'word': 'Canadians'},
	           {'frequency': 17668, 'word': 'casualties'},
	           {'frequency': 16747, 'word': 'canceled'},
	           {'frequency': 14622, 'word': 'Catholics'}],
	 'matches': 12385,
	 'more': 12370,
	 'searchTerm': {'frequency': 37, 'word': 'ca'}}


Calling the Word-of-the-Day Resource
------------------------------------

You can fetch Wordnik’s word-of-the day which contains definitions and example sentences.

URL:
        ``http://api.wordnik.com/api/wordoftheday.{format}``
Method:
        ``GET``
Header:
        ``api_key={your key}``

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/wordoftheday.xml

Sample XML response::

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

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/wordoftheday.json

Sample JSON response::

       {
        "@publishDate": "2009-10-21T04:00:00Z",
        "@id": 51,
        "definition":
                [
                        {"text": "noun, a deep dint or furrow, a contusion, or a flaw in a marble."},
                ],
                "example":
                [
                        {"text": "He knew his garnet cats-eye with the sparkly doke would be taken by the tough kid in the next game"},
                ],
                "note": "A rare word."
        }

Calling the Random Word Resource
--------------------------------

You can fetch a random word from the Alpha Corpus.

URL:
        ``http://api.wordnik.com/api/words.{format}/randomWord``
Method:
        ``GET``
Header:
        ``api_key={your key}``

Parameters:
        * ``hasDictionaryDef=true`` - You can ask the API to return
          only words where there is a definition available.

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/words.xml/randomWord

Sample XML response::

	<word>
	   <id>96066</id>
	   <word>whetstone</word>
	</word>

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/words.json/randomWord

Sample JSON response::

       {
        "id":131921,
        "word":"melanotekite"
       }

Access Messages
---------------

If you attempt to call any API methods with invalid or an incorrect
API key you will see a message like below:

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/cat/definitions

XML Format::

	<apiResponse>
	   <message>unauthorized</message>
	   <type>error</type>
	</apiResponse>

Furthermore if you have exceeded a limit assigned to your key, you
will see this:

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/cat/definitions

XML Format::

	<apiResponse>
	   <message>exceeded access limits</message>
	   <type>error</type>
	</apiResponse>

If you request a resource that doesn’t exist, you will see the
following:

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/cat/definitions

XML Format::

	<apiResponse>
	   <message>exceeded access limits</message>
	   <type>invalid resource</type>
	</apiResponse>

And finally, if the server is really busy it is possible to see this:

Request::

        curl -H "api_key:{token}" http://api.wordnik.com/api/word.xml/cat/definitions

XML Format::

	<apiResponse>
	   <message>too busy</message>
	   <type>unable to {do what you asked}</type>
	</apiResponse>


Indices and tables
==================

.. * :ref:`genindex`
.. * :ref:`modindex`

* :ref:`search`

