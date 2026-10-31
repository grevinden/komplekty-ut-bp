# Пробник — диагностика живой базы (УТ 11.5 и БП 3.0)

Внешняя обработка: ищет объекты комплектации по подстроке имени (конфигуранезависимо),
для найденных документов читает реквизиты, табличные части, движения по регистрам и
проводки; пишет `/tmp/opencode/diag_<ИмяКонфигурации>.json`, при проблемах —
`diag_progress.txt` (последний шаг), `.crash.txt` (незакрытое исключение),
`.error.txt` (не записан JSON). Сама завершает сеанс (`&НаКлиенте ПриОткрытии`).

Сборка и прогон (одна платформа 8.3.27, файловые базы):

```bash
P=/opt/1cv8/x86_64/8.3.27.2342/1cv8
export DISPLAY=:0   # для запуска ENTERPRISE из-под сессии с окнами

$P DESIGNER /F<база> /N"Администратор" /DisableStartupDialogs \
  /LoadExternalDataProcessorOrReportFromFiles <этот каталог>/Пробник.xml /tmp/Пробник.epf \
  /Out"/tmp/build.log"

$P ENTERPRISE /F<база> /N"Администратор" \
  /DisableStartupDialogs /DisableStartupMessages /Execute /tmp/Пробник.epf
```

Проверено: минимальная форма (пing в оба обработчика) собирается и отрабатывает;
полная версия в УТ 11.5.22.186 зависала без JSON — добавлены прогресс-лог и crash-файл.

Про формат XML: у `ExternalDataProcessor` первым ребёнком обязателен `<InternalInfo>`
с `<xr:GeneratedType ... category="Object">`; в `Properties` нет `UseStandardCommands`,
`ExtendedPresentation`, `Explanation`; без заполненного `DefaultForm` ключ `/Execute`
открывает пустую автоматическую форму, а не нашу.
