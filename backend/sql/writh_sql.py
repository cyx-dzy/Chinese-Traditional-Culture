import pymysql
import csv
import os

# 数据库连接配置（请根据实际情况修改）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "135792468aB.",  # 替换为实际密码
    "database": "ancient_building",
    "charset": "utf8mb4",
}


def insert_csv_to_table(cursor, table_name, csv_file, columns=None, extra_process=None):
    """
    从CSV文件插入数据到指定表
    :param cursor: 数据库游标
    :param table_name: 表名
    :param csv_file: CSV文件路径
    :param columns: 需要插入的列名列表，若为None则使用CSV的第一行所有列
    :param extra_process: 可选函数，对每行数据值进行额外处理，函数原型 extra_process(values, row) -> values
    """
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if columns is None:
            columns = reader.fieldnames
        # 构造插入SQL
        placeholders = ", ".join(["%s"] * len(columns))
        cols = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        for row in reader:
            values = []
            for col in columns:
                val = row.get(col, None)
                # 把空字符串、“无”、“待考究”等占位符统一当成 NULL
                if isinstance(val, str):
                    if val.strip() in ("", "无", "待考究"):
                        val = None
                values.append(val)
            if extra_process:
                values = extra_process(values, row)
            try:
                cursor.execute(sql, values)
            except Exception as e:
                print(f"插入 {table_name} 时出错: {e}")
                print("问题行:", row)
                raise


def main():
    # 连接数据库
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 数据文件目录：当前脚本所在目录（即 backend/sql，下有 *.csv）
    base_dir = os.path.dirname(__file__)
    data_dir = base_dir

    # 1. 插入 buildings（CSV 不含 id，id 由数据库自增）
    buildings_csv = os.path.join(data_dir, "buildings.csv")
    print("正在导入 buildings...")
    buildings_columns = [
        "name",
        "name_en",
        "dynasty",
        "location",
        "category",
        "summary",
        "cover_image",
        "height",
        "bay_count",
        "dougong_types",
        "earthquake_resistance",
        "material",
        "preservation_status",
    ]
    insert_csv_to_table(cursor, "buildings", buildings_csv, columns=buildings_columns)
    conn.commit()

    # 2. 插入 building_details（CSV 不含 id，id 由数据库自增）
    details_csv = os.path.join(data_dir, "building_details.csv")
    print("正在导入 building_details...")
    details_columns = [
        "building_id",
        "section_type",
        "title",
        "content",
        "sort_order",
    ]
    insert_csv_to_table(
        cursor, "building_details", details_csv, columns=details_columns
    )
    conn.commit()

    # 3. 插入 images（CSV 不含 id，id 由数据库自增；需要处理 is_cover 字段）
    images_csv = os.path.join(data_dir, "images.csv")
    print("正在导入 images...")
    images_columns = [
        "building_id",
        "image_path",
        "image_type",
        "caption",
        "sort_order",
        "is_cover",
    ]

    def process_images(values, row):
        # is_cover 在列表中的索引为5（从0开始）
        if values[5] is not None:
            # 将 'TRUE'/'FALSE' 或 '1'/'0' 转为整数 1/0
            if isinstance(values[5], str):
                if values[5].upper() == "TRUE" or values[5] == "1":
                    values[5] = 1
                else:
                    values[5] = 0
            else:
                values[5] = int(values[5])
        return values

    insert_csv_to_table(
        cursor,
        "images",
        images_csv,
        columns=images_columns,
        extra_process=process_images,
    )
    conn.commit()

    # 4. 插入 faq（CSV 不含 id，id 由数据库自增）
    faq_csv = os.path.join(data_dir, "faq.csv")
    print("正在导入 faq...")
    faq_columns = ["question", "answer", "sort_order"]
    insert_csv_to_table(cursor, "faq", faq_csv, columns=faq_columns)
    conn.commit()

    cursor.close()
    conn.close()
    print("所有数据导入成功！")


if __name__ == "__main__":
    main()
