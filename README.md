# verbs_game

Два бота - для телеграм и vk, обученные нейросетью с помощью DialogFlow.

Отвечают на типичные вопросы клиентов, что позволяет сократить время ожидания ответа и повышает у сотрудников службы поддержки 
уровень удовлетворенности работой

![gif](https://dvmn.org/filer/canonical/1569214089/322/)

## Установка

Скачайте код:
```sh
git clone https://github.com/PaSeRouS/verbs_game.git
```

Перейдите в каталог проекта:
```sh
cd verbs_game
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Рекомендуем установить версию Python не ниже 3.10

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`.
Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

## Установка виртуального окружения и настройка зависимостей
В каталоге `verbs_game/` создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```
## Переменные окружения
В каталоге `verbs_game/` создайте файл `.env` для хранения переменных окружения

#### TG_TOKEN
* Через поиск телеграм найдите бот @BotFather. 
* Отправьте `/start` для получения списока всех его команд.
* Выберите команду /newbot - бот попросит придумать имя вашему новому боту. 
Необходимо создать два бота - основной бот и бот, который будет получать сообщения о логах
* Сохраните полученные токены в переменных `TELEGRAM_BOT_TOKEN` и LOGS_TELEGRAM_BOT_TOKEN в файле `.env`:

```
TELEGRAM_TOKEN=<Токен для основного бота>

LOGS_TELEGRAM_BOT_TOKEN = <Токен для бота логов>

```

#### LOGS_TELEGRAM_CHAT_ID
Чтобы получить свой chat_id, напишите в Telegram специальному боту: `@userinfobot`

Сохраните chat_id в переменной `LOGS_TELEGRAM_CHAT_ID` в файле `.env`:
```
LOGS_TELEGRAM_CHAT_ID=<Ваш chat_id>
```

#### VK_TOKEN
* Создайте группу во ВКонтакте
* В настройках группы выберите 'Работа с API'
* Создайте ключ и скопируйте его в файл `.env`

```
VK_TOKEN=<Созданный ключ>
```

#### PROJECT_ID

Создайте проект в [DialogFlow](https://dialogflow.cloud.google.com/#/login).<br>

[Как создать проект в DialogFlow?](https://cloud.google.com/dialogflow/docs/quick/setup)<br>

Полученный идентификатор проекта сохраните его в переменной `PROJECT_ID` в файле `.env`

```
PROJECT_ID=<индентификатор проекта>
```

Создайте агента в DialogFlow. [Как создать агента?](https://cloud.google.com/dialogflow/docs/quick/build-agent)

Обязательно выбирайте русский язык, иначе бот не будет понимать ваши фразы. Отдельно проверьте, что ProjectID совпадает с ID от вашего проекта в Google Cloud

В итоге вы должны попасть на страницу, как на скриншоте:

![agent](https://dvmn.org/media/agent.png)

#### GOOGLE_APPLICATION_CREDENTIALS

* [Включите API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) DialogFlow на вашем Google-аккаунте
* Воспользуйтесь консольной утилитой [gloud](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk) для получения
файла `credentials.json` с ключами от вашего Google-аккаунта
* В файле `.env` сохраните переменную `GOOGLE_APPLICATION_CREDENTIALS` содержащую путь к полученному файлу `credentials.json`

```
GOOGLE_APPLICATION_CREDENTIALS='path/to/file'
```
### Обучите DialogFlow

Для обучения ИИ новым фразам необходимо подготовить json-файл вида:
```
{
    "Тема диалога_1": {
        "questions": [
            "Фраза пользователя",
            "Фраза пользователя"
        ],
        "answer": "Ответ вашего бота"
    },
    "Тема диалога_1": {
        "questions": [
            "Фраза пользователя",
            "Фраза пользователя"
        ],
        "answer": "Ответ вашего бота"
    }
}
```
Сохраните json-файл и укажите путь к нему в переменной `TRAINING_PHRASES_PATH` в файле `.env`

```
TRAINING_PHRASES_PATH='path/to/json'
```

Затем запустите команду для обучения:
```
python dialogflow_intent_creator.py
```

## Запуск ботов
#### Команды для запуска ботов
Телеграм:
```
python tg_bot.py
```
Вконтакте:
```
python vk_bot.py
```
 
