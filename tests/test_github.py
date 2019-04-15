import urllib.parse as up

import pytest

import pyapi


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


def test_post_repo_commit_comment(capsys):
    """
    Please run this test with disabling capture

    =======
    Example
    =======
    $ pytest -s tests
    """
    with capsys.disabled():
        df = pyapi.get_auth_df()
    
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html

        with open('test_post_repo_commit_comment_info.txt', 'r') as f:
            info = [line.strip() for line in f.readlines()]

        tested = False

        for row_i, row in df.iterrows():

            if info[0] in row['app']['name']:

                assert str(row['id']) in info

                tested = True

                print(
                    f"[{row_i:02d}]\n"
                    f"id : {row['id']}\n"
                    f"app.name : {row['app']['name']}\n"
                    f"app.url : {row['app']['url']}\n"
                    f"created_at : {row['created_at']}\n"
                    f"note : {row['note']}\n"
                    f"note_url : {row['note_url']}\n"
                    f"scopes : {row['scopes']}\n"
                    f"updated_at : {row['updated_at']}\n"
                    f"url : {row['url']}\n"
                )

        assert tested
