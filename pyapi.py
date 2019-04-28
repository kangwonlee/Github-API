# https://github.com/msaisushma/Github-API
# Dawson & Straub, Building Tools with GitHub
# Jason McVetta, Password Privacy, Generate a Github OAuth2 Token, https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy
# Ian Stapleton Cordasco, softvar, how to use github api token in python for requesting, 2013 July 13, https://stackoverflow.com/questions/17622439/how-to-use-github-api-token-in-python-for-requesting
# List comments in a repository, Review Comments, Pull Requests, REST API v3, https://developer.github.com/v3/pulls/comments/#list-comments-in-a-repository
# Authentication, Request, http://docs.python-requests.org/en/master/user/authentication/
# Create a comment, Comments, Issues, REST API v3, https://developer.github.com/v3/issues/comments/#create-a-comment
# Create a commit comment, Comments, Repositories, REST API v3, https://developer.github.com/v3/repos/comments/#create-a-commit-comment
# aknuds1, How do I add keyword arguments to a derived class's constructor in Python?, Stackoverflow, Oct 9 2016, https://stackoverflow.com/a/27472354
# Input, Create a commit comment, Comments, Repositories, REST API v3, https://developer.github.com/v3/repos/comments/#input
# Mark, How to format JSON data when writing to a file, Stackoverflow, Jul 9 '16, https://stackoverflow.com/questions/38283596/how-to-format-json-data-when-writing-to-a-file
# Authentication, Overview, REST API v3, https://developer.github.com/v3/#authentication

import getpass
import json
import os
import pprint
import sys
import urllib.parse as up

import pandas
import requests

api_url = "https://api.github.com/"
api_user_url = "https://api.github.com/users"


def get_basic(url=api_url):
    req = requests.get(url)
    pd = req_to_df(req)

    return pd


def req_to_df(req):
    resp = parse_req_json(req)

    if isinstance(resp, dict):
        resp = [resp]

    try:
        pd = pandas.DataFrame(resp)
    except BaseException as e:
        pprint.pprint(resp)
        raise e

    return pd


def parse_req_json(req):
    return json.loads(req.content)


def req_to_df_unpack_dict(req):
    """
    request to DataFrame unpacking nested dictionaries

    req : list of dictionaries (or nested dictionaries)
            [
               {'a1': 'a1 str', 'b1': {'c1': 'b1.c1 str'}},
               {'a2': 'a2 str', 'b2': {'c2': 'b2.c2 str'}},
               {'a3': 'a3 str', 'b3': {'c3': 'b3.c3 str'}},
               {'a4': 'a4 str', 'b4': {'c4': 'b4.c4 str'}},
            ]

    """

    resp = parse_req_json(req)

    # response check
    if isinstance(resp, dict):
        raise ValueError(f'dict : {resp}')

    # unpack nested dictionaries into simpler dictionaries
    rows = unpack_list_of_nested_dict(resp)

    try:
        pd = pandas.DataFrame(rows)
    except BaseException as e:
        pprint.pprint(rows)
        raise e

    return pd


def unpack_list_of_nested_dict(resp):
    # unpack nested dictionaries into simpler dictionaries
    rows = []
    for d in resp:
        row = {}
        for k in d.keys():
            keys = [k]
            if isinstance(d[k], dict):
                for dk in d[k]:
                    keys.append(dk)
                    # recursion possible?
                    row['.'.join(keys)] = d[k][dk]
                    keys.pop()
            else:
                row[k] = d[k]
        rows.append(row)
    return rows


def get_page_030():
    pd = get_basic()
    print(pd['current_user_url'])


def get_page_033():
    repos_url = '/'.join((api_user_url, 'xrd', 'repos'))

    pd = get_basic(repos_url)

    pprint.pprint(pd['owner'][0]['id'])


def get_page_039():
    # http://docs.python-requests.org/en/master/user/authentication/
    # https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

    df = get_auth_df()

    pprint.pprint(df)


