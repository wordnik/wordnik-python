#!/
#!/usr/bin/env python

import unittest
import wordnik
import urllib2

## please just trust me... D:
params = [{u'paramType': u'path', u'required': False, u'description': u'ID of WordOfTheDayList', u'name': u'date'}, {u'paramType': u'query', u'required': False, u'description': u'Returns future WordOfTheDay items', u'name': u'includeAll'}, {u'name': u'format', u'paramType': u'path', u'required': True, u'allowableValues': u'json,xml', u'defaultValue': u'json', u'description': u'API response format'}]

alt_params = [{u'paramType': u'path', u'required': False, u'description': u'ID of WordOfTheDayList', u'name': u'date'}, {u'paramType': u'query', u'required': True, u'description': u'Returns future WordOfTheDay items', u'name': u'includeAll'} ]

response = [] ## not currently used, so not tested
summary = "Generic function summary"
path = "/fake.{format}/{parameter}/path"

def fake_do_http(uri, headers, body=None, method="GET", beta=False):
    return """{ "fakeKey": "fakeValue" }"""

def fake_fail_http(uri, headers, body=None, method="GET", beta=False):
    return None

class TestHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.h = wordnik.helpers

    def test_generate_docs(self):
        expectedDoc = """Generic function summary
/fake.{format}/{parameter}/path

Path Parameters:
  date
  format

Other Parameters:
  includeAll
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

        self.assertEqual(type(fake_do_http), type(self.h.create_method("name", doc, params, path, "GET")))
        
    def test_process_args(self):

        self.assertRaises(TypeError, self.h.process_args, path)
        self.assertRaises(TypeError, self.h.process_args, path, params)
        self.assertRaises(TypeError, self.h.process_args, path, params, [])

        expectedPath = """/fake.json/fake%20Param/path?"""
        expectedHeaders = {}
        expectedBody = None

        self.assertEqual(self.h.process_args(path, params, [], { "parameter": "fake Param"} ),
                         (expectedPath, expectedHeaders, expectedBody) )
        
        expectedBody = '{"key": "value"}'        
        self.assertEqual(self.h.process_args(path, params, [], { "parameter": "fake Param", "body": {"key": "value"}} ),
                         (expectedPath, expectedHeaders, expectedBody) )
        expectedBody = None
        expectedPath = "/fake.json/fakeParam/path?includeAll=true&"
        
        self.assertRaises(wordnik.MissingParameters, self.h.process_args,path,alt_params,[],{ "parameter": "fakeParam"})
        self.assertEqual(self.h.process_args(path, alt_params, [], { "parameter": "fakeParam", "includeAll": "true" }  ),
                         (expectedPath, expectedHeaders, expectedBody) )

    def test_uncamel(self):
        self.assertEqual(self.h.uncamel("camelString"), "camel_string")
    
    def test_remove_params(self):
        self.assertEqual(self.h.remove_params("/test/{path}/with/{params}"), "/test//with/")
    
    def test_componentize(self):
        self.assertEqual(self.h.componentize("one_two_three"), ["one", "two", "three"])
        
    def test_normalize(self):
        self.assertRaises(TypeError, self.h.normalize)
        self.assertEqual(self.h.normalize(path, "get"), "fake_get_path")
    
    

if __name__ == "__main__":
    unittest.main()
  
