# Python 2.7 client for Wordnik.com API

## Overview

This is a Python 2.7 client for the Wordnik.com v4 API. For more information, see http://developer.wordnik.com/ . This client has been generated using the Swagger code generator, which builds robust API clients and beautiful API documentation automatically. If you'd like to learn more about Swagger, visit http://swagger.wordnik.com/ (but you don't need to know anything about Swagger to simply use this API client for Wordnik, this page will tell get you up to speed on that account).

If you need help after reading the below, please find us on Google Groups at https://groups.google.com/group/wordnik-api , @wordnikapi on Twitter, or on #wordnik on IRC.

## Basic Setup

You should be able to install using `easy_install` or `pip` in the usual ways:

```sh
$ easy_install wordnik
$ pip install wordnik
```

Or just clone this repository and place the `wordnik` folder that you downloaded somewhere where it can be accessed by your scripts. Create a connection as follows:

```python
from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'YOUR API KEY HERE'
client = swagger.ApiClient(apiKey, apiUrl)
```

You'll want to substitute your own personal API key, of course. If you don't have an API key yet, you can get one here: http://developer.wordnik.com/ .

## Calling a Method

Once you have a client set up, you need to instantiate an API object for whichever category or categories of items you are interested in working with. For example, to work with the `word` API and apply the method `getTopExample` method, you can do the following:

```python
wordApi = WordApi.WordApi(client)
example = wordApi.getTopExample('irony')
print example.text
```

To find out what arguments the method expects, consult the online, interactive documentation at http://developer.wordnik.com/docs , and also check out the method definitions in `wordnik/WordApi.py`.

You can find out what fields to expect in the return value by using the interactive docs. You can also check out the tests in the `tests/` folder in this repository; each method is shown and tested there. In this case, the documentation in `WordAPI.py` shows that `getTopExample` returns an instance of `Example`, so you would examine that class in `wordnik/models/Example.py`.

Some methods, like `getDefinitions`, also take optional keyword parameters which should be specified by name. Again, these are shown in the online documentation and in the method defintions.

```python
wordApi = WordApi.WordApi(client)
definitions = wordApi.getDefinitions('badger',
                                     partOfSpeech='verb',
                                     sourceDictionaries='wiktionary',
                                     limit=1)
print definitions[0].text
```

The variable `definitions` is now an list of instances of the `Definition` class defined in `wordnik/models/Definition.py`, as indicated in the documentation for `getDefinition`.


## Testing

The tests require you to set three environment variables:

```sh
$ export API_KEY=your api key
$ export USER_NAME=some wordnik.com username
$ export PASSWORD=the user's password
```

The tests can be run as follows:

```sh
$ python tests/BaseApiTest.py
```

License
-------

Copyright 2013 Reverb Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
