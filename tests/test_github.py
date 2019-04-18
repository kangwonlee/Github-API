import ast
import urllib.parse as up

import pytest

import pyapi


@pytest.fixture
def get_auth(capsys):

    with capsys.disabled():
        auth = pyapi.get_basic_auth()

    return auth


def test_get_repo_comments_public():
    result = pyapi.get_repo_pr_comments_public('octocat', 'Hello-World')
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


def test_url_repo_comments():
    owner = 'octocat'
    repo = 'Hello-World'

    parse = up.urlparse(pyapi.get_url_repo_pr_comments(owner, repo))

    assert 'https' == parse.scheme
    assert parse.netloc.endswith('github.com')
    assert owner in parse.path
    assert repo in parse.path


def test_req_to_df_unpack_dict():
    list_nested_dict = [
        {'a1': 'a1 str', 'b1': {'c1': 'b1.c1 str', 'd1': 'b1.d1 str'}},
        {'a2': 'a2 str', 'b2': {'c2': 'b2.c2 str', 'd2': 'b2.d2 str'}},
        {'a3': 'a3 str', 'b3': {'c3': 'b3.c3 str', 'd3': 'b3.d3 str'}},
        {'a4': 'a4 str', 'b4': {'c4': 'b4.c4 str', 'd4': 'b4.d4 str'}},
    ]

    result = pyapi.unpack_list_of_nested_dict(list_nested_dict)

    expected = [
        {'a1': 'a1 str', 'b1.c1': 'b1.c1 str', 'b1.d1': 'b1.d1 str'},
        {'a2': 'a2 str', 'b2.c2': 'b2.c2 str', 'b2.d2': 'b2.d2 str'},
        {'a3': 'a3 str', 'b3.c3': 'b3.c3 str', 'b3.d3': 'b3.d3 str'},
        {'a4': 'a4 str', 'b4.c4': 'b4.c4 str', 'b4.d4': 'b4.d4 str'},
    ]

    for row_result, row_expected in zip(result, expected):
        assert row_result == row_expected


def test_post_repo_commit_comment(get_auth):
    """
    Please run this test with disabling capture

    =======
    Example
    =======
    $ pytest -s tests
    """

    # test info
    with open('test_post_repo_commit_comment_info.txt', 'r') as f:
        info = [line.strip() for line in f.readlines()]

    post_info = ast.literal_eval(info[-1])

    github = pyapi.GitHub(api_auth=get_auth)

    post_result = github.post_repo_commit_comment(
            owner=post_info['owner'],
            repo=post_info['repo'],
            sha=post_info['sha'],
            comment_str='test ok?',
    )

    assert not post_result.content.strip().endswith(b'[401]'), 'Not authorized'
