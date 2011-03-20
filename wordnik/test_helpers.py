#!/
#!/usr/bin/env python

import unittest
import wordnik
import urllib2
from wordnik import Wordnik

## please just trust me... D:
params = {u'includeSuggestions': {u'paramType': u'query', u'required': False, u'description': u'Return suggestions (for correct spelling, case variants, etc.)', u'name': u'includeSuggestions'}, u'word': {u'paramType': u'path', u'required': True, u'description': u'String value of WordObject to return', u'name': u'word'}, u'useCanonical': {u'paramType': u'query', u'required': False, u'description': u"If true will try to return the correct word root ('cats' -> 'cat'). If false returns exactly what was requested.", u'name': u'useCanonical'}, u'format': {u'name': u'format', u'paramType': u'path', u'required': True, u'allowableValues': u'json,xml', u'defaultValue': u'json', u'description': u'API response format'}}

response = [] ## not currently used, so not tested
summary = "Generic function summary"
path = "/fake.{format}/{parameter}/path"

def fake_do_http(uri, headers, body=None):
    return """{ "fakeKey": "fakeValue" }"""

def fake_fail_http(uri, headers, body=None):
    return None

class TestHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.h = wordnik.helpers

    def test_generate_docs(self):
        expectedDoc = """Generic function summary
/fake.{format}/{parameter}/path

Path Parameters:
  word

Other Parameters:
  useCanonical
"""
        self.assertRaises(TypeError, self.h.generate_docs)
        self.assertRaises(TypeError, self.h.generate_docs, params)
        self.assertRaises(TypeError, self.h.generate_docs, params, response)
        self.assertRaises(TypeError, self.h.generate_docs, params, summary)

        self.assertEqual(self.h.generate_docs(params, response, summary, path), expectedDoc)

    def test_create_method(self):

        doc = self.h.generate_docs(params, response, summary, path)

        self.assertRaises(TypeError, self.h.create_method)
        self.assertRaises(TypeError, self.h.create_method, "name")
        self.assertRaises(TypeError, self.h.create_method, "name", doc)
        self.assertRaises(TypeError, self.h.create_method, "name", doc, params)

        self.assertEqual(type(fake_do_http), type(self.h.create_method("name", doc, params, path)))
        
    def test_process_args(self):

        self.assertRaises(TypeError, self.h.process_args, path)
        self.assertRaises(TypeError, self.h.process_args, path, params)
        self.assertRaises(TypeError, self.h.process_args, path, params, [])

        expectedPath = "/fake.json/fakeParam/path?"
        expectedHeaders = {}
        expectedBody = None

        self.assertEqual(self.h.process_args(path, params, [], { "parameter": "fakeParam"} ),
                         (expectedPath, expectedHeaders, expectedBody) )



if __name__ == "__main__":
    unittest.main()
  
