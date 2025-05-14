import os

import numpy as np


def remove_toprule(s):
    return s.replace("\\toprule\n", "")


def remove_bottomrule(s):
    return s.replace("\\bottomrule\n", "")


def replace_midrule_with_hline(s):
    return s.replace("\\midrule", "\\hline")


def replace_bottomrule_with_hline(s):
    return s.replace("\\bottomrule", "\\hline")


def change_header(s, header_list):
    lines = s.split("\n")
    header_line = lines[2]
    new_header_line = " & ".join(header_list) + " \\\\"
    new_lines = lines[:2] + [new_header_line] + lines[3:]
    new_s = "\n".join(new_lines)

    return new_s


def change_values_title(s, new_values_title):
    lines = s.split("\n")
    values_line = lines[-4]
    values_list = values_line.split("&")

    new_values_list = [new_values_title + " "] + values_list[1:]
    new_values_line = "&".join(new_values_list)
    new_lines = lines[:4] + [new_values_line] + lines[5:]
    s = "\n".join(new_lines)

    return s


def add_hline(s, line_number_from_end=3):
    """Add hline at line_number_from_end.

    The default '3' corresponds to
    adding a line before the last line of the table.
    """
    lines = s.split("\n")
    new_lines = (
        lines[:-line_number_from_end] + ["\\hline"] + lines[-line_number_from_end:]
    )

    return "\n".join(new_lines)


def format_table(s, header_list=None, new_values_title=None):
    if header_list is not None:
        s = change_header(s, header_list)
    if new_values_title is not None:
        s = change_values_title(s, new_values_title)
    s = remove_toprule(s)
    s = remove_bottomrule(s)
    s = replace_midrule_with_hline(s)
    #     s = replace_bottomrule_with_hline(s)
    return s


def write_table_to_file(s, variable, dirpath):
    with open(os.path.join(dirpath, variable + "_table.tex"), "w") as f:
        f.write(s)


def boldify_line(line, words_to_boldify):
    for word in words_to_boldify:
        line = line.replace(word, "\\textbf{" + f"{word}" + "}")
    return line


def get_latex_table_bold_col_header(df2, round_n_digits=1):
    table_lines = df2.round(round_n_digits).to_latex().split("\\\\")

    col_headers = list(df2.columns.str.replace("%", "\\%").str.replace("_", "\\_"))
    new_line0 = boldify_line(table_lines[0], col_headers)

    boldified_table = "\\\\".join([new_line0] + table_lines[1:])
    return boldified_table


def get_n_decimals_to_include(std, min_n_decimals=1):
    # If std == 0, return min_n_decimals, otherwise we get an error when applying the log
    if std == 0:
        return min_n_decimals

    n_decimals_to_include = -(np.log10(std).round() - 1)

    if n_decimals_to_include < 1:
        return min_n_decimals
    else:
        return int(n_decimals_to_include)
