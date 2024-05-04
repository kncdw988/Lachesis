from utils import Translater
from utils import const


class TestTranslater:

    def test_display_to_storage(self):
        translater = Translater(const.CaseFieldType)
        display = const.CaseFieldType.Display.STRING
        storage = translater.display_to_storage(display)
        assert storage == const.CaseFieldType.Storage.STRING

        display = const.CaseFieldType.Display.DATE
        storage = translater.display_to_storage(display)
        assert storage == const.CaseFieldType.Storage.DATE

    def test_storage_to_display(self):
        translater = Translater(const.CaseFieldType)
        storage = const.CaseFieldType.Storage.INT
        display = translater.storage_to_display(storage)
        assert display == const.CaseFieldType.Display.INT

        storage = const.CaseFieldType.Storage.FLOAT
        display = translater.storage_to_display(storage)
        assert display == const.CaseFieldType.Display.FLOAT
