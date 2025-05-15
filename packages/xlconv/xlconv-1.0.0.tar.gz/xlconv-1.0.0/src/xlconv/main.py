# Copyright (c) 2025, lujiawan <lujiawan@163.com>

import os
from src.xlconv import xlconv


def main():
    """
    :function: 将构造的数据,从excel获取并转换为json,再写入到文件
    :param file: xlsx/xls文件名称
    :return: json写文件,同一类Json写入同一个目录,唯一标识作为文件名
    """
    # 项目路径
    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # log
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s  %(filename)s:%(lineno)d %(message)s')
    logger = logging.getLogger('xlconv')
    # 获取文件
    tmp_file=sys.argv[1]
    # 获取绝对路径
    file_path=os.path.normpath(os.path.join(project_path,tmp_file))
    # 获取文件名
    obj_file_path=os.path.split(file_path)[0]
    file_name=os.path.split(file_path)[1]

    if file_path:
        xlsx_book = xlrd.open_workbook(filename=file_path)
    else:
        logger.error(f"没有查找到文件! 文件名称: {file}.")
        sys.exit()
    id_key,cases_set = getJsonSet(xlsx_book)
    print(id_key,cases_set)
    if cases_set is None:
        logger.error(f"页面'Json集'无数据")
        # 兼容非标准的格式转换
        sys.exit()
    json_data = dict()
    for case in cases_set:
        logger.info(f"{cases_set[case]}")
        json_data[case] = xlConvJson(xlsx_book,cases_set[case],id_key,case)
        os.makedirs(str(cases_set[case]), exist_ok=True)
        with open(str(cases_set[case]) + "/" + case + ".json", "w", encoding="utf-8") as f:
            f.write(str(json.dumps(json_data[case],ensure_ascii=False)))  


if __name__ == "__main__":
    main()
