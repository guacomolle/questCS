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

from pathlib import Path

import streamlit as st

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
# ДАННЫЕ ДЛЯ УРОВНЯ 1: «ОСТОРОЖНО, НЕЗНАКОМЕЦ!»
# --------------------------------------------------------------------------
LEVEL1_INTRO = """
Пи-пи-пи! 🚨

Подожди...

Мой датчик безопасности что-то обнаружил!

Посмотри внимательно на экран. Кажется, тебе пришло сообщение.

Прочитай его и попробуй определить: можно ли сразу доверять этому человеку?

Не спеши!

Иногда самое правильное решение — сначала остановиться и подумать.

<b>Задание:</b> выбери, какие сообщения могут быть подозрительными.
"""

# Каждое сообщение — от вымышленного отправителя в стиле мессенджера.
# "suspicious" = True у сообщений 2, 4 и 5 (единственный верный набор ответов).
LEVEL1_MESSAGES = [
    {
        "id": 1,
        "sender": "Аноним_92",
        "text": "Привет! Как дела? Чем занимаешься сегодня?",
        "suspicious": False,
        "explanation": "Обычный дружеский вопрос без каких-либо просьб и манипуляций — поводов для тревоги нет.",
    },
    {
        "id": 2,
        "sender": "БыстрыйЗаработок",
        "text": "Слушай, тут есть возможность быстро заработать 10 000 робаксов, безо всяких усилий. Интересно?",
        "suspicious": True,
        "explanation": "Обещание лёгких денег или подарков «без усилий» — классическая приманка, которую используют мошенники и вербовщики.",
    },
    {
        "id": 3,
        "sender": "КиноФанат",
        "text": "Какой у тебя любимый фильм?",
        "suspicious": False,
        "explanation": "Обычный вопрос об интересах — безобидная тема для разговора.",
    },
    {
        "id": 4,
        "sender": "Тайный_Клуб",
        "text": "Привет! Хочешь попасть в закрытый клуб? Там очень крутые ребята. "
                "Нужно просто выполнить одно задание. Никому не говори 🤐",
        "suspicious": True,
        "explanation": "Приглашение в «закрытый клуб» с условием хранить всё в тайне — тревожный сигнал: секретность часто используют, чтобы скрыть вовлечение в опасную деятельность от взрослых.",
    },
    {
        "id": 5,
        "sender": "НовыйЗнакомый",
        "text": "Ты один дома? А родители скоро придут?",
        "suspicious": True,
        "explanation": "Вопросы о том, один ли ты дома и когда вернутся родители, — попытка выведать информацию об отсутствии присмотра взрослых. Это опасный сигнал.",
    },
    {
        "id": 6,
        "sender": "Соня_2012",
        "text": "Классная у тебя аватарка! Где фоткался?",
        "suspicious": False,
        "explanation": "Дружеский комплимент и лёгкий вопрос — сам по себе не является признаком вовлечения или манипуляции.",
    },
]
LEVEL1_CORRECT_IDS = {m["id"] for m in LEVEL1_MESSAGES if m["suspicious"]}

LEVEL1_SUCCESS_TEXT = (
    "Отлично! Ты настоящий детектив! Ты правильно заметил, что незнакомцы, "
    "которые предлагают лёгкие деньги, просят хранить тайну или выведывают, "
    "один ли ты дома — это опасные сигналы!"
)
LEVEL1_FAIL_INTRO_TEXT = "Не всё так просто! Давай разберёмся..."

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
        "phase": "intro",       # "intro" (пролог с Безопасиком) или "quest"
        "intro_screen": 1,      # 1, 2 или 3 — текущий экран пролога
        "intro_choice": None,   # "yes" / "no" — ответ на «Хочешь начать игру?»
        "level": 1,             # текущий уровень квеста: 1, 2, 3 или 4 (финал)
        "score": 0,             # количество верных действий (макс. 3 — по числу уровней)
        "errors": [],           # список ошибок вида {"level":.., "title":.., "explanation":..}
        "level1_had_error": False,
        "level1_solved_clean": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def restart_quest():
    """Полный сброс прогресса — используется кнопкой «Начать заново»."""
    keys_to_clear = [
        "phase", "intro_screen", "intro_choice",
        "level", "score", "errors",
        "level1_had_error", "level1_solved_clean",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    # Также очищаем чекбоксы уровня 1, если они были созданы
    for m in LEVEL1_MESSAGES:
        cb_key = f"l1_cb_{m['id']}"
        if cb_key in st.session_state:
            del st.session_state[cb_key]
    init_state()


def add_error(level: int, title: str, explanation: str):
    """Добавляет запись об ошибке в общий список для финального разбора."""
    st.session_state.errors.append({
        "level": level,
        "title": title,
        "explanation": explanation,
    })


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


# ==========================================================================
# БОКОВАЯ ПАНЕЛЬ
# ==========================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"## {DOG} Прогресс квеста")
        st.divider()

        if st.session_state.phase == "intro":
            st.markdown("▶️ **Пролог: знакомство с Безопасиком**")
        else:
            level_names = {
                1: "1️⃣ Осторожно, незнакомец!",
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
                st.session_state.phase = "quest"
                st.rerun()


# ==========================================================================
# УРОВЕНЬ 1: «ОСТОРОЖНО, НЕЗНАКОМЕЦ!»
# ==========================================================================
def render_level1():
    st.markdown("# 1️⃣ Уровень: «Осторожно, незнакомец!»")
    bezopasik_bubble(LEVEL1_INTRO.replace("\n\n", "<br><br>"))
    st.divider()

    selected_ids = set()
    for msg in LEVEL1_MESSAGES:
        col_icon, col_msg = st.columns([1, 9])
        with col_icon:
            st.markdown("### 💬")
        with col_msg:
            st.markdown(f"**{msg['sender']}**")
            st.markdown(f"> {msg['text']}")
            checked = st.checkbox(
                "Отметить как подозрительное",
                key=f"l1_cb_{msg['id']}",
            )
            if checked:
                selected_ids.add(msg["id"])
        st.markdown("")

    st.divider()

    if st.button("✅ Проверить выбор", type="primary", use_container_width=True):
        if selected_ids == LEVEL1_CORRECT_IDS:
            st.session_state.level1_solved_clean = not st.session_state.level1_had_error
            if st.session_state.level1_solved_clean:
                st.session_state.score += 1
            bezopasik_bubble(LEVEL1_SUCCESS_TEXT)
            st.session_state.level = 2
            st.rerun()
        else:
            st.session_state.level1_had_error = True
            missed = LEVEL1_CORRECT_IDS - selected_ids
            extra = selected_ids - LEVEL1_CORRECT_IDS
            wrong_ids = missed | extra
            by_id = {m["id"]: m for m in LEVEL1_MESSAGES}

            explanation_lines = []
            for mid in sorted(wrong_ids):
                m = by_id[mid]
                verdict = "подозрительное, но не отмечено" if mid in missed else "безопасное, но отмечено как подозрительное"
                explanation_lines.append(
                    f"«{m['text']}» ({verdict}). {m['explanation']}"
                )
            add_error(
                level=1,
                title="Не все сообщения определены верно",
                explanation=" ".join(explanation_lines),
            )

            bezopasik_bubble(LEVEL1_FAIL_INTRO_TEXT)
            for mid in sorted(wrong_ids):
                m = by_id[mid]
                icon = "🔴" if mid in missed else "🟡"
                st.markdown(f"{icon} **{m['sender']}:** _{m['text']}_")
                st.caption(m["explanation"])
            st.info("Попробуй ещё раз — отметь сообщения заново и нажми «Проверить выбор».")


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
