Bootstrapping
=============

::

    ~/python-wordnik$ python bootstrap.py
    Creating directory '/home/martin/python-wordnik/bin'.
    Creating directory '/home/martin/python-wordnik/parts'.
    Creating directory '/home/martin/python-wordnik/eggs'.
    Creating directory '/home/martin/python-wordnik/develop-eggs'.
    Generated script '/home/martin/python-wordnik/bin/buildout'.
    ~/python-wordnik$ ./bin/buildout
    Develop: '/home/martin/python-wordnik/.'
    Getting distribution for 'zc.recipe.egg'.
    Got zc.recipe.egg 1.2.2.
    Installing python.
    Generated interpreter '...bin/python'.

Generating the REST API documentation
=====================================

::

	~/python-wordnik$ cd api_docs/
	~/python-wordnik/api_docs$ make html
	sphinx-build -b html -d build/doctrees   source build/html
	Making output directory...
	Running Sphinx v0.6.3
	loading pickled environment... not found
	building [html]: targets for 1 source files that are out of date
	updating environment: 1 added, 0 changed, 0 removed
	reading sources... [100%] index
	looking for now-outdated files... none found
	pickling environment... done
	checking consistency... done
	preparing documents... done
	writing output... [100%] index
	writing additional files... genindex search
	copying static files... done
	dumping search index... done
	dumping object inventory... done
	build succeeded.
	
	Build finished. The HTML pages are in build/html.


Generating Python API documentation
===================================

Just run ``epydoc --html -o doc src/wordnik``.


Running some test
=================

Output abbreviated for readability

::

    ~/python-wordnik$ ./bin/python

    >>> from pprint import pprint
    >>> import wordnik
    >>> w = wordnik.Wordnik(api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    >>> pprint(w.word("cat"))
    {'id': 27568, 'word': 'cat'}
    >>> pprint(w.definitions("cat"))
    [{'@headerId': 515951,
      '@id': 595351,
      'defTxtSummary': 'In medieval warfare, a machine resembling the pluteus, under the protection of which soldiers worked in sapping walls and fosses.',
      'headword': 'cat',
      'headwordId': 27568,
      'partOfSpeech': 'n.',
      'pos': 0},
     {'@headerId': 295572,
      '@id': 343222,
      'defTxtExtended': 'It is uncertain whether any animal now existing in a wild state is the ancestor of the domestic cat; probably it is descended from a cat originally domesticated in Egypt, though some regard the wildcat of Europe, F. catus, as the feral stock. The wildcat is much larger than the domestic cat, strong and ferocious, and very destructive to poultry, lambs, etc.',
      'defTxtSummary': u'A domesticated carnivorous quadruped of the family Felid\xe6 and genus Felis, F. domestica.',
      'headword': 'cat',
      'headwordId': 27568,
      'partOfSpeech': 'n.',
      'pos': 0},
      ...
     {'@headerId': 515951,
      '@id': 595353,
      'defTxtSummary': 'Same as channel-cat.',
      'headword': 'cat',
      'headwordId': 27568,
      'partOfSpeech': 'n.',
      'pos': 25}]
    >>> pprint(w.frequency("cat"))
    {'frequency': [{'count': 2, 'year': 1344},
                   {'count': 2, 'year': 1520},
                   {'count': 4, 'year': 1562},
                   ...
                   {'count': 11, 'year': 1861},
                   {'count': 74, 'year': 1862},
                   {'count': 48, 'year': 1863},
                   ...
                   {'count': 5, 'year': 1987},
                   {'count': 1, 'year': 2003},
                   {'count': 2, 'year': 2004},
                   ...
                   {'count': 27, 'year': 2007},
                   {'count': 9133, 'year': 2008},
                   {'count': 26243, 'year': 2009}],
     'totalCount': 47829,
     'unknownYearCount': 4184,
     'wordId': 27568}
    >>> pprint(w.examples("cat"))
    [{'display': 'If your cat is adjudged to be worth more than my ladle I will pay you the excess; and if my ladle be worth more than your cat, then you must pay me."',
      'documentId': 752174,
      'exampleId': 214053135,
      'id': 214053135,
      'rating': 75,
      'title': "Childhood's Favorites and Fairy Stories The Young Folks Treasury, Volume 1",
      'url': 'http://www.gutenberg.org/dirs/1/9/9/9/19993/19993-8.txt',
      'year': 1865},
     {'display': 'I admit the cat is your cat, and that I have no right to it, and that I am just a common sneak-thief.',
      'documentId': 1514909,
      'exampleId': 259296282,
      'id': 259296282,
      'rating': 75,
      'title': 'The Man with Two Left Feet And Other Stories',
      'url': 'http://www.gutenberg.org/dirs/etext05/2left10.txt',
      'year': 1928},
      ...
     {'display': "As the Chinese president said, it doesn't matter if the cat is a white cat or a black cat as long as the cat can do a good job.",
      'documentId': 16136876,
      'exampleId': 678140493,
      'id': 678140493,
      'rating': 55,
      'title': 'Top Stories - Google News',
      'url': 'http://www.ctv.ca/servlet/ArticleNews/story/CTVNews/20081110/Obama_bush_081110/20081110?hub=CTVNewsAt11',
      'year': 2008}]
    >>> pprint(w.suggest("oxymo"))
    {'match': [{'frequency': 0, 'word': 'oxymo'},
               {'frequency': 1000, 'word': 'oxymorphine'},
               {'frequency': 176, 'word': 'oxymoronic'},
               {'frequency': 67, 'word': 'Oxymoron'},
               {'frequency': 62, 'word': 'oxymoron'},
               {'frequency': 62, 'word': 'oxymorons'}],
     'matches': 5,
     'more': 0,
     'searchTerm': {'frequency': 0, 'word': 'oxymo'}}
    >>> pprint(w.suggest("oxymo", start_at=2))
    {'match': [{'frequency': 0, 'word': 'oxymo'},
               {'frequency': 1000, 'word': 'oxymorphine'},
               {'frequency': 176, 'word': 'oxymoronic'},
               {'frequency': 67, 'word': 'Oxymoron'},
               {'frequency': 62, 'word': 'oxymoron'},
               {'frequency': 62, 'word': 'oxymorons'}],
     'matches': 5,
     'more': 0,
     'searchTerm': {'frequency': 0, 'word': 'oxymo'}}
    >>> pprint(w.word_of_the_day())
    {'@id': 58,
     '@publishDate': '2009-10-30T04:00:00Z',
     'definition': [{'text': 'adjective, diligent in application or in the pursuit of an object; constant, steady, and persevering; steadily industrious; assiduous.'}],
     'example': [{'text': 'His sedulous pursuit of leisure left little time for relaxing.'}],
     'note': "The noun form is 'sedulity.'",
     'word': 'sedulous'}
    >>>
