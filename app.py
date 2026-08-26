"""
================================================================================
 ВЕБ-КВЕСТ (ЭСКЕЙП-РУМ): «Выявление и минимизация рисков экстремизма
 и деструктивной деятельности»
================================================================================

УСТАНОВКА И ЗАПУСК:
    1) Установите зависимости:
           pip install streamlit
    2) Запустите приложение командой:
           streamlit run app.py
       (или python main.py — он сам поднимет сервер и откроет браузер)

Приложение полностью самодостаточно и не требует внешних файлов/БД —
всё состояние хранится в st.session_state.
================================================================================
"""

import html
from pathlib import Path

import streamlit as st

# Плейсхолдер имени игрока внутри текстов сценариев уровней.
NAME_PLACEHOLDER = "<user_name>"
DEFAULT_NAME = "друг"

# --------------------------------------------------------------------------
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Квест: Безопасик",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="expanded",
)

DOG = "🐶🤖"  # персонаж-проводник — Безопасик

# Портрет маскота: файл должен лежать рядом с app.py.
# Если файла нет — вместо картинки показываем эмодзи-заглушку.
MASCOT_PATH = Path(__file__).resolve().parent / "mascot.png"
MASCOT_WIDTH = 100

# --------------------------------------------------------------------------
# ТЕКСТЫ ВСТУПЛЕНИЯ (ПРОЛОГ ОТ БЕЗОПАСИКА)
# --------------------------------------------------------------------------
INTRO_SCREEN_1 = f"""
Привет! Меня зовут Безопасик! {DOG}

Я не совсем обычный щенок. Когда-то меня создали как робота-помощника, чтобы я мог
путешествовать по цифровому миру и помогать людям находить безопасный путь.

Однажды во время своего путешествия я заметил, что в интернете существуют разные
ловушки. Иногда незнакомцы могут казаться добрыми и дружелюбными. Они обещают
подарки, лёгкие деньги, интересные задания или предлагают вступить в «секретную
команду».

Но я узнал важную вещь: <b>не каждый, кто кажется другом, действительно хочет тебе
добра.</b>

Некоторые люди могут пытаться обманом, хитростью или манипуляциями вовлечь детей
и подростков в опасные сообщества и противоправные действия.
"""

INTRO_SCREEN_2 = """
Тогда я решил создать свою особую миссию.

Вместе мы пройдём настоящий квест. Тебя ждут загадки, непростые ситуации,
неожиданные сообщения и важные решения.

Твоя задача — научиться замечать опасность, отличать правду от обмана и понимать,
что делать, если кто-то пытается втянуть тебя во что-то подозрительное или
опасное.

Но помни: <b>настоящая сила — не в том, чтобы рисковать. Настоящая сила — уметь
остановиться, подумать и попросить помощи.</b>

Готов? Тогда включаем режим безопасности! Миссия начинается! 🚀🐶🛡️
"""

INTRO_SCREEN_3_QUESTION = "«Хочешь начать игру?»"

INTRO_REPLY_YES = (
    "Отлично! Я знал, что ты смелый и любознательный! Впереди нас ждут настоящие "
    "приключения и важные уроки. Но помни: в игре, как и в жизни, важно быть "
    "внимательным и не поддаваться на уловки. Погнали! 🚀"
)

INTRO_REPLY_NO = (
    "Понимаю, может быть, ты немного волнуешься или сомневаешься. Это нормально! "
    "Но знаешь, эта игра поможет тебе стать увереннее и научит распознавать "
    "опасность. Давай попробуем, я буду рядом! Если захочешь остановиться в любой "
    "момент — всегда можно сделать паузу. Ну что, начнём? 😊"
)

# --------------------------------------------------------------------------
# ДАННЫЕ ДЛЯ УРОВНЯ 1: «ОШИБСЯ НОМЕРОМ» (вариативный диалог)
# --------------------------------------------------------------------------
LEVEL1_TITLE = "1️⃣ «Ошибся номером»"

LEVEL1_INTRO = (
    "Входящее сообщение от номера, которого нет в твоей телефонной книге. "
    "Незнакомец. Это не друг, не родственник, не учитель. Просто цифры на экране. "
    "Представь, что сейчас у тебя включились «Детектор чужаков» и «Вежливый дипломат»."
)

