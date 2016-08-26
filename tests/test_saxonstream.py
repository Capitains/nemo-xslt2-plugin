from nemo_xslttwo_plugin import SaxonStreamTransform
from unittest import TestCase, mock
import logging
from capitains_nautilus.flask_ext import NautilusRetriever
from flask_nemo import Nemo
from flask import Flask
from werkzeug.contrib.cache import FileSystemCache


class TestSaxonStream(TestCase):

    def setUp(self):
        self.cache = FileSystemCache("./cache")
        self.saxon = SaxonStreamTransform(
            "./jars/saxon.jar",
            "./tests/data/xsl/ciham.xsl",
            cache=self.cache
        )
        self.nautilus = NautilusRetriever(
            folders=[
                "./tests/data/repo"
            ]
        )
        self.nautilus.logger.setLevel(logging.ERROR)

        app = Flask("Nemo")
        app.debug = True
        nemo = Nemo(
            app=app,
            base_url="",
            retriever=self.nautilus,
            transform={
                "default": self.saxon.transform
            }
        )

        self.client = app.test_client()

    def tearDown(self):
        # We clean the cache folder to ensure that no cache is passed from one test to the other
        self.cache.clear()

    def test_simple_transformation(self):
        """ Test transformation works fine"""
        read = self.client.get("/read/froLit/jns915/jns1856/ciham-fro1/1")
        data = read.data.decode()
        self.assertIn(
            '<span class="expan">et </span>', data,
            "Text content should be transformed"
        )
        self.assertIn(
            'Facsimilaire', data,
            "Other content should be added"
        )

        cached = self.cache.get("urn:cts:froLit:jns915.jns1856.ciham-fro1:1").decode()
        self.assertIn('<aside class="text-left">', cached, "Assert cache is made")

    def test_cache_retrieved(self):
        """ Test that cache is nicely used and built """
        read = self.client.get("/read/froLit/jns915/jns1856/ciham-fro1/1")
        data = read.data.decode()
        self.assertIn(
            '<span class="expan">et </span>', data,
            "Text content should be transformed"
        )
        self.assertIn(
            'Facsimilaire', data,
            "Other content should be added"
        )

        cached = self.cache.get("urn:cts:froLit:jns915.jns1856.ciham-fro1:1").decode()
        self.assertIn('<aside class="text-left">', cached, "Assert cache is made")

        with mock.patch("nemo_xslttwo_plugin.shell") as shell:
            read = self.client.get("/read/froLit/jns915/jns1856/ciham-fro1/1")
            cached_response = read.data.decode()
            self.assertEqual(
                cached_response, data,
                "Text content should the same in cache"
            )
            self.assertEqual(
                shell.call_count, 0,
                "Shell should not be called because we use cache"
            )

    def test_two_transformations(self):
        """ Test transformation works fine"""
        read = self.client.get("/read/froLit/jns915/jns1856/ciham-fro1/1")
        read = self.client.get("/read/froLit/jns915/jns1856/ciham-fro1/2")
        data = read.data.decode()
        self.assertIn(
            '<span class="expan">et </span>', data,
            "Text content should be transformed"
        )
        self.assertIn(
            'Facsimilaire', data,
            "Other content should be added"
        )

        cached = self.cache.get("urn:cts:froLit:jns915.jns1856.ciham-fro1:1").decode()
        self.assertIn('<aside class="text-left">', cached, "Assert cache is made")