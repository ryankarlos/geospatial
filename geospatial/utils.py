import logging
import os

import git
from geospatial.logging_config import logging_config

logger = logging_config("utils")


def set_working_dir_repo_root(func):
    """
    Decorator for checking whether the
    current working dir is set as root of repo.
    If not, changes the working dir to root of repo
    Returns
    -------
    """

    def inner(*args, **kwargs):

        git_repo = git.Repo(".", search_parent_directories=True)
        git_root = git_repo.working_tree_dir
        if os.getcwd() != git_root:
            logger.info(
                f"current working dir: {os.getcwd()},"
                f"is not correctly set as repo root, "
                f"so changing to {git_root}"
            )
            os.chdir(git_root)
        else:
            logger.info(
                f"current working dir correctly set as" f" repo root {os.getcwd()}"
            )
        result = func(*args, **kwargs)

        return result

    return inner
