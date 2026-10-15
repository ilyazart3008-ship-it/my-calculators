import pandas as pd
import streamlit as st

st.set_page_config(page_title="Мои калькуляторы", page_icon="🧮", layout="centered")

st.title("🧮 Мои калькуляторы")
st.caption("Конвертер единиц, проценты")


def fmt(x: float, digits: int = 2) -> str:
    """Красивое число: 1 234 567,89"""
    return f"{x:,.{digits}f}".replace(",", " ").replace(".", ",")
def fmt_short(x: float, digits: int = 6) -> str:
    """Число без лишних нулей: 1 000 вместо 1 000,000000"""
    s = f"{x:,.{digits}f}".rstrip("0").rstrip(".")
    return s.replace(",", " ").replace(".", ",")

tab_units, tab_percent = st.tabs(
    ["📏 Единицы", "％ Проценты"]
)

# ---------------------------------------------------------------- Единицы
with tab_units:
    st.subheader("Конвертер единиц")

    # Коэффициенты: сколько базовых единиц в одной данной единице
    UNITS = {
        "Длина": {"мм": 0.001, "см": 0.01, "м": 1, "км": 1000,
                  "дюйм": 0.0254, "фут": 0.3048, "ярд": 0.9144, "миля": 1609.344},
        "Масса": {"мг": 1e-6, "г": 0.001, "кг": 1, "т": 1000,
                  "унция": 0.028349523125, "фунт": 0.45359237},
        "Объём": {"мл": 0.001, "л": 1, "м³": 1000,
                  "галлон (США)": 3.785411784, "пинта (США)": 0.473176473},
        "Площадь": {"см²": 0.0001, "м²": 1, "га": 10000, "км²": 1e6,
                    "фут²": 0.09290304, "акр": 4046.8564224},
        "Скорость": {"м/с": 1, "км/ч": 1 / 3.6, "миля/ч": 0.44704, "узел": 0.514444},
        "Время": {"с": 1, "мин": 60, "ч": 3600, "сутки": 86400, "неделя": 604800},
        "Температура": {"°C": None, "°F": None, "K": None},
    }

    def convert_temperature(value, src, dst):
        # Сначала переводим в градусы Цельсия
        if src == "°F":
            c = (value - 32) * 5 / 9
        elif src == "K":
            c = value - 273.15
        else:
            c = value
        if dst == "°F":
            return c * 9 / 5 + 32
        if dst == "K":
            return c + 273.15
        return c

    category = st.selectbox("Что переводим?", list(UNITS.keys()))
    units = list(UNITS[category].keys())

    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    value = col1.number_input("Значение", value=1.0, format="%g", key="unit_value")
    src = col2.selectbox("Из", units, index=0, key="unit_src")
    dst = col3.selectbox("В", units, index=min(1, len(units) - 1), key="unit_dst")

    if category == "Температура":
        result = convert_temperature(value, src, dst)
    else:
        result = value * UNITS[category][src] / UNITS[category][dst]

    st.success(f"{fmt_short(value)} {src} = **{fmt_short(result)} {dst}**")

# ---------------------------------------------------------------- Проценты
with tab_percent:
    st.subheader("Калькулятор процентов")

    mode = st.radio(
        "Что нужно посчитать?",
        [
            "Сколько составляет X% от Y",
            "Сколько процентов X от Y",
            "Увеличить / уменьшить число на X%",
            "На сколько процентов изменилось число",
        ],
    )

    if mode == "Сколько составляет X% от Y":
        x = st.number_input("X (проценты)", value=15.0, key="p1x")
        y = st.number_input("Y (число)", value=200.0, key="p1y")
        st.success(f"{fmt(x)}% от {fmt(y)} = **{fmt(y * x / 100)}**")

    elif mode == "Сколько процентов X от Y":
        x = st.number_input("X", value=30.0, key="p2x")
        y = st.number_input("Y", value=200.0, key="p2y")
        if y == 0:
            st.error("Y не может быть равен нулю.")
        else:
            st.success(f"{fmt(x)} составляет **{fmt(x / y * 100)}%** от {fmt(y)}")

    elif mode == "Увеличить / уменьшить число на X%":
        n = st.number_input("Число", value=1000.0, key="p3n")
        x = st.number_input("Процент", value=10.0, key="p3x")
        st.success(
            f"Увеличить на {fmt(x)}%: **{fmt(n * (1 + x / 100))}**\n\n"
            f"Уменьшить на {fmt(x)}%: **{fmt(n * (1 - x / 100))}**"
        )

    else:
        old = st.number_input("Было", value=80.0, key="p4o")
        new = st.number_input("Стало", value=100.0, key="p4n")
        if old == 0:
            st.error("Начальное значение не может быть равно нулю.")
        else:
            change = (new - old) / abs(old) * 100
            word = "выросло" if change > 0 else "уменьшилось" if change < 0 else "не изменилось"
            st.success(f"Число {word} на **{fmt(abs(change))}%**")
