import urllib.parse as up

import pytest

import pyapi


def test_get_repo_comments_public():
    result = pyapi.get_repo_comments_public('octocat', 'Hello-World')
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html#pandas.DataFrame.at

    id = result.at[result.index[-1], 'id']
    url = result.at[result.index[-1], 'url']
    parse = up.urlparse(url)

    assert 'https' == parse.scheme
    assert parse.path.endswith(str(id))
