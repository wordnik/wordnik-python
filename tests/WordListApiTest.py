#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
import urllib2
import json
from pprint import pprint
from BaseApiTest import BaseApiTest

sys.path = ['./'] + sys.path
from wordnik import *


class WordListApiTest(BaseApiTest):

    def setUp(self):
        super(WordListApiTest, self).setUp()
        self.authToken = self.accountApi.authenticate(self.username,
                                                      self.password).token
        self.existingList = self.accountApi.getWordListsForLoggedInUser(self.authToken,
                                                                        limit=1)[0]

        from wordnik.models import WordList
        wordList = WordList.WordList()
        wordList.name = "my test list"
        wordList.type = "PUBLIC"
        wordList.description = "some words I want to play with"

    def testGetWordListByPermalink(self):
        res = self.wordListApi.getWordListByPermalink(self.existingList.permalink,
                                                      self.authToken)
        assert res, 'null getWordListByPermalink result'

    def testGetWordListByPermalink(self):
        res = self.wordListApi.getWordListByPermalink(self.existingList.permalink,
                                                      self.authToken)
        assert res, 'null getWordListByPermalink result'

    def testUpdateWordList(self):
        import time
        description = 'list updated at ' + str(time.time())
        self.existingList.description = description
        self.wordListApi.updateWordList(self.existingList.permalink,
                                        self.authToken, body=self.existingList)

        res = self.wordListApi.getWordListByPermalink(self.existingList.permalink,
                                                      self.authToken)

        assert res.description == description, 'did not update wordlist'

    def testAddWordsToWordList(self):
        from wordnik.models import StringValue
        wordsToAdd = []
        word1 = StringValue.StringValue()
        word1.word = "delicious"
        wordsToAdd.append(word1)
        word2 = StringValue.StringValue()
        word2.word = "tasty"
        wordsToAdd.append(word2)
        word3 = StringValue.StringValue()
        word3.word = "scrumptious"
        wordsToAdd.append(word3)
        word4 = StringValue.StringValue()
        word4.word = u"élan"
        wordsToAdd.append(word4)
        self.wordListApi.addWordsToWordList(self.existingList.permalink,
                                        self.authToken, body=wordsToAdd)

        res = self.wordListApi.getWordListWords(self.existingList.permalink,
                                                self.authToken)
        listSet = set([word.word for word in res])
        addedSet = set(["delicious", "tasty", "scrumptious", u"élan"])
        assert len(listSet.intersection(addedSet)) == 4, 'did not get added words'

    def testDeleteWordsFromList(self):
        from wordnik.models import StringValue
        wordsToRemove = []
        word1 = StringValue.StringValue()
        word1.word = "delicious"
        wordsToRemove.append(word1)
        word2 = StringValue.StringValue()
        word2.word = "tasty"
        wordsToRemove.append(word2)
        word3 = StringValue.StringValue()
        word3.word = "scrumptious"
        wordsToRemove.append(word3)
        word4 = StringValue.StringValue()
        word4.word = u"élan"
        wordsToRemove.append(word4)
        self.wordListApi.deleteWordsFromWordList(self.existingList.permalink,
                                                 self.authToken,
                                                 body=wordsToRemove)

        res = self.wordListApi.getWordListWords(self.existingList.permalink,
                                                self.authToken)
        listSet = set([word.word for word in res])
        addedSet = set(["delicious", "tasty", "scrumptious", u"élan", "élan"])
        assert len(listSet.intersection(addedSet)) == 0, 'did not get removed words'

    def testAddUnicodeWordsToWordList(self):
       from wordnik.models import StringValue
       wordsToAdd = []
       word1 = StringValue.StringValue()
       word1.word = u"délicieux"
       wordsToAdd.append(word1)
       word2 = StringValue.StringValue()
       word2.word = u"νόστιμος"
       wordsToAdd.append(word2)
       word3 = StringValue.StringValue()
       word3.word = u"великолепный"
       wordsToAdd.append(word3)
       self.wordListApi.addWordsToWordList(self.existingList.permalink,
                                       self.authToken, body=wordsToAdd)
 
       res = self.wordListApi.getWordListWords(self.existingList.permalink,
                                               self.authToken)
       listSet = set([word.word for word in res])
       addedSet = set([u"délicieux", u"νόστιμος", u"великолепный"])
       assert len(listSet.intersection(addedSet)) == 3, 'did not get added words'

    def testDeleteUnicodeWordsFromList(self):
       from wordnik.models import StringValue
       wordsToRemove = []
       word1 = StringValue.StringValue()
       word1.word = u"délicieux"
       wordsToRemove.append(word1)
       word2 = StringValue.StringValue()
       word2.word = u"νόστιμος"
       wordsToRemove.append(word2)
       word3 = StringValue.StringValue()
       word3.word = u"великолепный"
       wordsToRemove.append(word3)
       self.wordListApi.deleteWordsFromWordList(self.existingList.permalink,
                                                self.authToken,
                                                body=wordsToRemove)
 
       res = self.wordListApi.getWordListWords(self.existingList.permalink,
                                               self.authToken)
       listSet = set([word.word for word in res])
       addedSet = set([u"délicieux", u"νόστιμος", u"великолепный"])
       assert len(listSet.intersection(addedSet)) == 0, 'did not get removed words'

    def testAddUnicodeWordsToWordList(self):
        from wordnik.models import StringValue
        wordsToAdd = []
        word1 = StringValue.StringValue()
        word1.word = u"délicieux"
        wordsToAdd.append(word1)
        word2 = StringValue.StringValue()
        word2.word = u"νόστιμος"
        wordsToAdd.append(word2)
        word3 = StringValue.StringValue()
        word3.word = u"великолепный"
        wordsToAdd.append(word3)
        self.wordListApi.addWordsToWordList(self.existingList.permalink,
                                        self.authToken, body=wordsToAdd)

        res = self.wordListApi.getWordListWords(self.existingList.permalink,
                                                self.authToken)
        listSet = set([word.word for word in res])
        addedSet = set([u"délicieux", u"νόστιμος", u"великолепный"])
        assert len(listSet.intersection(addedSet)) == 3, 'did not get added words'

    def testDeleteUnicodeWordsFromList(self):
        from wordnik.models import StringValue
        wordsToRemove = []
        word1 = StringValue.StringValue()
        word1.word = u"délicieux"
        wordsToRemove.append(word1)
        word2 = StringValue.StringValue()
        word2.word = u"νόστιμος"
        wordsToRemove.append(word2)
        word3 = StringValue.StringValue()
        word3.word = u"великолепный"
        wordsToRemove.append(word3)
        self.wordListApi.deleteWordsFromWordList(self.existingList.permalink,
                                                 self.authToken,
                                                 body=wordsToRemove)

        res = self.wordListApi.getWordListWords(self.existingList.permalink,
                                                self.authToken)
        listSet = set([word.word for word in res])
        addedSet = set([u"délicieux", u"νόστιμος", u"великолепный"])
        assert len(listSet.intersection(addedSet)) == 0, 'did not get removed words'


if __name__ == "__main__":
    unittest.main()
