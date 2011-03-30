#!/usr/bin/env python

import unittest
import wordnik
import urllib2

def fake_do_http(uri, headers, body=None, method="GET", beta=False):
    return """{ "fakeKey": "fakeValue", "token": "deadbeef" }"""

def fake_fail_http(uri, headers, body=None, method="GET", beta=False):
    return None

class TestWordnikModule(unittest.TestCase):
    def setUp(self):
        self.key    = 'deadbeef'
        self.w      = wordnik.Wordnik(api_key=self.key)
        

    def test_bad_init(self):
        self.assertRaises(wordnik.NoAPIKey,
                          wordnik.Wordnik)

    def test_internals(self):
        self.assertEqual(wordnik.DEFAULT_FORMAT, 'json')
        self.assertEqual(wordnik.DEFAULT_URL, 'http://api.wordnik.com/v4')
        self.assertEqual(self.w._api_key, self.key)

    def test_methods(self):
        self.assertEqual(type(self.w.word_get), type(self.w.__init__))

class TestWordnikAPIMethods(unittest.TestCase):
    def setUp(self):
        self.key        = 'deadbeef'
        self.w          = wordnik.Wordnik(api_key=self.key)
        self.w._do_http = fake_do_http
        self.response   = fake_do_http(None, None)

    def test_account_methods(self):
        self.assertEqual(self.w.account_get_api_token_status(),self.response)

        self.assertRaises(wordnik.MissingParameters,self.w.account_get_authenticate)
        self.assertRaises(wordnik.MissingParameters,self.w.account_get_authenticate, "user")
        self.assertEqual(self.w.account_get_authenticate("testuser", password="testpass"),self.response)
                
        self.assertRaises(wordnik.MissingParameters,self.w.account_get_user)
        self.assertEqual(self.w.account_get_user(auth_token="eee"),self.response)

        self.assertRaises(wordnik.MissingParameters,self.w.account_post_authenticate)
        self.assertRaises(wordnik.MissingParameters,self.w.account_post_authenticate, "testuser")
        self.assertEqual(self.w.account_post_authenticate("testuser", body={}),self.response)

    def test_authenticate(self):
        self.assertRaises(TypeError, self.w.authenticate)
        self.assertEqual(self.w.authenticate("user", "pass"), True)
        
    def test_multi(self):
        ## XXX This needs to be done; multi() might need to get rewritten
        pass

    # def test_user_methods(self):
    # 
    #             
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_get_word_of_the_day_list)
    #     self.assertEqual(self.w.user_get_word_of_the_day_list("user"),self.response)
    # 
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_post_word_of_the_day_list)
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_post_word_of_the_day_list, "user")
    #     self.assertEqual(self.w.user_post_word_of_the_day_list("user", "link", body={}),self.response)
    # 
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_put_word_of_the_day_list)
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_put_word_of_the_day_list, "user")
    #     self.assertEqual(self.w.user_put_word_of_the_day_list("user", "link", body={}),self.response)
    # 
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_put_word_of_the_day_list_add)
    #     self.assertRaises(wordnik.MissingParameters,self.w.user_put_word_of_the_day_list_add, "user")
    #     self.assertEqual(self.w.user_put_word_of_the_day_list_add("user", "link", body={}),self.response)

    def test_word_methods(self):
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get)
        self.assertEqual(self.w.word_get("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_audio)
        self.assertEqual(self.w.word_get_audio("cat"),self.response)
          
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_definitions)
        self.assertEqual(self.w.word_get_definitions("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_examples)
        self.assertEqual(self.w.word_get_examples("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_frequency)
        self.assertEqual(self.w.word_get_frequency("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_hyphenation)
        self.assertEqual(self.w.word_get_hyphenation("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_phrases)
        self.assertEqual(self.w.word_get_phrases("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_pronunciations)
        self.assertEqual(self.w.word_get_pronunciations("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_related)
        self.assertEqual(self.w.word_get_related("cat"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_get_top_example)
        self.assertEqual(self.w.word_get_top_example("cat"),self.response)
        
    
    def test_word_list_methods(self):

        self.assertRaises(wordnik.MissingParameters,self.w.word_list_delete)
        self.assertEqual(self.w.word_list_delete("808"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_list_get)
        self.assertEqual(self.w.word_list_get("808"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_list_get_words)
        self.assertEqual(self.w.word_list_get_words("808"),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_list_post_delete_words)
        self.assertRaises(wordnik.MissingParameters,self.w.word_list_post_delete_words, "808")
        self.assertEqual(self.w.word_list_post_delete_words("808", body={}),self.response)
        
        self.assertRaises(wordnik.MissingParameters,self.w.word_list_post_words)
        self.assertRaises(wordnik.MissingParameters,self.w.word_list_post_words, "808")
        self.assertEqual(self.w.word_list_post_words("808", body={}),self.response)
        
    def test_word_lists_methods(self):

        self.assertEqual(self.w.word_lists_get(),self.response)

        self.assertRaises(wordnik.MissingParameters,self.w.word_lists_post)
        self.assertEqual(self.w.word_lists_post(body={}),self.response)

    def test_words_methods(self):

        self.assertEqual(self.w.words_get_random_word(),self.response)

        self.assertEqual(self.w.words_get_random_words(),self.response)

        self.assertRaises(wordnik.MissingParameters,self.w.words_get_search)
        self.assertEqual(self.w.words_get_search(query="cat"),self.response)


if __name__ == "__main__":
    unittest.main()
  
