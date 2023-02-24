import re

import pytest

from tor.movies import Movies


@pytest.fixture
def root_movie():
    return Movies()

@pytest.fixture
def movie_quotes():
    return Movies(quotes=True)


class TestMovieOverrides:

    def test_movie_attributes(self, root_movie):
        """Verify that Movies have their special values set properly"""
        assert root_movie.RESOURCE == 'movie'
        assert root_movie.SUB_RESOURCES == ['quote']

    def test_quote_query(self, movie_quotes):
        """"Verify that a quote query for Movies is internally set properly"""
        assert movie_quotes.sub_resource == 'quote'
