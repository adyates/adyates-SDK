# pylint: disable=W0621,R0201
import re

import pytest
import requests 

from tor.base import _TORResource

@pytest.fixture
def two_towers():
    """Raw result for Two Towers"""
    return {
        "docs": [
            {
                "_id": "5cd95395de30eff6ebccde5b",
                "name": "The Two Towers",
                "runtimeInMinutes": 179,
                "budgetInMillions": 94,
                "boxOfficeRevenueInMillions": 926,
                "academyAwardNominations": 6,
                "academyAwardWins": 2,
                "rottenTomatoesScore": 96
            }
        ],
        "total": 1,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1
    }
    
@pytest.fixture
def movies():
    """Raw result for all movies"""
    return {
        "docs": [
            {
                "_id": "5cd95395de30eff6ebccde56",
                "name": "The Lord of the Rings Series",
                "runtimeInMinutes": 558,
                "budgetInMillions": 281,
                "boxOfficeRevenueInMillions": 2917,
                "academyAwardNominations": 30,
                "academyAwardWins": 17,
                "rottenTomatoesScore": 94
            },
            {
                "_id": "5cd95395de30eff6ebccde57",
                "name": "The Hobbit Series",
                "runtimeInMinutes": 462,
                "budgetInMillions": 675,
                "boxOfficeRevenueInMillions": 2932,
                "academyAwardNominations": 7,
                "academyAwardWins": 1,
                "rottenTomatoesScore": 66.33333333
            },
            {
                "_id": "5cd95395de30eff6ebccde58",
                "name": "The Unexpected Journey",
                "runtimeInMinutes": 169,
                "budgetInMillions": 200,
                "boxOfficeRevenueInMillions": 1021,
                "academyAwardNominations": 3,
                "academyAwardWins": 1,
                "rottenTomatoesScore": 64
            },
            {
                "_id": "5cd95395de30eff6ebccde59",
                "name": "The Desolation of Smaug",
                "runtimeInMinutes": 161,
                "budgetInMillions": 217,
                "boxOfficeRevenueInMillions": 958.4,
                "academyAwardNominations": 3,
                "academyAwardWins": 0,
                "rottenTomatoesScore": 75
            },
            {
                "_id": "5cd95395de30eff6ebccde5a",
                "name": "The Battle of the Five Armies",
                "runtimeInMinutes": 144,
                "budgetInMillions": 250,
                "boxOfficeRevenueInMillions": 956,
                "academyAwardNominations": 1,
                "academyAwardWins": 0,
                "rottenTomatoesScore": 60
            },
            {
                "_id": "5cd95395de30eff6ebccde5b",
                "name": "The Two Towers",
                "runtimeInMinutes": 179,
                "budgetInMillions": 94,
                "boxOfficeRevenueInMillions": 926,
                "academyAwardNominations": 6,
                "academyAwardWins": 2,
                "rottenTomatoesScore": 96
            },
            {
                "_id": "5cd95395de30eff6ebccde5c",
                "name": "The Fellowship of the Ring",
                "runtimeInMinutes": 178,
                "budgetInMillions": 93,
                "boxOfficeRevenueInMillions": 871.5,
                "academyAwardNominations": 13,
                "academyAwardWins": 4,
                "rottenTomatoesScore": 91
            },
            {
                "_id": "5cd95395de30eff6ebccde5d",
                "name": "The Return of the King",
                "runtimeInMinutes": 201,
                "budgetInMillions": 94,
                "boxOfficeRevenueInMillions": 1120,
                "academyAwardNominations": 11,
                "academyAwardWins": 11,
                "rottenTomatoesScore": 95
            }
        ],
        "total": 8,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1
    }

@pytest.fixture
def base_root_query():
    """Instantiated version of the base class with some placeholders"""
    base =  _TORResource()
    base.RESOURCE = 'test'
    base.SUB_RESOURCES = ['testing']
    return base

@pytest.fixture
def base_id_query():
    """Instantiated version of the base class with some placeholders"""
    base =  _TORResource(id='sample')
    base.RESOURCE = 'test'
    base.SUB_RESOURCES = ['testing']
    return base

@pytest.fixture
def base_sub_query():
    """Instantiated version of the base class with some placeholders"""
    base =  _TORResource(id='sample')
    base.RESOURCE = 'test'
    base.SUB_RESOURCES = ['testing']
    base.sub_resource = 'testing'
    return base

