import requests
import sys

def make_http_request(url, 
                       method='post', 
                       headers=None, 
                       params=None, 
                       data=None, 
                       auth=None):
    """
    Make an HTTP request and return a json object of the response.
    """

    try:
        request_method = requests.post if method == 'post' else requests.get
        res = request_method(url, 
                             headers=headers, 
                             params=params, 
                             data=data, 
                             auth=auth)
        responsejson = res.json()

        if res.status_code != 200:
            raise Exception(res.text)
    except ValueError:
        # if the response isn't JSON, .json() method 
        # will raise JSONDecodeError, which is a subclass of ValueError
        return res.text
    except Exception as err:
        raise
        # sys.exit(f'Error during HTTP request to {url}: {err}')
    return responsejson