# presentation-evaluation

Веб-приложение, созданное для оценки презентаций с помощью моделей машинного обучения. Приложение поддерживает загрузку презентаций в форматах PPTX или PDF, анализ их содержания, структуры и шрифтов (для PPTX), а также генерацию отчетов в форматах DOCX и PDF.

## Возможности

**Загрузка и анализ презентаций**:
- Поддержка файлов форматов PPTX и PDF
  
**Оценка с помощью ИИ**:
- Интеграция с несколькими моделями ИИ (например, Meta Llama, Mistral, Google Gemma, Qwen)
- Возможность настройки запроса для индивидуальной оценки
- Генерация подробных отчетов с анализом структуры, содержания и рекомендациями по улучшению

**Генерация отчетов**:
- Реализована возможность скачивания отчётов в форматах DOCX и PDF

**Пользовательский интерфейс**:
- Удобный и интуитивный веб-интерфейс
- Имеет две вкладки: одна для загрузки презентаций и выбора модели ИИ, другая для настройки текста запроса
- Поддерживает светлую и темную темы с динамической сменой логотипа

**Облачное развертывание**:
- Доступно по адресу [ http://62.84.122.115](http://62.84.122.115/)

## Требования

- **Python 3.10+**: Необходим для локального запуска приложения;
- **Ключ API OpenRouter**: Получите ключ API на [OpenRouter](https://openrouter.ai/) и установите его в переменную окружения `OPENAI_API_KEY`;
- **Зависимости**: Установите библиотеки, указанные в файлах `frontend/requirements.txt`, `backend/requirements.txt` и `tests/requirements.txt`;
- **LibreOffice и Pandoc**: Требуются для конвертации файлов (PPTX/PDF в изображения, Markdown в DOCX/PDF);
- **Poppler**: Требуется для конвертации PDF в изображения.

## Установка и настройка

### Локальный запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/presentation-evaluation.git
   cd presentation-evaluation
   ```

2. Создайте и активируйте виртуальное окружение:
   ```
   python3 -m venv env
   source env/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -U -r frontend/requirements.txt
   pip install -U -r backend/requirements.txt
   ```

4. Установите ключ API OpenRouter:
   ```bash
   export OPENAI_API_KEY='your-openrouter-api-key'
   ```

5. Запустите приложение:
   ```
   python3 -m streamlit run frontend/app.py
   ```

6. Откройте приложение по адресу `http://localhost:8501`.

7. Деактивируйте виртуальное окружение после завершения:
   ```
   deactivate
   ```

### Запуск в Docker
1. Сборка Docker-образа 
```
docker build -t pe-ml .
```

2. Запуск контейнера Docker
```
docker run -d -p 80:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY pe-ml
```

3. Откройте приложение по адресу
```
http://localhost
```
 

### Запуск тестов для приложения
1. Создание виртуального окружения
```
python3 -m venv env
```

2. Активация виртуального окружения
```
source env/bin/activate
```

3. Установка/обновление зависимостей
```
pip install -U -r frontend/requirements.txt
pip install -U -r backend/requirements.txt
pip install -U -r tests/requirements.txt
```
4. Запуск тестов
```
coverage run -m pytest -v -s
```

5. Запуск flake8
```
flake8 || echo
```

6. Деактивация виртуального окружения
```
deactivate
```


## Использование

1. **Загрузка презентации**:
   - Перейдите на вкладку "Загрузка";
   - Загрузите файл в формате PPTX или PDF;
   - Выберите модель ИИ из выпадающего списка (например, Meta Llama 4 Maverick);
   - Нажмите "Отправить презентацию" для обработки файла;
   - Примечание: Анализ шрифтов поддерживается только для файлов PPTX.

2. **Настройка запроса**:
   - Перейдите на вкладку "Текст запроса";
   - Отредактируйте текст запроса по умолчанию для настройки критериев оценки;
   - Нажмите "Изменить текст запроса" для сохранения изменений.

3. **Просмотр и скачивание отчетов**:
   - После обработки просмотрите отчет об оценке в разделе "Отчет";
   - Скачайте отчет в формате DOCX или PDF с помощью соответствующих кнопок.

## Примечания

- Убедитесь, что на системе установлены LibreOffice, Pandoc и Poppler для конвертации файлов;
- Для работы приложения требуется активное интернет-соединение для взаимодействия с API OpenRouter.