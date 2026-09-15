"""COMP9001 Week 6：函数创建与调用 / Defining and calling functions.

运行 / Run:
    python L0_9001_w6_test.py

直接运行会按顺序演示；import 本文件时不自动执行示例。
Running this file shows the examples; importing it does not run them.

需要 Python 3.10+。只用 Python 标准库，不需要 Pygame 或其他第三方包。
Requires Python 3.10+. Uses only the standard library; no third-party packages.

基本格式 / Basic form:
    def function_name(parameter):    # 定义 / definition
        return result               # 返回 / return
    value = function_name(argument)  # 调用 / call

parameter（形参）：定义函数时写的名称；argument（实参）：调用时传入的值。
例如 def square(number) 中 number 是形参；square(3) 中 3 是实参。
类型标注如 number: int、-> int 用于说明类型，不会自动检查实参类型。
Annotations document types; they do not automatically validate arguments.
"""

from collections.abc import Callable  # 标准库：可调用对象的类型标注 / callable type hint


# 01. 无参数，无显式返回值 / No parameters, no explicit return value

def say_hello() -> None:
    """打印问候；无参数，隐式返回 None。
    Print a greeting; take no parameters and implicitly return None.
    """
    print("你好，欢迎学习函数！ / Hello, welcome to functions!")
    # 没有 return 语句，函数结束时仍然返回 None。
    # Without a return statement, Python returns None automatically.


# 02. 有参数，无显式返回值 / Parameters, no explicit return value

def greet(name: str) -> None:
    """打印指定姓名的问候 / Print a greeting for the given name.

    name（姓名 / name）：要问候的人 / the person to greet.
    返回 / Returns：None.
    """
    print(f"你好，{name}！ / Hello, {name}!")


# 03. 无参数，有返回值 / No parameters, with a return value

def get_course_name() -> str:
    """返回课程名；无参数 / Return the course name; no parameters.

    返回 / Returns：课程名称字符串 / a course-name string.
    """
    return "COMP9001"


# 04. 有参数，有返回值 / Parameters and a return value

