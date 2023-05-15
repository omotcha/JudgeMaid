import os
from config.common import tmp_dir

target_dir = os.path.join(tmp_dir, "txt_pool")

replacement = {
    r"\n": r" ",
    r"\r": r" ",
    r"\n\r": r" "
}


def remove_splitters(splitters: list, fin: str or os.PathLike, fout: str or os.PathLike) -> None:
    """
    remove the splitters
    :param splitters: list of splitter(e.g. "\n")
    :param fin: input file
    :param fout: output file
    :return:
    """
    for splitter in splitters:
        if splitter not in replacement.keys():
            return
    result = []
    with open(os.path.join(target_dir, fin), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            new_line = line
            for splitter in splitters:
                new_line = new_line.replace(splitter, replacement[splitter])
            result.append(new_line)
    with open(os.path.join(target_dir, fout), 'a', encoding='utf-8') as f:
        f.writelines(result)


if __name__ == '__main__':
    remove_splitters([r'\n'], fin="01_raw.txt", fout="01_split.txt")
