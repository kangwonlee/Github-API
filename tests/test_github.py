import urllib.parse as up

import pytest

import pyapi


def test_get_repo_comments_public():
    result = pyapi.get_repo_comments_public('octocat', 'Hello-World')
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html#pandas.DataFrame.at

    id = result.at[result.index[-1], 'id']
    url = result.at[result.index[-1], 'url']
    parse = up.urlparse(url)
    # sample : ParseResult(
    #               scheme='https', 
    #               netloc='api.github.com', 
    #               path='/repos/octocat/Hello-World/pulls/comments/124412547', 
    #               params='', query='', fragment='')

    assert 'https' == parse.scheme
    assert parse.netloc.endswith('github.com')
    assert parse.path.endswith(str(id))
