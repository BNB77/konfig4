# ИКБО-11-24 Лебедев Антон Владимирович

## <img width="762" height="1184" alt="image" src="https://github.com/user-attachments/assets/6aa35342-307c-4a02-b3f0-3e7b9672639e" />


Это учебный проект, реализующий собственный конфигурационный язык с поддержкой основных конструкций: переменных, массивов, словарей и вычислений констант. Проект демонстрирует принципы работы компиляторов и интерпретаторов.

## ✨ Возможности

- **Лексический анализ** - разбор входного текста на токены
- **Синтаксический анализ** - построение AST (абстрактного синтаксического дерева)
- **Интерпретация** - вычисление значений и обработка конструкций
- **Конвертация в TOML** - экспорт конфигурации в формат TOML
- **Вычисление константных выражений** - поддержка операций min() и других
- **Обработка комментариев** - однострочные и многострочные комментарии


## 📦 Зависимости

Проект использует стандартную библиотеку Python. Все необходимые зависимости указаны в `requirements.txt`.

## 💻 Использование

### Командная строка

```bash
# Преобразование конфигурационного файла в TOML
python config_tool.py input.conf output.toml
```

### Программное использование

```python
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from toml_converter import TOMLConverter

# Чтение конфигурационного файла
with open('example.conf', 'r') as f:
    config_text = f.read()

# Лексический анализ
lexer = Lexer(config_text)
tokens = lexer.tokenize()

# Синтаксический анализ
parser = Parser(tokens)
ast = parser.parse()

# Интерпретация
interpreter = Interpreter()
result = interpreter.evaluate(ast)

# Конвертация в TOML
converter = TOMLConverter()
toml_output = converter.convert(result)
print(toml_output)
```

## 📝 Синтаксис языка

### Объявление переменных

```
var name = "value";
var number = 42;
```

### Массивы

```
var list = #(1, 2, 3, 4, 5);
```

### Словари

```
var config = {
    host : "localhost",
    port : 8080,
    debug : true
};
```

### Вычисление констант

```
var min_value = min(10, 20, 30);
```

## 🧪 Тестирование

Проект включает полный набор unit-тестов и интеграционных тестов:

```bash
# Запуск всех тестов
python -m pytest

# Запуск конкретного модуля тестов
python -m pytest test_lexer.py
python -m pytest test_parser.py
python -m pytest test_interpreter.py
python -m pytest test_toml_converter.py
python -m pytest test_integration.py
```

## 📚 Примеры

В репозитории доступны примеры конфигурационных файлов:

- `example1.conf` - базовый пример
- `example2.conf` - работа с массивами и словарями
- `example3.conf` - сложные вычисления

### Демонстрационные скрипты

```bash
# Демонстрация работы лексера
python demo_lexer.py

# Демонстрация работы парсера
python demo_parser.py

# Демонстрация работы интерпретатора
python demo_interpreter.py
```

## 🔧 Компоненты системы

### Lexer (Лексический анализатор)
Преобразует исходный текст в последовательность токенов (идентификаторы, операторы, литералы).

### Parser (Синтаксический анализатор)
Строит абстрактное синтаксическое дерево (AST) из последовательности токенов.

### Interpreter (Интерпретатор)
Обходит AST и вычисляет значения выражений, обрабатывает объявления переменных.

### TOML Converter
Конвертирует результат интерпретации в формат TOML для совместимости с другими системами.

## 📖 Примеры использования

### Пример 1: Простая конфигурация

```conf
var app_name = "MyApp";
var version = "1.0.0";
var port = 8080;
```

Результат в TOML:
```toml
app_name = "MyApp"
version = "1.0.0"
port = 8080
```

### Пример 2: Конфигурация с вложенными структурами

```conf
var database = {
    host : "localhost",
    port : 5432,
    credentials : {
        username : "admin",
        password : "secret"
    }
};
```

### Пример 3: Использование вычислений

```conf
var limits = {
    min : min(10, 20, 5),
    max : 100
};
```
## 📞 Контакты

GitHub: [BNB77](https://github.com/BNB77)

---

**Статус проекта:** Активная разработка  
**Версия Python:** 3.7+
