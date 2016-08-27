import abc
import os
import importlib
import six

from aumbry.errors import DependencyError


@six.add_metaclass(abc.ABCMeta)
class AbstractHandler(object):
    def __init__(self, options=None):
        self.options = options or {}

        self.vars = {}
        self.vars.update(self.environmental_vars)
        self.vars.update(self.options)

    @abc.abstractmethod
    def fetch_config_data(self):
        """ Retrieves configuration data from pre-configured location. """

    @abc.abstractmethod
    def deserialize(self, raw_config, config_cls):
        """ Method to handle deserialization to a Config object. """

    @abc.abstractmethod
    def serialize(self, config):
        """ Method to handle serialization to a string. """

    @abc.abstractproperty
    def environment_var_prefix(self):
        """ The prefix of all environmental variables to fetch. """

    @abc.abstractproperty
    def extras_name(self):
        """ The name of the extras package requirement. """

    @abc.abstractproperty
    def imports(self):
        """ List of modules to import. """

    def import_requirements(self):
        def _import(req, pkg=None):
            try:
                importlib.import_module(req, pkg)
            except:
                raise DependencyError(self.extras_name)

        for req in self.imports:
            if isinstance(req, six.text_type) or isinstance(req, str):
                _import(req)
            else:
                name, package = req
                _import(name, package)

    @property
    def environmental_vars(self):
        keys_to_fetch = [
            key for key in os.environ.keys()
            if key.startswith(self.environment_var_prefix)
        ]

        return {key: os.environ[key] for key in keys_to_fetch}