def add(a: int, b: int) -> int:
    """计算两个整数的和 / Add two integers.

    a（第一个数 / first number）、b（第二个数 / second number）。
    返回 / Returns：a + b.
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """计算乘积 / Multiply two integers.

    a、b（两个乘数 / two factors）。返回 / Returns：a * b.
    """
    return a * b


# 05. 默认参数与关键字传参 / Default parameters and keyword arguments

def introduce(name: str, course: str = "COMP9001") -> str:
    """生成介绍 / Build an introduction.

    name（姓名 / name）：学生姓名 / student's name.
    course（课程 / course）：默认 COMP9001 / defaults to COMP9001.
    返回 / Returns：介绍字符串 / an introduction string.
    """
    return f"{name} is studying {course}."


# 06. 多个返回值与下划线 / Multiple return values and underscore

def calculate(a: int, b: int) -> tuple[int, int]:
    """同时给出和与积 / Return both the sum and the product.

    a、b（输入整数 / input integers）。
    返回 / Returns：(和 / sum, 积 / product)，一个包含两项的 tuple。
    """
    return a + b, a * b
    # Python 实际返回一个 tuple；调用者可以将它解包成两个变量。
    # Python returns one tuple, which the caller can unpack into two variables.


def calculate_sum_only(a: int, b: int) -> int:
    """演示在函数内部给 _ 赋值 / Assign to _ inside a function.

    a、b（输入整数 / input integers）。
    返回 / Returns：和 / the sum only.
    """
    total, _ = calculate(a, b)
    # _ 接收乘积，名称表达“此处不打算使用它”，并不是特殊的丢弃指令。
    # _ receives the product; its name means "unused here" by convention only.
    return total


# 07–09. 函数赋给变量、作为参数、调用结果作为参数
# Function aliases, function arguments, and function results as arguments

def apply_operation(operation: Callable[[int, int], int], a: int, b: int) -> int:
    """接收一个函数，并使用两个数调用它 / Accept and call a function.

    operation（运算函数 / operation function）：接收两个 int、返回 int。
    a、b（传给运算函数的数 / numbers passed to the operation）。
    返回 / Returns：operation(a, b) 的计算结果 / the operation's result.
    """
    return operation(a, b)


def report_score(score: int) -> None:
    """显示得分 / Display a score.

    score（得分 / score）：已经计算好的整数 / an already computed integer.
    返回 / Returns：None.
    """
    print(f"得分 / Score: {score}")


# 10. 局部变量 / Local variables

def increase_score(score: int, amount: int = 1) -> int:
    """返回加分后的新值 / Return a new, increased score.

    score（当前分数 / current score）、amount（增加量 / increment，默认 1）。
    返回 / Returns：新分数 / the new score.
    """
    score = score + amount
    # 这里重新绑定的是函数里的局部名称，不会替换调用者的整数变量。
    # This rebinds the local name; it does not replace the caller's integer variable.
    return score


# 11. 提前返回 / Early return

def score_message(score: int) -> str:
    """按分数返回信息 / Return a message based on the score.

    score（待检查分数 / score to check）。
    返回 / Returns：对应的提示文本 / the corresponding message.
    """
    if score < 0:
        return "分数不能为负 / Score cannot be negative"
    if score == 0:
        return "继续尝试 / Keep trying"
    return "做得不错 / Well done"
    # return 结束当前函数，这一行之后不会继续执行本次函数体。
    # return ends the current function call.


# 12. 数量不固定的位置参数 / Variable-length positional arguments

def total_scores(*scores: int) -> int:
    """把任意数量的分数相加 / Add any number of scores.

    scores（分数集合 / scores）：*scores 将位置实参收集成 tuple。
    *scores collects positional arguments into a tuple.
    返回 / Returns：总分 / total score；没有实参时为 0。
    """
    return sum(scores)


# 13. 数量不固定的关键字参数 / Variable-length keyword arguments

def show_profile(**details: object) -> None:
    """显示任意命名信息 / Display any named details.

    details（信息字典 / details dictionary）：**details 收集关键字实参。
    **details collects keyword arguments into a dictionary.
    返回 / Returns：None.
    """
    for key, value in details.items():
        print(f"  {key}: {value}")
    # scores/details 名称可自行选择；* 和 ** 才决定收集方式。
    # The names are arbitrary; * and ** determine how arguments are collected.


# 14. lambda 与 key 参数 / lambda and the key argument

def get_score(record: tuple[str, int]) -> int:
    """提取一条成绩记录的分数 / Extract the score from a record.

    record（记录 / record）：(姓名 / name, 分数 / score)。
    返回 / Returns：记录中的分数 / the score in the record.
    """
    return record[1]


# 15. 返回另一个函数 / Returning another function (closure)

def make_multiplier(factor: int) -> Callable[[int], int]:
    """生成一个乘法函数 / Create a multiplier function.

    factor（倍数 / multiplication factor）：内层函数会使用此值。
    返回 / Returns：一个接收整数、返回整数的函数 / an int-to-int function.
    """
    def times(number: int) -> int:
        """number（输入数 / input number）；返回它与 factor 的乘积。
        Return number multiplied by the captured factor.
        """
        return number * factor

    return times  # 返回函数对象，暂不调用 / return the function without calling it


# 16. 列表参数与默认值 None / List arguments and the default value None

def add_item(item: str, items: list[str] | None = None) -> list[str]:
    """向列表追加一项 / Append one item to a list.

    item（新内容 / new item）、items（目标列表 / target list，可省略）。
    返回 / Returns：追加后的列表 / the list after appending.
    若传入已有列表，此函数会修改它 / An existing list is modified in place.
    """
    if items is None:
        items = []  # 省略参数时，每次创建新列表 / create a fresh list when omitted
    items.append(item)
    return items
    # 不写 items=[]：可变默认值只在定义时创建一次，可能被多次调用共享。
    # Avoid items=[]: a mutable default is created once and reused across calls.


# 17. 只能按关键字传入的参数 / Keyword-only parameters

def format_score(score: int, *, prefix: str = "Score") -> str:
    """格式化成绩 / Format a score.

    score（分数 / score）；prefix（前缀 / prefix）必须写 prefix=...。
    返回 / Returns：格式化文本 / formatted text.
    """
    return f"{prefix}: {score}"


def run_examples() -> None:
    """按顺序运行所有演示；无参数 / Run all examples in order; no parameters.

    返回 / Returns：None；用 print 显示结果 / display results with print.
    """
    print("\n01 无参数，无显式返回值 / No parameters, no explicit return")
    returned = say_hello()
    print("函数返回 / Returned:", returned)  # None，不是打印出来的问候字符串

    print("\n02 有参数，无显式返回值 / Parameters, no explicit return")
    greet("Alex")

    print("\n03 无参数，有返回值 / No parameters, with return")
    course = get_course_name()
    print(course)  # COMP9001

    print("\n04 有参数，有返回值 / Parameters and return")
    answer = add(3, 5)
    print(answer)       # 8
    print(answer * 2)   # 16，返回值还能继续参与计算 / reuse the returned value

    print("\n05 默认、位置、关键字实参 / Default, positional, keyword arguments")
    print(introduce("Alex"))                    # Alex is studying COMP9001.
    print(introduce("Alex", "COMP9123"))        # 两个位置实参 / positional arguments
    print(introduce(course="COMP9120", name="Alex"))  # 关键字可以调换顺序

    print("\n06 多返回值和 _ 赋值 / Multiple results and assigning to _")
    total, product = calculate(3, 4)
    print(total, product)                 # 7 12
    print(calculate_sum_only(3, 4))       # 7，函数内部使用 total, _ 解包
    _, product = calculate(3, 4)
    print(product)                       # 12
    print("_ 仍保存了值 / _ still holds:", _)  # 7，证明 _ 是普通变量
    _ = say_hello()                       # 先打印问候，再把返回的 None 赋给 _
    print("_ 现在是 / _ is now:", _)     # None
    # _、_name、__name__ 不是同一种概念；这里练习的 _ 只是一个普通名称。

    print("\n07 函数赋给变量 / Assign a function to a variable")
    operation = add                      # 不加括号：保存函数对象 / function object
    print(operation(2, 3))               # 5，通过新名称调用同一个函数
    value = add(2, 3)                    # 加括号：立即调用，保存结果 / result
    print(value)                         # 5，value 是整数，不可以写 value()
    print(operation is add)              # True

    print("\n08 函数作为参数 / Pass a function as an argument")
    print(apply_operation(add, 6, 2))       # 8：operation 参数接收 add 函数
    print(apply_operation(multiply, 6, 2))  # 12：同一调用框架，换一个运算函数
    # apply_operation(add(6, 2), 6, 2) 是错误示范，不执行：
    # 它传入的是整数 8，而 operation 必须可以调用。
    # Do not pass add(6, 2) here: that passes 8, not a callable.

    print("\n09 调用结果作为另一个实参 / Pass a function's result as an argument")
    report_score(add(6, 2))  # 先得到 8，再调用 report_score(8)
    # 与上一例不同：这里需要整数，所以应该调用 add(...)。
    # Unlike the previous example, this function expects an integer result.

    print("\n10 局部变量与接收返回值 / Local names and receiving a return value")
    score = 10
    updated = increase_score(score, 2)
    print(score, updated)                # 10 12，外面的 score 尚未改变
    score = increase_score(score, 2)
    print(score)                         # 12：主动把返回值赋给外面的变量

    print("\n11 提前返回 / Early return")
    for score in (-1, 0, 8):
        print(score_message(score))

    print("\n12 *args 与列表解包 / *args and unpacking a list")
    print(total_scores())                # 0
    print(total_scores(2, 3, 4))          # 9
    values = [2, 3, 4]
    print(total_scores(*values))         # 9：展开为 total_scores(2, 3, 4)
    # 定义里的 * 是收集，调用里的 * 是展开 / collect in definitions, unpack in calls

    print("\n13 **kwargs 与字典解包 / **kwargs and unpacking a dictionary")
    show_profile(name="Alex", course="COMP9001")
    profile = {"name": "Sam", "week": 6}
    show_profile(**profile)              # 等价于 show_profile(name="Sam", week=6)

    print("\n14 lambda 与 sorted(key=函数) / lambda and sorted(key=function)")
    records = [("Alex", 7), ("Sam", 3), ("Jo", 9)]
    print(sorted(records, key=get_score))          # [('Sam', 3), ('Alex', 7), ('Jo', 9)]
    print(sorted(records, key=lambda record: record[1]))  # 相同结果 / same result
    # sorted 将每条记录传给 key 函数，以它的返回值排序。
    # sorted calls the key function for each record and sorts by its result.
    # lambda 是单个表达式的小函数；复杂逻辑优先使用 def。

    print("\n15 返回函数 / Return a function")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(double(5), triple(5))           # 10 15
    # 内层 times 使用外层的 factor，这是闭包 / times captures factor: a closure

    print("\n16 列表修改与安全默认值 / List mutation and safe defaults")
    first = add_item("apple")
    second = add_item("banana")
    print(first, second)                 # ['apple'] ['banana']，不是共享同一列表
    bag = ["book"]
    returned_bag = add_item("pen", bag)
    print(bag)                           # ['book', 'pen']，传入的列表被修改
    print(returned_bag is bag)           # True，返回的是同一个列表对象

    print("\n17 只能用关键字的参数 / Keyword-only parameter")
    print(format_score(8))               # Score: 8
    print(format_score(8, prefix="得分"))  # 得分: 8
    # format_score(8, "得分") 会报错；* 后的参数必须写名称。
    # format_score(8, "得分") would fail: parameters after * require their names.


# 练习建议 / Practice tasks:
# 1. 写一个无参数函数，返回你自己的课程名 / Return your course name with no parameters.
# 2. 写 subtract(a, b)，传给 apply_operation / Pass your subtract function to apply_operation.
# 3. 调用 calculate(5, 6)，用 _ 只保留乘积 / Use _ to keep only the product.
# 4. 用 sorted 的 key 函数按姓名排序 / Sort records by name using a key function.
# 5. 用 make_multiplier 创建 times_ten / Create a times-ten function.

if __name__ == "__main__":
    run_examples()
