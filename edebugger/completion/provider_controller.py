import os

from edebugger.completion.extractor import Extractor
from edebugger.completion.provider import Provider


class ProviderController:
    def __init__(self):
        self.__providers = self.__create_providers()

    def __create_providers(self):
        db_file = os.path.join(os.path.dirname(__file__), "octave_symbols.db")
        extractor = Extractor()
        blocks = extractor.extract(db_file)
        providers = []

        for block in blocks:
            header, symbols = block.items()[0]
            provider = Provider(header, symbols)
            providers.append(provider)
        return providers

    def get_providers(self):
        return self.__providers
