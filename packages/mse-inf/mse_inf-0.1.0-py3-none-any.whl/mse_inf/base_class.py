from typing import Optional, Callable
import os
import subprocess
import sys
import traceback
from dataclasses import dataclass
from enum import Enum

RUN_TIMEOUT = 20

class MessageLevel(Enum):
    ALL = "Тест #{test_number} не пройден.\nВходные данные:\n{inp}\nПолучено:\n{obt}\nОжидалось:\n{exp}"
    NO_INPUT = "Тест #{test_number} не пройден.\nПолучено:\n{obt}\nОжидалось:\n{exp}"
    ONLY_TEST_NUMBER = "Тест #{test_number} не пройден.\n"

TEST_NUM = 5

@dataclass
class TestItem:
    params: dict
    compare_func: Callable[[str, str], bool]
    expected: str = ""

class BaseTaskClass:
    def __init__(
        self, 
        prog_name: str = "prog.py", 
        seed: int = 0,
        fail_on_first_test: bool = True,
        message_level = MessageLevel.ALL
    ):
        self.solution = ""
        self.prog_name = prog_name
        self.seed = seed
        self.tests: list[TestItem] = []
        self.run_timeout = RUN_TIMEOUT
        self.fail_on_first = fail_on_first_test,
        self.message_level = message_level

    def load_student_solution(self, solfile: Optional[str] = None, solcode: Optional[str] = None):
        if solcode is None and solfile is None:
            raise ValueError("Файл с решением и код не предоставлены")
        if solcode is not None and solfile is not None:
            raise ValueError("Предоставлены и файл с решением и код")
        if solcode is not None:
            self.solution = solcode
        elif solfile is not None:
            if not os.path.exists(solfile):
                raise ValueError("Ошибка: Файл решения не найден.")
            with open(solfile, "r", encoding="utf-8") as f:
                self.solution = f.read().strip()

    def check_sol_prereq(self) -> Optional[str]:
        lines = self.solution.splitlines()

        if len(lines) == 0:
            return "Ошибка: пустой файл."

        if 'import' in self.solution:
            return "Ошибка: для выполнения задания импортировать библиотеки не нужно."

        if 'exec(' in self.solution:
            return "Ошибка: использованиие функции exec() не предусмотрено заданием."

        if 'eval(' in self.solution:
            return "Ошибка: использованиие функции eval() не предусмотрено заданием."

        return None  # check is passed
    
    def write_to_file(self, libs = "", code_to_add = ""):
        with open(self.prog_name, "w", encoding="utf-8") as src:
            code = libs.format(**self.params).strip() + '\n' + self.solution.strip() + '\n' + code_to_add.format(**self.params).strip() 
            print(code, file=src)

    def generate_task(self) -> str:
        pass

    def _generate_tests(self):
        pass

    def _get_expected_test(self, libs, solution, code_to_add, params):
        code = (libs+ solution + code_to_add).strip().format(**params)
        with open("test.py", "w", encoding="utf-8") as src:
            print(code, file=src)

        try:
            output = subprocess.check_output(
                ["python3", 'test.py'], 
                input='', 
                universal_newlines=True,
                timeout=self.run_timeout
            )
            output = output.strip()
            return output
        except:
            return "error"

    def _run_solution_internal(
        self, 
        test: TestItem,
    ):
        """
        функция проверки (check_func): принимает два аргумента -- входные данные и ожидаемые результат -- и
        возвращает None, если тест успешно пройден, иначе, возвращает ожидаемый результат
        """
        self.write_to_file(self.libs.format(**test.params), self.code_to_add.format(**test.params))

        try:
            output = subprocess.check_output(
                ["python3", self.prog_name], 
                input='', 
                universal_newlines=True,
                timeout=self.run_timeout
            )
            output = output.strip()
            passed = test.compare_func(output, test.expected)
            if passed:
                return None
            return output, test.expected
        except subprocess.TimeoutExpired as te:
            return (f"Выполнение программы превысило ограничение в {te.timeout} секунд",
                    f"Программа выполняется менее {te.timeout} секунд")

    def _compare_default(self, input_str: str, obtained: str) -> bool:
        return input_str.strip() == obtained.strip()

    def run_solution(self, test: TestItem) -> Optional[str]:
        return self._run_solution_internal(test)

    def make_failed_test_msg(
        self, test_number:int, showed_input: str, obtained: str, expected: str
    ) -> str:
        """
        Формирует текст с информацией о проваленном тесте
        """
        if (self.message_level == MessageLevel.ALL):
            return self.message_level.value.format(
                test_number=test_number,
                inp=showed_input,
                obt=obtained,
                exp=expected
            )
        elif (self.message_level == MessageLevel.NO_INPUT):
            return self.message_level.value.format(
                test_number=test_number,
                obt=obtained,
                exp=expected
            )
        elif (self.message_level == MessageLevel.ONLY_TEST_NUMBER):
            return self.message_level.value.format(
                test_number=test_number
            )

    def run_tests(self) -> tuple[bool, str]:
        msgs = []
        for i in range(len(self.tests)):
            test = self.tests[i]
            result = self.run_solution(test)
            if (result is not None):
                msgs.append(self.make_failed_test_msg(
                    i+1, self.code_to_add.format(**test.params), result[0], result[1]
                ))
                if self.fail_on_first:
                    break

        if len(msgs) == 0:
            return True, "OK"
        return False, "\n".join(msgs)

    # ======== Pipeline methods ========
    def init_task(self) -> str:
        return self.generate_task()

    def check(self) -> tuple[bool, str]:
        """
        Запускает проверки на загруженном решении. **Важно**:
        `load_student_solution` должен быть вызван перед этим методом
        """

        try:
            if (msg := self.check_sol_prereq()) is not None:
                return msg
            
            self._generate_tests()
            return self.run_tests()
        except Exception as e:  # pylint: disable=W0718
            return "Ошибка при прохождении тестов"

    def make_array_failed_test_msg(
        self, caption: list[str], arrs: list[list], max_col_len: int,
        correctness: list[bool],
    ) -> str:
        """
        format:
        | i | caption[0] | caption[1] | ... | caption[N] | Correct |
        +---+------------+------------+-----+------------+---------+
        | 0 | arrs[0][0] | arrs[1][0] | ... | arrs[N][0] |    X    |
        | 1 | arrs[0][1] | arrs[1][1] | ... | arrs[N][1] |    V    |
        ....
        +---+------------+------------+-----+------------+---------+
        """
        ret = ""
        cols = ["i"]
        cols_lens = [max(len(cols[0]), len(str(len(correctness))))]
        cols += caption
        cols_lens += [max(max_col_len, len(col)) for col in cols[1:]]
        cols.append("Correct")
        correct_s, fail_s = "V", "X"
        cols_lens.append(max(map(len, (correct_s, fail_s, cols[-1]))))
        # cols_lens[:] = (col_len + 2 for col_len in cols_lens)
        ret += "| " + " | ".join(
                col.center(col_len)
                for col, col_len in zip(cols, cols_lens)
            ) + " |\n"
        separator = "+" + "+".join("-" * (col_len + 2) for col_len in cols_lens) + "+\n"
        ret += separator
        corr_iter = (correct_s if c else fail_s for c in correctness)
        for vals in zip(range(len(correctness)), *arrs, corr_iter):
            ret += "| " + " | ".join(
                self._align_value(col, col_len)
                for col, col_len in zip(vals, cols_lens)
            ) + " |\n"
        ret += separator
        return ret
