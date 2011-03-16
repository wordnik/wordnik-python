Help on class Wordnik in wordnik:

wordnik.Wordnik = class Wordnik(__builtin__.object)
 |  A generic Wordnik object. Use me to interact with the Wordnik API.
 |  
 |  All of my methods can be called in multiple ways. All positional
 |  arguments passed into one of my methods (with the exception of "format")
 |  will be substituted for the correponding path parameter, if possible.
 |  For example, consider the "get_word_examples" method. The URI path is:
 |  
 |  /word.{format}/{word}/examples
 |  
 |  So we can skip format (default format is JSON) and infer that the first
 |  positional argument is the word we want examples for. Hence:
 |  
 |  Wordnik.word_get_examples('cat')
 |  
 |  All other (non-path) arguments are keyword arguments. The "format"
 |  paramater can be passed in this way as well. Hence:
 |  
 |  Wordnik.word_get_examples('cat', format='xml', limit=500)
 |  
 |  In the case where you're making a POST, you will need a "body" keyword:
 |  
 |  Wordnik.word_list_put(wordListId=1234, body="Some HTTP body")
 |  
 |  Methods defined here:
 |  
 |  __init__(self, api_key=None)
 |      Initialize a Wordnik object. You must pass in an API key when
 |      you make a new Wordnik. We don't validate the API key until the
 |      first call against the API is made, at which point you'll find
 |      out if it's good.
 |  
 |  account_get_api_token_status(self, *args, **kwargs)
 |      Returns usage statistics for the API account.
 |      /account.{format}/apiTokenStatus
 |      
 |      Other Parameters:
 |        api_key
 |  
 |  account_get_authenticate(self, *args, **kwargs)
 |      Authenticates a User
 |      /account.{format}/authenticate/{username}
 |      
 |      Path Parameters:
 |        username
 |      
 |      Other Parameters:
 |        password
 |  
 |  account_get_regenerate_api_token(self, *args, **kwargs)
 |      Regenerates an API Token.  Currently not supported or tested.
 |      /account.{format}/regenerateApiToken
 |      
 |      Other Parameters:
 |        api_key
 |  
 |  account_get_user(self, *args, **kwargs)
 |      Returns the logged-in User
 |      /account.{format}/user
 |      
 |      Other Parameters:
 |        auth_token
 |  
 |  account_get_username_available(self, *args, **kwargs)
 |      Returns an ApiResponse indicating whether or not a username is available
 |      /account.{format}/usernameAvailable/{username}
 |      
 |      Path Parameters:
 |        username
 |  
 |  account_post_authenticate(self, *args, **kwargs)
 |      Authenticates a user
 |      /account.{format}/authenticate/{username}
 |      
 |      Path Parameters:
 |        username
 |      
 |      Other Parameters:
 |        body
 |  
 |  multi(self, calls, **kwargs)
 |      Multiple calls, batched. This is a "special case" method
 |      in that it's not automatically generated from the API documentation.
 |      That's because, well, it's undocumented. Here's how you use it:
 |      
 |      Wordnik.multi( [call1, call2, call3 ], **kwargs)
 |      
 |      where each "call" is (word, resource, {param1: value1, ...} )
 |      So we could form a batch call like so:
 |      
 |      calls = [("dog","examples"),("cat","definitions",{"limit":500})]
 |      
 |      Wordnik.multi(calls, format="xml")
 |  
 |  user_delete_word_of_the_day_list(self, *args, **kwargs)
 |      Deletes a specific word from a user's WordOfTheDayList
 |      /user.{format}/{username}/wordOfTheDayList/{permalink}/{wordToDelete}
 |      
 |      Path Parameters:
 |        username
 |        permalink
 |        wordToDelete
 |  
 |  user_get_word_of_the_day(self, *args, **kwargs)
 |      Returns the WordOfTheDay for a given user on a given date
 |      /user.{format}/{username}/wordOfTheDay/{date}
 |      
 |      Path Parameters:
 |        username
 |        date
 |      
 |      Other Parameters:
 |        includeAll
 |  
 |  user_get_word_of_the_day_list(self, *args, **kwargs)
 |      Returns a user's WordOfTheDayList
 |      /user.{format}/{username}/wordOfTheDayList
 |      
 |      Path Parameters:
 |        username
 |      
 |      Other Parameters:
 |        includeAll
 |  
 |  user_post_word_of_the_day_list(self, *args, **kwargs)
 |      Creates a WordOfTheDayList
 |      /user.{format}/{username}/wordOfTheDayList
 |      
 |      Path Parameters:
 |        username
 |      
 |      Other Parameters:
 |        body
 |  
 |  user_put_word_of_the_day_list(self, *args, **kwargs)
 |      Adds a WordOfTheDay to a user's WordOfTheDayList
 |      /user.{format}/{username}/wordOfTheDayList/{permalink}
 |      
 |      Path Parameters:
 |        username
 |        permalink
 |      
 |      Other Parameters:
 |        body
 |  
 |  user_put_word_of_the_day_list_add(self, *args, **kwargs)
 |      Adds an item to a user's WordOfTheDayList
 |      /user.{format}/{username}/wordOfTheDayList/{permalink}/add
 |      
 |      Path Parameters:
 |        username
 |        permalink
 |      
 |      Other Parameters:
 |        body
 |  
 |  word_get(self, *args, **kwargs)
 |      Given a word as a string, returns the WordObject that represents it
 |      /word.{format}/{word}
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        useCanonical
 |        includeSuggestions
 |  
 |  word_get_audio(self, *args, **kwargs)
 |      Fetches audio metadata for a word.
 |      /word.{format}/{word}/audio
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        useCanonical
 |        limit
 |  
 |  word_get_definitions(self, *args, **kwargs)
 |      Return definitions for a word
 |      /word.{format}/{word}/definitions
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        limit
 |        partOfSpeech
 |        includeRelated
 |        sourceDictionaries
 |        useCanonical
 |        includeTags
 |  
 |  word_get_examples(self, *args, **kwargs)
 |      Returns examples for a word
 |      /word.{format}/{word}/examples
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        limit
 |        includeDuplicates
 |        contentProvider
 |        useCanonical
 |        skip
 |  
 |  word_get_frequency(self, *args, **kwargs)
 |      Returns word usage over time
 |      /word.{format}/{word}/frequency
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        useCanonical
 |        startYear
 |        endYear
 |  
 |  word_get_hyphenation(self, *args, **kwargs)
 |      Returns syllable information for a word
 |      /word.{format}/{word}/hyphenation
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        useCanonical
 |        sourceDictionary
 |        limit
 |  
 |  word_get_phrases(self, *args, **kwargs)
 |      Fetches bi-gram phrases for a word
 |      /word.{format}/{word}/phrases
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        limit
 |        wlmi
 |        useCanonical
 |  
 |  word_get_pronunciations(self, *args, **kwargs)
 |      Returns text pronunciations for a given word
 |      /word.{format}/{word}/pronunciations
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        useCanonical
 |        sourceDictionary
 |        typeFormat
 |        limit
 |  
 |  word_get_related(self, *args, **kwargs)
 |      Return related words (thesaurus data) for a word
 |      /word.{format}/{word}/related
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        partOfSpeech
 |        sourceDictionary
 |        limit
 |        useCanonical
 |        type
 |  
 |  word_get_top_example(self, *args, **kwargs)
 |      Returns a top example for a word
 |      /word.{format}/{word}/topExample
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        contentProvider
 |        useCanonical
 |  
 |  word_get_word_forms(self, *args, **kwargs)
 |      Returns other forms of a word
 |      /word.{format}/{word}/wordForms
 |      
 |      Path Parameters:
 |        word
 |      
 |      Other Parameters:
 |        useCanonical
 |  
 |  word_list_delete(self, *args, **kwargs)
 |      Deletes an existing WordList
 |      /wordList.{format}/{wordListId}
 |      
 |      Path Parameters:
 |        wordListId
 |  
 |  word_list_get(self, *args, **kwargs)
 |      Fetches a WordList by ID
 |      /wordList.{format}/{wordListId}
 |      
 |      Path Parameters:
 |        wordListId
 |  
 |  word_list_get_words(self, *args, **kwargs)
 |      Fetches words in a WordList
 |      /wordList.{format}/{wordListId}/words
 |      
 |      Path Parameters:
 |        wordListId
 |      
 |      Other Parameters:
 |        sortBy
 |        sortOrder
 |        skip
 |        limit
 |  
 |  word_list_post_delete_words(self, *args, **kwargs)
 |      Removes words from a WordList
 |      /wordList.{format}/{wordListId}/deleteWords
 |      
 |      Path Parameters:
 |        wordListId
 |      
 |      Other Parameters:
 |        body
 |  
 |  word_list_post_words(self, *args, **kwargs)
 |      Adds words to a WordList
 |      /wordList.{format}/{wordListId}/words
 |      
 |      Path Parameters:
 |        wordListId
 |      
 |      Other Parameters:
 |        body
 |  
 |  word_list_put(self, *args, **kwargs)
 |      Updates an existing WordList
 |      /wordList.{format}/{wordListId}
 |      
 |      Path Parameters:
 |        wordListId
 |      
 |      Other Parameters:
 |        body
 |  
 |  word_lists_get(self, *args, **kwargs)
 |      Returns information about API parameters
 |      /wordLists
 |  
 |  word_lists_post(self, *args, **kwargs)
 |      Creates a WordList.
 |      /wordLists
 |      
 |      Other Parameters:
 |        body
 |  
 |  words_get_random_word(self, *args, **kwargs)
 |      Returns a single random WordObject, in the format specified by the URL
 |      /words.{format}/randomWord
 |      
 |      Other Parameters:
 |        hasDictionaryDef
 |        includePartOfSpeech
 |        excludePartOfSpeech
 |        minCorpusCount
 |        maxCorpusCount
 |        minDictionaryCount
 |        maxDictionaryCount
 |        minLength
 |        maxLength
 |  
 |  words_get_random_words(self, *args, **kwargs)
 |      Returns an array of random WordObjects, in the format specified by the URL
 |      /words.{format}/randomWords
 |      
 |      Other Parameters:
 |        hasDictionaryDef
 |        includePartOfSpeech
 |        excludePartOfSpeech
 |        minCorpusCount
 |        maxCorpusCount
 |        minDictionaryCount
 |        maxDictionaryCount
 |        minLength
 |        maxLength
 |        sortBy
 |        sortOrder
 |        skip
 |        limit
 |  
 |  words_get_search(self, *args, **kwargs)
 |      Searches words.
 |      /words.{format}/search
 |      
 |      Other Parameters:
 |        query
 |        caseSensitive
 |        includePartOfSpeech
 |        excludePartOfSpeech
 |        minCorpusCount
 |        maxCorpusCount
 |        minDictionaryCount
 |        maxDictionaryCount
 |        minLength
 |        maxLength
 |        skip
 |        limit
 |  
 |  words_get_word_of_the_day_lists(self, *args, **kwargs)
 |      Fetches WordOfTheDay objects for a specific date
 |      /words.{format}/wordOfTheDayLists/{date}
 |      
 |      Path Parameters:
 |        date
 |      
 |      Other Parameters:
 |        includeAll
 |  
 |  words_post_word_of_the_day_list_subscription(self, *args, **kwargs)
 |      Subscribes a user to a WordOfTheDayList
 |      /words.{format}/wordOfTheDayList/{permalink}/subscription
 |      
 |      Path Parameters:
 |        permalink
 |      
 |      Other Parameters:
 |        auth_token
 |        medium
 |        body
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)

