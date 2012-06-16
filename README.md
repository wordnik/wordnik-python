Wordnik Python Client
==========
This client has been generated using the Swagger code generator, which builds robust API clients and beautiful API documentation automatically. If you'd like to learn more about Swagger, visit http://swagger.wordnik.com/ (but you don't need to know anything about Swagger to simply use this API client for Wordnik, this page will tell get you up to speed on that account).

Basic Setup
-----
You can install the Wordnik API client using either `easy_install` or `pip`:

```
easy_install wordnik

pip install wordnik
```

Or you can download this repository and place the `wordnik` folder somewhere where it can be accessed by your scripts.

Create a new API connection as follows:

```
# If you installed manually, put the full path to the directory containing
# the wordnik directory into your sys.path, if necessary
import sys
sys.path.append('/parent/path')

from wordnik.api.APIClient import APIClient
import wordnik.model

api_key = 'YOUR API KEY HERE'

my_client = APIClient(api_key, 'http://api.wordnik.com/v4')
```

You'll want to edit those lines to reflect the full path to where you extracted the `wordnik` folder you downloaded, and to use your own personal API key.

Calling a Method
-----

Once you have a client set up, you need to instantiate an API object for whichever category or categories of items you are interested in working with. For example, to work with the `word` API and apply the method `getTopExample` method, you can do the following:

```
from wordnik.api.WordAPI import WordAPI
wordAPI = WordAPI(my_client)

example = wordAPI.getTopExample('irony')
print example.text
```

To find out what arguments the method expects, consult the online, interactive documentation at http://developer.wordnik.com/docs , and also check out the method definitions in `wordnik/api/word.php`. You can find out what fields to expect in the return value again by using the interactive docs, or by looking at the object which is returned by the method. In this case, the documentation in `WordAPI.py` shows that `getTopExample` returns an instance of `Example`, so you would examine that class in `wordnik/model/Example.py`.

Some methods like `getTopExample` take a few arguments corresponding to different method parameters. Some of our more complex methods instead take an input object as their parameter. This object is a container for the values for all of the various paremeters the method accepts. To use a method of this sort, first you instantiate its input object and then set whatever values you desire for the properties of that object, which correspond to the method parameters you can see in the online docs. You can find out the class of the input object you need to instantiate by examining the argument in the method definition.

Let's see an example using the `getDefinitions` method. Examining its definition in `WordAPI.php`:

```
	def getDefinitions(self, wordDefinitionsInput=None, ):
```

we see that it takes `wordDefinitionsInput` as its input, so we'll first instantiate an object of class `WordDefinitionsInput`.

```
input = wordnik.model.WordDefinitionsInput.WordDefinitionsInput()
```

Here `word` is a mandatory argument to the `getDefinitions` method, so we make sure to set that property on the input object after instantiating it. We'll also set a limit of 3 definitions.

```
input.word = 'tree'
input.limit = 3
definitions = wordAPI.getDefinitions(input)
```

The variable `$definitions` is now a list of instances of the `Definition` class defined in `wordnik/model/Definition.py`, as indicated in the documentation for `getDefinition`. These instances have all the properties that you'll see in the response body for that method call if you invoke it from the online documentation. For example, you can loop through and print all the definition texts:

```
for definition in definitions:
    print definition.text
```