class TestBaseUrlBuilder:
    """Test building the URL from base parts"""

    def test_base_collection_query(self, base_root_query):
        """Verify the root collection can be built"""
        test_url = base_root_query._build_url()
        assert test_url == 'https://the-one-api.dev/v2/test'

    def test_base_collection_query(self, base_id_query):
        """Verify the id query can be built"""
        test_url = base_id_query._build_url()
        assert test_url == 'https://the-one-api.dev/v2/test/sample'

    def test_base_collection_query(self, base_sub_query):
        """Verify the deep collection can be built"""
        test_url = base_sub_query._build_url()
        assert test_url == 'https://the-one-api.dev/v2/test/sample/testing'

    def test_invalid_collection_query(self, base_sub_query):
        """Verify a bad deep collection throws an error"""
        base_sub_query.sub_resource = 'error'
        with pytest.raises(
                requests.RequestException, 
                match='Invalid URL used: https://the-one-api.dev/v2/test/sample/error'
            ):
            test_url = base_sub_query._build_url()

class TestBasePaginationBuilder:

    def test_empty_pagination(self, base_root_query):
        """Verify unused pagination is fine"""
        base_root_query._validate_pagination()
        assert True

    def test_simple_limit_pagination(self, base_root_query):
        """Verify limit pagination is fine"""
        base_root_query.pagination = {'limit': 10}
        base_root_query._validate_pagination()
        assert True

    def test_broken_pagination(self, base_root_query):
        """Verify weird pagination breaks"""
        base_root_query.pagination = {'pointer': 'ad3edef'}
        with pytest.raises(
                requests.RequestException, 
                match=re.escape("Invalid pagination keys used: ['pointer']")
            ):
            base_root_query._validate_pagination()
        
class TestBaseFilterConversion:

    def test_empty_filtering(self, base_root_query):
        """Verify no filtering options returns an empty dict"""
        assert base_root_query._convert_filtering() == {}

    def test_isolated_filtering(self, base_root_query):
        """Verify simple filtering option (e.g. lessThan) returns a dict with an empty key"""
        assert base_root_query._convert_filtering(['budgetInMillions<100']) == {'budgetInMillions<100': ''}

    def test_valued_filtering(self, base_root_query):
        """Verify parameterized filtering options (e.g. exists) returns a dict with correct pair"""
        assert base_root_query._convert_filtering(['name=Gandalf']) == {'name': 'Gandalf'}

    def test_invalid_filtering(self, base_root_query):
        """Verify badly formatted filtering options (e.g. '=') throws an error"""
        with pytest.raises(
                requests.RequestException, 
                match=re.escape("Malformed filter parameter '=' found.")
            ):
            base_root_query._convert_filtering(['='])

        with pytest.raises(
                requests.RequestException, 
                match=re.escape("Malformed filter parameter 'name=Frodo=Gandalf' found.")
            ):
            base_root_query._convert_filtering(['name=Frodo=Gandalf'])

class TestBaseFinalParams:

    def test_empty_collection(self, base_root_query):
        """Verify the parameters are properly emptywhen nothing is set"""
        assert base_root_query._collect_params({}) == {}

    def test_pagination_params(self, base_root_query):
        """Verify pagination combines properly"""
        base_root_query.pagination = {'limit': 10}
        assert base_root_query._collect_params({}) == {'limit': 10}

    def test_filtering_params(self, base_root_query):
        """Verify filtering combines properly"""
        filters = {
            'budgetInMillions<100': '',
            'name': 'Gandalf',
        }
        assert base_root_query._collect_params(filters) == {
            'budgetInMillions<100': '',
            'name': 'Gandalf',
        }

    def test_sortby_param(self, base_root_query):
        """Verify sortby is parameterized properly"""
        base_root_query.sortby = 'character:asc'
        assert base_root_query._collect_params({}) == {'sortby': 'character:asc'}

    def test_full_combination(self, base_root_query):
        """"Verify all three portions are combined properly"""
        base_root_query.pagination = {'page': 4}
        filters = {
            'budgetInMillions<100': '',
            'name': 'Gandalf',
        }
        base_root_query.sortby = 'character:asc'
        assert base_root_query._collect_params(filters) == {
            'page': 4,
            'budgetInMillions<100': '',
            'name': 'Gandalf',
            'sortby': 'character:asc'
        }


@pytest.mark.skip(reason="I'd like to get this published and I haven't mocked Python in a hot minute")
class TestRequestParsing:
    """Doing this correctly would use PyMock or similar, but you'll get the point regardless"""

    def test_authentication(self, base_root_query):
        """Verify the request header has the environmental key"""
        # Stub out requests.get() and r.raise_for_status() (to no-op)
        # assert mock_request.args[0] == {'Authorization': 'Bearer testToken'}

    def test_results(self, base_root_query, two_towers):
        """Verify successful results are parsed properly"""
        # Stub out requests.get() and r.raise_for_status() (to no-op)
        # assert self.results and self.meta are correct based on two_towers fixture