# Общая мини-лекция, которую Безопасик читает после ЛЮБОЙ концовки уровня.
LEVEL1_LECTURE = """
Запомни три правила из этого уровня:

1. Если номер незнакомый – ты не обязан отвечать. Но если ответил – не ври.
2. «Извините, вы ошиблись» – универсальная и безопасная фраза.
3. Не задавай лишних вопросов незнакомцу о нём или о себе – так ты не даёшь ему крючок для дальнейшего общения.

Это был лёгкий противник. Впереди будут хитрее. Ты готов?
""".strip()

# --------------------------------------------------------------------------
# Дерево диалога: каждый узел — это либо развилка (есть "choices"),
# либо концовка (есть "ending"). "next" в choices указывает id следующего узла.
# --------------------------------------------------------------------------
LEVEL1_NODES = {
    "start": {
        "stranger": "«Привет! Это <user_name>? Ты обещал перезвонить насчёт стройматериалов. "
                    "Когда будет удобно?»",
        "hint": "Он явно ошибся номером. Но ошибка — это тоже проверка. Как ты ответишь?",
        "choices": [
            ("«Извините, вы ошиблись. Я не <user_name>».", "end_gold",
             "Чётко, вежливо, без лишней информации. Ты ставишь точку, но не хлопаешь дверью."),
            ("«Да, это я, <user_name>. Рассказывай, что там?»", "branch2",
             "Ты врёшь незнакомцу. Ложь в интернете — как минное поле: не знаешь, куда наступишь. "
             "Сейчас это шутка, но террористы используют ложь, чтобы втянуть тебя в игру."),
            ("«Кто вы? Откуда у вас мой номер?»", "branch3",
             "Вопрос резонный, но звучит подозрительно. Ты не даёшь личного, но можешь обидеть "
             "человека, который просто ошибся."),
            ("«Отстаньте, не пишите мне больше».", "end_rude",
             "Грубость не спасает, а только портит впечатление. Вдруг это важный звонок для "
             "кого-то? Плюс ты не уточнил, что это ошибка – он может подумать, что ты <user_name>, "
             "и продолжит писать."),
        ],
    },
    "branch2": {
        "stranger": "«Ну наконец-то! А то я уже начал волноваться. Так когда ты заедешь "
                    "за материалами? Нам нужно решить с доставкой к пятнице».",
        "choices": [
            ("«Извините, я пошутил. Я вообще-то не <user_name>».", "end_joke",
             "Ты признаёшь обман – это храбро. Мужчина поймёт, закроет диалог."),
            ("«Давайте обсудим детали, сколько стоят материалы?»", "branch2_pressure",
             "Ты продолжаешь врать и уже пытаешься получить информацию (цену). Это игра с огнём. "
             "Если бы это был вербовщик, он бы уцепился за твой интерес."),
            ("«А кто вы вообще? Я не понимаю, о чём вы».", "branch2_pressure",
             "Ты притворяешься, что не понял, но это тоже ложь. Лучше сразу сказать правду."),
        ],
    },
    "branch2_pressure": {
        "stranger": "«Ну ты странный. <user_name> бы знал, о чём речь. Ты точно он? Как тебя "
                    "зовут? Ты работаешь в «СтройГаранте»?»",
        "bezopasik": "Стоп! Он начал задавать вопросы о твоей работе, имени. Даже если он "
                     "просто запутался, ты уже дал ему повод спрашивать. Лучший выход – резко "
                     "прекратить диалог: напиши «Извините, я ошибся, я не <user_name>» и больше не отвечай.",
        "choices": [
            ("Признаться: «Извините, я ошибся, я не <user_name>».", "end_confess",
             "Признание — смелый и безопасный выход, хоть и с опозданием. Лучше поздно, чем "
             "продолжать врать."),
            ("Продолжать врать дальше.", "end_lie",
             "Каждая новая ложь – это ещё одна ниточка, за которую могут потянуть. Не продолжай игру."),
        ],
    },
    "branch3": {
        "stranger": "«Извините, я просто набрал номер из записной книжки, думал, это "
                    "<user_name>. А вы его знаете?»",
        "choices": [
            ("«Нет, такого имени не знаю. Вы ошиблись».", "end_silver",
             "Ты ответил на его вопрос, не говоря о себе. Диалог закрывается."),
            ("«А кто такой <user_name>? Расскажите подробнее».", "end_story",
             "Ты проявляешь интерес к чужому человеку. Это не опасно сейчас, но формирует привычку "
             "«вести беседу» с незнакомцами. Вдруг это проверка?"),
        ],
    },
}

