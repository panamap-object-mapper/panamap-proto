import pkg_resources

__version__ = pkg_resources.resource_string(__name__, 'panamap-proto.version').decode('utf-8').strip()

