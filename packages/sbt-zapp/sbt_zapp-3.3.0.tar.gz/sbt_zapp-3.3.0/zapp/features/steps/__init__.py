from zapp.features.core.settings import LOCATORS_DIR, LOCATORS_FILE_POSTFIX
from zapp.features.core.utils import import_locators


_LOCATORS = import_locators()

_EM_LOCATOR_NOT_FOUND = "Не найден локатор с именем {}. Убедитесь, что локатор добавлен в один из файлов {}*{}"


def locator(target: str) -> str:
    result = _LOCATORS.get(target, None)
    if result is None:
        raise AttributeError(
            _EM_LOCATOR_NOT_FOUND.format(target, LOCATORS_DIR, LOCATORS_FILE_POSTFIX)
        )
    return result
