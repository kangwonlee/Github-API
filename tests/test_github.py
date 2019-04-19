import ast
import json
import tempfile
import urllib.parse as up

import pytest

import pyapi


@pytest.fixture(scope='module')
def get_auth():

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

    response_dict = json.loads(post_result.content)

    assert isinstance(response_dict, dict), type(response_dict)

    expected_keys = [
        "html_url", "url", "id", "node_id", "body", "path", 
        "position", "line", "commit_id", "user", "created_at", "updated_at",        
    ]
    assert all(key in response_dict for key in expected_keys), post_result


def test_post_repo_issue_comment(get_auth):
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

    post_info = ast.literal_eval(info[-2])

    github = pyapi.GitHub(api_auth=get_auth)

    post_result = github.post_repo_issue_comment(
            owner=post_info['owner'],
            repo=post_info['repo'],
            issue_number=post_info['issue_no'],
            comment_str='test ok?',
    )

    assert not post_result.content.strip().endswith(b'[401]'), 'Not authorized'

    response_dict = json.loads(post_result.content)

    assert isinstance(response_dict, dict), type(response_dict)

    expected_keys = [
        "id", "node_id", "url", "html_url", "body", 
        "user", "created_at", "updated_at", 
    ]
    assert all(key in response_dict for key in expected_keys), post_result


@pytest.fixture
def sample_todo_list():
    sample_dict_0 = {'a': 'bc', 'de': 'fg'}
    sample_dict_1 = {'hi': 'jk', 'lm': 'no'}

    sample_todo_list = [
        sample_dict_0,
        sample_dict_1
    ]

    return sample_todo_list


def test_get_todo_list(sample_todo_list, get_auth):

    # get temp file name
    with tempfile.NamedTemporaryFile(mode='wt') as temp_name:
        temp_file_name = temp_name.name

    # write to the temp file
    with open(temp_file_name, mode='wt') as temp_write:
        json.dump(sample_todo_list, temp_write)

    # open to test
    result = pyapi.get_todo_list(temp_file_name)
    assert len(result) == len(sample_todo_list)
    for result_dict, expected_dict in zip(result, sample_todo_list):
        assert result_dict == expected_dict


def test_GitHubToDo_constructor(sample_todo_list, get_auth):

    todo_processor = pyapi.GitHubToDo(
        todo_list=sample_todo_list,
        api_auth=get_auth,
    )

    assert hasattr(todo_processor, 'session')