LEVEL1_ENDINGS = {
    "end_gold": {
        "title": "Идеальный отказ",
        "stranger": "«Ой, простите, перепутал номер. Извините за беспокойство!»",
        "bezopasik": "Идеально! Ты завершил разговор за 1 ход.<br>"
                     "— Ты не сказал своего имени.<br>"
                     "— Не подтвердил чужое имя.<br>"
                     "— Не вступил в переписку.<br>"
                     "Запомни: вежливый отказ + остановка – лучший щит. Даже если бы это был "
                     "террорист, он бы потерял интерес. Уровень пройден с «Золотым щитом».",
        "shield": "🥇 Золотой щит — Безопасная концовка",
        "color": "#2e7d32",
        "score": True,
    },
    "end_joke": {
        "title": "Отшутился, но заигрался",
        "stranger": "«Ах ты шутник! Ну ладно, бывает. Не переживай, найду нужного человека "
                    "по-другому. Пока!»",
        "bezopasik": "Фух, ты выкрутился. Но видишь, сколько лишних действий? Врать – значит "
                     "тратить время и нервы. В реальной опасной ситуации террорист не простит "
                     "такой «шутки». Запомни: честность с незнакомцами (без личных данных) – "
                     "самый короткий путь к безопасности.",
        "shield": "🟡 Нейтральная концовка — пройдено с предупреждением",
        "color": "#f9a825",
        "score": False,
    },
    "end_confess": {
        "title": "Признался слишком поздно",
        "stranger": "«Ладно, всё равно свяжусь с ним по-другому. Извините за путаницу!»",
        "bezopasik": "Ты вовремя остановился и признался — это правильно. Но ты уже успел "
                     "втянуться в разговор и почти назвал себя чужим именем. В следующий раз "
                     "останавливайся сразу, на первом шаге. Диалог закрыт нейтрально, но с "
                     "потерей очков за доверие.",
        "shield": "🟡 Нейтральная концовка — потеря очков доверия",
        "color": "#f9a825",
        "score": False,
    },
    "end_lie": {
        "title": "Продолжил врать",
        "stranger": "«Не смешно, перестаньте.»",
        "bezopasik": "Ты зашёл в тупик. Никогда не поддерживай чужую ошибку, это может быть "
                     "ловушкой. Итог: проход с «бронзовым щитом» – запомни урок.",
        "shield": "🥉 Бронзовый щит — прошёл, но с ошибками",
        "color": "#c62828",
        "score": False,
    },
    "end_silver": {
        "title": "Чёткий вопрос и точка",
        "stranger": "«А, понятно. Извините за беспокойство, видимо, ошибся!»",
        "bezopasik": "Ты задал вопрос, получил ответ и поставил точку. Отлично!",
        "shield": "🥈 Серебряный щит — хорошая концовка",
        "color": "#2e7d32",
        "score": True,
    },
    "end_story": {
        "title": "Заслушался чужой историей",
        "stranger": "«<user_name> — мой знакомый, работает в «СтройГаранте», обещал материалы "
                    "для дачи. Видимо, не туда попал».",
        "bezopasik": "Ты стал слушать историю чужого человека. Это отнимает время и может "
                     "усыпить бдительность. В реальной опасной ситуации террористы часто "
                     "начинают с безобидных историй. Лучше ограничиться коротким «нет».",
        "shield": "🟡 Нейтральная концовка — с замечанием",
        "color": "#f9a825",
        "score": False,
    },
    "end_rude": {
        "title": "Грубость вместо вежливого отказа",
        "stranger": "«Ну и грубо… Извините, что побеспокоил».",
        "bezopasik": "Ты обидел человека, который просто ошибся. Да, ты не дал ему "
                     "информации, но грубость – не защита, это оружие, которое ранит и тебя. "
                     "Террористы тоже могут притворяться обиженными, чтобы вызвать у тебя "
                     "чувство вины и начать манипуляцию. Учись говорить «нет» твёрдо, но "
                     "вежливо. Запомни фразу: «Извините, вы ошиблись» – она волшебная.",
        "shield": "🟢 Пройдено — но с потерей очков дружелюбия",
        "color": "#f9a825",
        "score": False,
    },
}

