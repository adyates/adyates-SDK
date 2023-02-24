"""Base class for handling all requests the same way"""

import functools

import requests
import tor

class _TORResource:
    
    # Base URL
    TOR_BASEURI = tor.TOR_URI

    # Authentication credentials
    TOR_APIKEY = tor.TOR_APIKEY

    # Endpoint for the resource
    RESOURCE = None

    # Allowable sub resources
    SUB_RESOURCES = []

    # Allowable pagination keys
    PAGINATION = ['limit', 'offset', 'page']

    def __init__(self, id=None, sub_resource=None, sortby=None, pagination={}, filters=[]):
        self.id = id
        self.sub_resource = sub_resource
        self.sortby = sortby
        self.pagination = pagination
        self.filters = filters

    def _convert_filtering(self, filters=[]):
        """Converts the filtering query into acceptable HTTP parameters for Requests.
        
        Paramaters:
        filters (str[]): List of filtering parameters as described by https://the-one-api.dev/documentation#5

        Returns:
        dict: An appropriate dictionary for use with the `params` keyword arg in `requests.get()`
        """
        params = {}
        for filter in filters:
            temp_filter = filter.split('=')
            print(temp_filter)
            if not temp_filter or len(temp_filter) > 2:
                # Raise an exception, because there's some '=' here that shouldn't be here
                raise requests.RequestException("Malformed filter parameter '%s' found." % filter)  
            elif len(temp_filter) == 1:
                # Standalone attribute, assign empty string
                params[temp_filter[0]] = ''
            elif len(temp_filter) == 2 and temp_filter[0] and temp_filter[1]:
                # Assigned attribute, assign the pair
                k, v = temp_filter
                params[k] =  v
            else:
                # We should never get here, but repeat the same error as above
                raise requests.RequestException("Malformed filter parameter '%s' found." % filter)  
        return params

    def _build_url(self):
        endpoint = self.RESOURCE
        url = '/'.join([self.TOR_BASEURI, endpoint])
        if self.id:
            # Add in the ID if it exists
            url = '/'.join([url, self.id])
            if self.sub_resource:
                # If there's an additional subresource (e.g. quotes for movies), add and check here
                url = '/'.join([url, self.sub_resource])
                if self.sub_resource not in self.SUB_RESOURCES:
                    raise requests.RequestException("Invalid URL used: %s" % url)
        return url
    
    def _validate_pagination(self):
        if self.pagination and not functools.reduce(
                lambda contains, k: contains and k in self.PAGINATION,
                self.pagination.keys(),
                True
            ):
            raise requests.RequestException(
                "Invalid pagination keys used: %s" % [
                    k for k in self.pagination.keys() if k not in self.PAGINATION]
                )

    def _collect_params(self, query_params):
        final_params = {}
        final_params.update(self.pagination)
        final_params.update(query_params)

        if self.sortby:
            final_params['sortby'] = self.sortby
        return final_params

    def get(self):

        # Construct the URL
        url = self._build_url()
        
        # Validate pagination
        self._validate_pagination()

        # Convery any filter parameters
        query_filters = self._convert_filtering(self.filters)

        # Construct the request
        headers = {
            'Authorization': 'Bearer %s' % self.TOR_APIKEY,
        }

        r = requests.get(url, headers=headers, params=self._collect_params(query_filters))
        r.raise_for_status()
        resp = r.json()
        self.results = resp['docs']

        # Remove the documents, keep the rest
        self.meta = { k:v for k, v in resp.items() if k != 'docs'}

        # Return self, so this can be used as a one-liner request
        return self

