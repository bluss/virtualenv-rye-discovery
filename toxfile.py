import logging

from tox.plugin import impl


@impl
def tox_add_env_config(env_conf, state):
    "Setup rye discovery in virtualenv"
    logging.getLogger(__name__).info("Using virtualenv discovery = rye")
    env_conf["set_env"].update({"VIRTUALENV_DISCOVERY": "rye"})