def get_auth_df():
    """
    Please run this without capturing
    """

    api_auth_url = up.urljoin(api_url, 'authorizations')

    note = 'OAuth practice'  # input('Note (optional): ')
    payload = {}

    if note:
        payload['note'] = note

    df = req_to_df_unpack_dict(reg_get_auth(api_auth_url, payload))

    return df


def get_page_49():
    # http://docs.python-requests.org/en/master/user/authentication/
    # https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

    df = pandas.DataFrame.from_dict(get_rate_limit_response())

    pprint.pprint(df)


def get_rate_limit_response():
    # http://docs.python-requests.org/en/master/user/authentication/
    # https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

    api_auth_url = up.urljoin(api_url, 'rate_limit')

    note = 'rate check practice'  # input('Note (optional): ')
    payload = {}
    if note:
        payload['note'] = note

    response = parse_req_json(reg_get_auth(api_auth_url, payload))

    return response


def reg_get_auth(auth_url, payload):
    req = requests.get(
        auth_url,
        auth=get_basic_auth(),
        data=json.dumps(payload)
    )
    return req


def get_basic_auth():
    return requests.auth.HTTPBasicAuth(
        input('Github username: '),
        getpass.getpass('Github password: ')
    )


def get_repo_pr_comments_public(owner, repo, b_verbose=False):
    url = get_url_repo_pr_comments(owner, repo)
    if b_verbose:
        print(f'get_repos_public() : url = {url}')
    return(get_basic(url))


def get_url_repo_pr_comments(owner, repo):
    # https://developer.github.com/v3/pulls/comments/#list-comments-in-a-repository
    return up.urljoin(api_url, '/'.join(('repos', owner, repo, 'pulls', 'comments')))


class GitHub(object):
    """
    Ian Stapleton Cordasco, softvar, how to use github api token in python for requesting, 2013 July 13, https://stackoverflow.com/questions/17622439/how-to-use-github-api-token-in-python-for-requesting
    """

    def __init__(self, api_token=False, api_auth=False, api_url=False):
        self.api_token = api_token
        self.api_auth = api_auth
        self.api_url = api_url

        self.session = requests.Session()

        # authentication for self
        if self.api_token:
            self.session.headers['Authorization'] = f'token {self.api_token}'
        elif self.api_auth:
            self.session.auth = self.api_auth
        else:
            self.session.auth = get_basic_auth()

        if self.api_url:
            self.api_url = 'https://api.github.com/'

    def __del__(self):
        self.session.close()

    def call_to_the_api(self, *args):
        url = ''
        return self.session.post(url)

    def post_repo_issue_comment(self, owner, repo, issue_number, comment_str):
        """
        Post a comment to an issue of an owner's one repostory

        CAUTION : This may cause abuse rate limit.
        """
        url = self.url_repo_issue_comment(
            owner, repo, issue_number, comment_str)
        payload = self.payload_repo_issue_comment(body_str=comment_str)

        return self.session.post(url, json=payload)

    def url_repo_issue_comment(self, owner, repo, issue_number, comment_str):
        """
        For post_repo_issue_comment()
        POST /repos/:owner/:repo/issues/:issue_number/comments

        https://developer.github.com/v3/issues/comments/#create-a-comment

        CAUTION : This may cause abuse rate limit.
        """
        return up.urljoin(api_url, '/'.join(('repos', owner, repo, 'issues', issue_number, 'comments')))

    @staticmethod
    def payload_repo_issue_comment(body_str=False):
        """
        Prepare the payload for an issue comment

        {
            "body": "content here"
        }

        ref : https://developer.github.com/v3/issues/comments/#input
        """

        assert body_str

        result = {'body': body_str, }

        return result

    def post_repo_commit_comment(self, owner, repo, sha, comment_str, path_str=False, position_int=False):
        """
        Post a comment to a commit of an owner's one repostory
        POST /repos/:owner/:repo/commits/:sha/comments

        https://developer.github.com/v3/repos/comments/#create-a-commit-comment

        CAUTION : This may cause abuse rate limit.
        """
        url = url_repo_commit_comment(owner, repo, sha)
        payload = payload_repo_commit_comment(
            body_str=comment_str, path_str=path_str, position_int=position_int)

        return self.session.post(url, json=payload)