# --------------------------------------------------------------------------
# ЮРИДИЧЕСКАЯ СПРАВКА (используется на финальном экране)
# --------------------------------------------------------------------------
LEGAL_REFERENCES = [
    {
        "article": "Ст. 280 УК РФ",
        "title": "Публичные призывы к осуществлению экстремистской деятельности",
    },
    {
        "article": "Ст. 282 УК РФ",
        "title": "Возбуждение ненависти либо вражды, а также унижение человеческого достоинства",
    },
    {
        "article": "Ст. 282.1 УК РФ",
        "title": "Организация экстремистского сообщества",
    },
    {
        "article": "Ст. 282.2 УК РФ",
        "title": "Организация деятельности экстремистской организации",
    },
    {
        "article": "Ст. 205.1 УК РФ",
        "title": "Содействие террористической деятельности",
    },
    {
        "article": "Ст. 205.2 УК РФ",
        "title": "Публичные призывы к осуществлению террористической деятельности",
    },
]
LEGAL_SOURCE_URL = "https://www.consultant.ru/document/cons_doc_LAW_10699/"


# ==========================================================================
# ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ СЕССИИ
# ==========================================================================
def init_state():
    """Создаёт все нужные ключи в st.session_state при первом запуске."""
    defaults = {
        "phase": "intro",       # "intro" → "name_entry" (ввод имени) → "quest"
        "intro_screen": 1,      # 1, 2 или 3 — текущий экран пролога
        "intro_choice": None,   # "yes" / "no" — ответ на «Хочешь начать игру?»
        "user_name": "",        # имя игрока, введённое перед 1-м уровнем
        "level": 1,             # текущий уровень квеста: 1, 2, 3 или 4 (финал)
        "score": 0,             # количество верных действий (макс. 3 — по числу уровней)
        "errors": [],           # список ошибок вида {"level":.., "title":.., "explanation":..}
        "l1_path": ["start"],   # история пройденных узлов диалога уровня 1 (для истории чата)
        "l1_choices": [],       # выбранные пользователем реплики между узлами l1_path
        "level1_had_error": False,      # был ли хоть раз пройден неидеальный узел/потребовался повтор
        "level1_ending_processed": None,  # id уже обработанной (засчитанной/залогированной) концовки
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def restart_quest():
    """Полный сброс прогресса — используется кнопкой «Начать заново»."""
    keys_to_clear = [
        "phase", "intro_screen", "intro_choice", "user_name",
        "level", "score", "errors",
        "l1_path", "l1_choices", "level1_had_error", "level1_ending_processed",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    init_state()


def restart_level1_dialogue():
    """Сбрасывает только диалог уровня 1, чтобы попробовать пройти его заново."""
    st.session_state.l1_path = ["start"]
    st.session_state.l1_choices = []
    st.session_state.level1_ending_processed = None


def add_error(level: int, title: str, explanation: str):
    """Добавляет запись об ошибке в общий список для финального разбора."""
    st.session_state.errors.append({
        "level": level,
        "title": title,
        "explanation": explanation,
    })


def personalize(text: str) -> str:
    """Подставляет имя игрока вместо плейсхолдера <user_name> в тексте сценария."""
    name = st.session_state.get("user_name", "").strip() or DEFAULT_NAME
    return text.replace(NAME_PLACEHOLDER, html.escape(name))


def bezopasik_bubble(text: str):
    """Отрисовывает реплику Безопасика: портрет маскота слева + текст справа."""
    col_avatar, col_text = st.columns([1, 5], vertical_alignment="center")
    with col_avatar:
        if MASCOT_PATH.exists():
            st.image(str(MASCOT_PATH), width=MASCOT_WIDTH)
        else:
            # Файл mascot.png не найден рядом с app.py — показываем эмодзи-заглушку.
            st.markdown(
                "<div style='font-size:64px;line-height:1;text-align:center;'>🐶</div>",
                unsafe_allow_html=True,
            )
    with col_text:
        st.markdown(
            f'<div style="background-color:rgba(120,170,255,0.12);'
            f'border:1px solid rgba(120,170,255,0.35);border-radius:16px;'
            f'padding:18px 20px;font-size:16px;line-height:1.55;">{text}</div>',
            unsafe_allow_html=True,
        )


def stranger_bubble(text: str):
    """Отрисовывает входящее сообщение от незнакомца в стиле мессенджера."""
    col_avatar, col_text = st.columns([1, 5], vertical_alignment="center")
    with col_avatar:
        st.markdown(
            "<div style='font-size:64px;line-height:1;text-align:center;'>👤</div>",
            unsafe_allow_html=True,
        )
    with col_text:
        st.markdown(
            f'<div style="background-color:rgba(150,150,150,0.15);'
            f'border:1px solid rgba(150,150,150,0.4);border-radius:16px;'
            f'padding:18px 20px;font-size:16px;line-height:1.55;">'
            f'<b>Незнакомец</b><br>{text}</div>',
            unsafe_allow_html=True,
        )


def user_message_bubble(text: str):
    """Отрисовывает отправленный игроком ответ в стиле мессенджера (справа)."""
    col_text, col_avatar = st.columns([5, 1], vertical_alignment="center")
    with col_text:
        st.markdown(
            f'<div style="background-color:rgba(46,125,50,0.15);'
            f'border:1px solid rgba(46,125,50,0.4);border-radius:16px;'
            f'padding:18px 20px;font-size:16px;line-height:1.55;text-align:right;">'
            f'<b>Ты</b><br>{text}</div>',
            unsafe_allow_html=True,
        )
    with col_avatar:
        st.markdown(
            "<div style='font-size:64px;line-height:1;text-align:center;'>🙂</div>",
            unsafe_allow_html=True,
        )


# ==========================================================================
# БОКОВАЯ ПАНЕЛЬ
# ==========================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"## {DOG} Прогресс квеста")
        st.divider()

        if st.session_state.phase == "intro":
            st.markdown("▶️ **Пролог: знакомство с Безопасиком**")
        elif st.session_state.phase == "name_entry":
            st.markdown("▶️ **Знакомство: как тебя зовут?**")
        else:
            level_names = {
                1: LEVEL1_TITLE,
                2: "2️⃣ Уровень 2",
                3: "3️⃣ Уровень 3",
                4: "🏁 Финальный разбор",
            }
            current_level = st.session_state.level
            progress_value = min(current_level - 1, 3) / 3
            st.progress(progress_value, text=level_names.get(current_level, ""))

            for lvl, name in level_names.items():
                if lvl == 4:
                    continue
                if lvl < current_level:
                    st.markdown(f"✅ {name}")
                elif lvl == current_level:
                    st.markdown(f"▶️ **{name}**")
                else:
                    st.markdown(f"⬜ {name}")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⭐ Счёт", f"{st.session_state.score}/3")
        with col2:
            st.metric("⚠️ Ошибок", len(st.session_state.errors))

        st.divider()
        if st.button("🔄 Начать заново", use_container_width=True):
            restart_quest()
            st.rerun()

        st.divider()
        st.caption(
            "Учебный тренажёр по профилактике вовлечения в экстремистскую "
            "и деструктивную деятельность. Все персонажи и ситуации вымышлены."
        )


# ==========================================================================
# ПРОЛОГ: ЗНАКОМСТВО С БЕЗОПАСИКОМ
# ==========================================================================
def render_intro():
    screen = st.session_state.intro_screen

    if screen == 1:
        bezopasik_bubble(INTRO_SCREEN_1.replace("\n\n", "<br><br>"))
        if st.button("Дальше ➡️", type="primary", use_container_width=True):
            st.session_state.intro_screen = 2
            st.rerun()

    elif screen == 2:
        bezopasik_bubble(INTRO_SCREEN_2.replace("\n\n", "<br><br>"))
        if st.button("Вперёд! 🚀", type="primary", use_container_width=True):
            st.session_state.intro_screen = 3
            st.rerun()

    elif screen == 3:
        if st.session_state.intro_choice is None:
            bezopasik_bubble(f"<b>{INTRO_SCREEN_3_QUESTION}</b>")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("ДА", type="primary", use_container_width=True):
                    st.session_state.intro_choice = "yes"
                    st.rerun()
            with col2:
                if st.button("НЕТ", use_container_width=True):
                    st.session_state.intro_choice = "no"
                    st.rerun()
        else:
            reply = INTRO_REPLY_YES if st.session_state.intro_choice == "yes" else INTRO_REPLY_NO
            bezopasik_bubble(reply)
            if st.button("Начать квест ➡️", type="primary", use_container_width=True):
                st.session_state.phase = "name_entry"
                st.rerun()


# ==========================================================================
# ЗНАКОМСТВО: ВВОД ИМЕНИ ИГРОКА (между прологом и уровнем 1)
# ==========================================================================
def render_name_entry():
    bezopasik_bubble(
        "Прежде чем мы отправимся в путь, я хочу узнать, как к тебе обращаться! "
        "Как тебя зовут?"
    )
    name = st.text_input("Введи своё имя", key="name_input", max_chars=30)
    if st.button("Продолжить ➡️", type="primary", use_container_width=True):
        cleaned = name.strip()
        if not cleaned:
            st.warning("Пожалуйста, введи своё имя, чтобы продолжить.")
        else:
            st.session_state.user_name = cleaned
            st.session_state.phase = "quest"
            st.rerun()


# ==========================================================================
# УРОВЕНЬ 1: «ОШИБСЯ НОМЕРОМ» (вариативный диалог)
# ==========================================================================
def render_level1():
    st.markdown(f"# {LEVEL1_TITLE}")
    bezopasik_bubble(LEVEL1_INTRO)
    st.divider()

    path = st.session_state.l1_path
    choices_made = st.session_state.l1_choices

    # История чата: все уже пройденные сообщения незнакомца и ответы игрока
    # остаются на экране и никуда не пропадают при переходе к новой развилке.
    for i, step in enumerate(path[:-1]):
        node = LEVEL1_NODES.get(step)
        if node and node.get("stranger"):
            stranger_bubble(personalize(node["stranger"]))
        user_message_bubble(personalize(choices_made[i]))

    current_step = path[-1]
    if current_step in LEVEL1_ENDINGS:
        render_level1_ending(current_step)
    else:
        render_level1_node(current_step)


def render_level1_node(step: str):
    """Отрисовывает текущий узел-развилку: сообщение незнакомца, варианты ответа, затем Безопасик."""
    node = LEVEL1_NODES[step]

    if node.get("stranger"):
        stranger_bubble(personalize(node["stranger"]))

    for i, (label, next_step, comment) in enumerate(node["choices"]):
        if st.button(
            personalize(label),
            key=f"l1_{step}_{i}",
            help=personalize(comment),
            use_container_width=True,
        ):
            st.session_state.l1_choices.append(label)
            st.session_state.l1_path.append(next_step)
            st.rerun()

    # Реплика Безопасика относится только к текущей развилке и меняется по мере
    # продвижения по сценарию — в постоянную историю чата она не попадает.
    if node.get("bezopasik"):
        bezopasik_bubble(personalize(node["bezopasik"]))
    if node.get("hint"):
        bezopasik_bubble(f"<i>🤫 «{personalize(node['hint'])}»</i>")


def render_level1_ending(step: str):
    """Отрисовывает концовку диалога, засчитывает очко/ошибку один раз за попытку."""
    ending = LEVEL1_ENDINGS[step]
    stranger_text = personalize(ending["stranger"])
    bezopasik_text = personalize(ending["bezopasik"])

    stranger_bubble(stranger_text)
    bezopasik_bubble(bezopasik_text)

    st.markdown(
        f'<div style="padding:14px 18px;border-radius:12px;'
        f'background-color:{ending["color"]};color:white;font-size:17px;'
        f'text-align:center;margin-bottom:8px;"><b>{ending["shield"]}</b></div>',
        unsafe_allow_html=True,
    )

    # Засчитываем очко или ошибку только один раз за каждую свежедостигнутую концовку.
    if st.session_state.level1_ending_processed != step:
        st.session_state.level1_ending_processed = step
        if ending["score"]:
            if not st.session_state.level1_had_error:
                st.session_state.score += 1
        else:
            st.session_state.level1_had_error = True
            add_error(level=1, title=ending["title"], explanation=bezopasik_text)

    st.divider()
    bezopasik_bubble(LEVEL1_LECTURE.replace("\n\n", "<br><br>").replace("\n", "<br>"))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Пройти уровень заново", use_container_width=True):
            restart_level1_dialogue()
            st.rerun()
    with col2:
        if st.button("Далее ➡️", type="primary", use_container_width=True):
            st.session_state.level = 2
            st.rerun()


# ==========================================================================
# ЗАГЛУШКИ ДЛЯ БУДУЩИХ УРОВНЕЙ (сценарий пока не предоставлен)
# ==========================================================================
def render_level_placeholder(level_number: int):
    st.markdown(f"# {level_number}️⃣ Уровень {level_number}")
    bezopasik_bubble(
        f"Этот уровень пока в разработке — сценарий для него ещё не готов. "
        f"Как только он появится, здесь будет новое приключение! {DOG}"
    )
    st.info("Временная кнопка ниже нужна только для тестирования перехода к финалу.")
    if st.button("Перейти дальше (временно) ➡️", type="primary", use_container_width=True):
        st.session_state.level += 1
        st.rerun()


# ==========================================================================
# ФИНАЛЬНЫЙ ЭКРАН
# ==========================================================================
def render_final():
    st.markdown("# 🏁 Финальный разбор")
    st.divider()

    score = st.session_state.score
    total_errors = len(st.session_state.errors)

    # --- Цветовой индикатор итогового результата ---
    if score == 3:
        color = "green"
        verdict = "Отличный результат! Ты уверенно распознаёшь признаки вовлечения и знаешь, как действовать."
        icon = "🟢"
    elif score == 2:
        color = "orange"
        verdict = "Хороший результат, но есть над чем поработать — перечитай пояснения к ошибкам ниже."
        icon = "🟡"
    else:
        color = "red"
        verdict = "Стоит внимательнее изучить признаки опасного поведения незнакомцев и алгоритм безопасных действий."
        icon = "🔴"

    st.markdown(
        f"""
        <div style="padding:20px;border-radius:12px;background-color:{color};
                    color:white;text-align:center;font-size:20px;">
            {icon} <b>Итоговый счёт: {score} / 3</b><br>
            <span style="font-size:16px;">{verdict}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # --- Список ошибок ---
    st.markdown("## ⚠️ Разбор ошибок")
    if total_errors == 0:
        st.success("Ошибок не было — ты прошёл квест без единой ошибки! 👏")
    else:
        for i, err in enumerate(st.session_state.errors, start=1):
            with st.expander(f"Ошибка №{i} — Уровень {err['level']}: {err['title']}"):
                st.markdown(err["explanation"])

    st.divider()

    # --- Юридическая справка ---
    st.markdown("## ⚖️ Юридическая справка")
    st.markdown(
        "Вовлечение в экстремистскую и террористическую деятельность, а также "
        "публичные призывы к ней, влекут уголовную ответственность по "
        "законодательству Российской Федерации:"
    )
    for ref in LEGAL_REFERENCES:
        st.markdown(f"- **{ref['article']}** — {ref['title']}")
    st.markdown(f"\n🔗 Полный текст Уголовного кодекса РФ: [{LEGAL_SOURCE_URL}]({LEGAL_SOURCE_URL})")

    st.info(
        "💡 **Если ты столкнулся с подозрительной активностью в интернете** — "
        "сохрани переписку и расскажи об этом взрослому, которому доверяешь, "
        "или обратись в полицию (тел. 102). Не вступай в диалог и не передавай "
        "никаких личных данных."
    )

    st.divider()
    if st.button("🔄 Начать заново", type="primary", use_container_width=True):
        restart_quest()
        st.rerun()


# ==========================================================================
# ТОЧКА ВХОДА
# ==========================================================================
def main():
    init_state()

    col_logo, col_title = st.columns([1, 6], vertical_alignment="center")
    with col_logo:
        if MASCOT_PATH.exists():
            st.image(str(MASCOT_PATH), width=70)
        else:
            # Файл mascot.png не найден рядом с app.py — показываем эмодзи-заглушку.
            st.markdown(
                "<div style='font-size:48px;line-height:1;'>🐶🤖</div>",
                unsafe_allow_html=True,
            )
    with col_title:
        st.title("Квест: Безопасик")
    st.divider()

    render_sidebar()

    if st.session_state.phase == "intro":
        render_intro()
        return

    if st.session_state.phase == "name_entry":
        render_name_entry()
        return

    level = st.session_state.level
    if level == 1:
        render_level1()
    elif level == 2:
        render_level_placeholder(2)
    elif level == 3:
        render_level_placeholder(3)
    else:
        render_final()


if __name__ == "__main__":
    main()
