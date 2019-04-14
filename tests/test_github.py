import pytest

import pyapi


def test_get_repo_comments_public():
    result = pyapi.get_repo_comments_public('octocat', 'Hello-World')
    
