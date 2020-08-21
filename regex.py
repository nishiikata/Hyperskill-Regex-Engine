
# Stage 1
def single_or_empty_char(regex: str, literal: str) -> bool:
    if regex == "":
        print(True)
    elif literal == "":
        print(False)
    elif regex == ".":
        print(True)
    else:
        return regex == literal


# Stage 2
def equal_len(regex: str, literal: str) -> bool:
    if regex == "":
        return True
    elif literal == "":
        return False
    elif regex[0] != "." and regex[0] != literal[0]:
        return False
    else:
        return equal_len(regex[1:], literal[1:])


# Stage 3
def different_len(regex: str, literal: str) -> bool:
    equal_len_matches: bool = equal_len(regex, literal)

    if equal_len_matches:
        return True
    elif literal == "":
        return False
    else:
        return different_len(regex, literal[1:])


# Stage 4
def fix_operators(regex: str, literal: str) -> bool:
    if regex.startswith("^"):
        regex: str = regex.replace("^", "")
        regex_removed_suffix: str = regex.replace("$", "")
        for i in range(len(regex_removed_suffix)):
            if regex_removed_suffix[i] != "." and regex_removed_suffix[i] != literal[i]:
                return False

    if regex.endswith("$"):
        regex: str = regex.replace("$", "")
        for i in range(-1, -1 - len(regex), -1):
            if regex[i] != "." and regex[i] != literal[i]:
                return False

    return different_len(regex, literal)


# Stage 5 - sub-helper function
def current_scenario(base: list, index: int, symbol: str, literal_len: int) -> list:
    scenario_branches: list = []

    if symbol in ["?", "*"]:
        base_copy: list = base[:]
        base_copy[index] = ""
        scenario_branches.append(base_copy)

    if symbol in ["*", "+"]:
        offset: int = 0
        if base[0] == "^":
            offset += 1
        if base[-1] == "$":
            offset += 1

        repeat_count: int = 2
        current_len: int = len(base) + repeat_count - 1

        max_len: int = literal_len + offset
        while current_len <= max_len:
            base_copy: list = base[:]
            index_char: str = base_copy[index]
            base_copy[index] = index_char * repeat_count
            scenario_branches.append(base_copy)
            repeat_count += 1
            current_len += 1

    return scenario_branches


# Stage 5 - helper function
def find_scenarios(base: list, idx_with_meta: dict, max_len: int) -> list:
    all_scenarios: list = [base]
    for index, meta in idx_with_meta.items():
        current_scenarios: list = all_scenarios[:]
        for scenario in current_scenarios:
            all_scenarios.extend(current_scenario(scenario, index, meta, max_len))

    return ["".join(scenario) for scenario in all_scenarios]


# Stage 5
def repetition_operators(regex: str, literal: str, escape: dict = None):
    """
    Retroactively added :param dict escape:
    to this function during Stage 6 implementation
    """

    meta_char: list = ["?", "*", "+"]
    if all(char not in meta_char for char in regex):
        return fix_operators(regex, literal)

    index_meta: dict = {}

    if escape is None:
        escape: dict = {}

    for i in range(1, len(regex)):
        if regex[i] in meta_char and escape.get(i) is None:
            offset = len(index_meta)
            index_meta[i - 1 - offset] = regex[i]

    base_chars: list = [v for i, v in enumerate(regex) if v not in meta_char or escape.get(i)]
    scenarios: list = find_scenarios(base_chars, index_meta, len(literal))

    for regex_scenario in scenarios:
        current_eval: bool = fix_operators(regex_scenario, literal)
        if current_eval:
            return True

    return False


# Stage 6
def escape_operator(regex, string):
    if all(char != "\\" for char in regex):
        return repetition_operators(regex, string)

    index_meta: dict = {}
    offset: int = 0
    base_chars: list = []

    for i in range(len(regex)):
        if regex[i] == "\\":
            if i > 0 and index_meta.get(i - offset) is not None:
                base_chars.append(regex[i])
                continue

            index_meta[i - offset] = "\\"
            offset = len(index_meta)
        else:
            base_chars.append(regex[i])

    base_chars_str: str = "".join(base_chars)

    return repetition_operators(base_chars_str, string, index_meta)


if __name__ == "__main__":
    regex_input, string_input = input().split("|")
    print(escape_operator(regex_input, string_input))