class GitHubToDo(GitHub):
    def __init__(self, **config_options):
        # https://stackoverflow.com/questions/27472250/how-do-i-add-keyword-arguments-to-a-derived-classs-constructor-in-python
        self.todo_list = config_options.pop('todo_list', [])

        super().__init__(**config_options)

        assert hasattr(self, 'todo_list'), "argument todo_list missing"

    def run_todo(self):
        response_list = []

        for todo_dict in self.todo_list:
            # TODO : more data centric coding possible?
            if 'issue_number' in todo_dict:
                response = self.post_repo_issue_comment(**todo_dict)
            elif 'sha' in todo_dict:
                response = self.post_repo_commit_comment(**todo_dict)
            else:
                raise NotImplementedError(repr(todo_dict))

            response_list.append(response)

        return response_list


def url_repo_commit_comment(owner, repo, sha):
    """
    POST /repos/:owner/:repo/commits/:sha/comments
    ref : https://developer.github.com/v3/repos/comments/#create-a-commit-comment
    """
    return up.urljoin(api_url, '/'.join(('repos', owner, repo, 'commits', sha, 'comments')))


def payload_repo_commit_comment(body_str=False, path_str=False, position_int=False):
    """
    Prepare the payload for a comment
    ref : https://developer.github.com/v3/repos/comments/#input
    """

    assert body_str

    result = {'body': body_str, }

    if path_str:
        result['path'] = str(path_str)

    if position_int:
        result['position'] = int(position_int)

    return result


def get_todo_list(json_filename):
    with open(json_filename) as json_file:
        todo_list = json.load(json_file)

    return todo_list


def process_todo_list_json_file(*todo_list_json_filename_list):

    todo_list = []

    for todo_list_json_filename in todo_list_json_filename_list:
        todo_list += get_todo_list(todo_list_json_filename)

    if todo_list:
        todo_processor = GitHubToDo(
            todo_list=todo_list,
            api_auth=get_basic_auth(),
        )
        response_list = todo_processor.run_todo()

        print(f'len(response_list) = {len(response_list)}')

        retry_list = []

        for todo_dict, response in zip(todo_list, response_list):
            # https://stackoverflow.com/questions/38283596/how-to-format-json-data-when-writing-to-a-file
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(f'todo_dict = {todo_dict}')
                print(f'response = {response}')
                print(f'response.json() = {response.json()}')
                retry_list.append(todo_dict)

        if retry_list:
            retry_todo_processor = GitHubToDo(
                todo_list=retry_list,
                api_auth=get_basic_auth(),
            )
            retry_response_list = retry_todo_processor.run_todo()

            retry_retry_list = []

            for todo_dict, response in zip(retry_list, retry_response_list):
                # https://stackoverflow.com/questions/38283596/how-to-format-json-data-when-writing-to-a-file
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    print(f'todo_dict = {todo_dict}')
                    print(f'response = {response}')
                    print(f'response.json() = {response.json()}')
                    retry_retry_list.append(todo_dict)

            print(f'len(retry_retry_list) = {len(retry_retry_list)}')


def main(argv):
    if argv:
        process_todo_list_json_file(*argv)
    else:
        print(f"usage : python {os.path.split(__file__)[-1]} <github id>")
        print(get_rate_limit_response())


def get_comments():
    usrname = input("Enter the username:")
    url = api_url+usrname+"/events"
    req = requests.get(url)
    resp = parse_req_json(req)

    pprint.pprint(resp)

    pload = [li['payload']for li in resp]
    payload = pload[3]
    # print payload

    for _, v in payload.items():
        print(v['html_url'])


if __name__ == '__main__':
    main(sys.argv[1:])
