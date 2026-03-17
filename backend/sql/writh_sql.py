import pymysql
import csv
import os
import sys

# 数据库连接配置（从环境变量获取）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("DB_PASSWORD"),
    "database": "ancient_building",
    "charset": "utf8mb4",
}

if not DB_CONFIG["password"]:
    print("错误: 未设置数据库密码环境变量 DB_PASSWORD")
    sys.exit(1)


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
    # 先创建数据库（如果不存在）
    print("正在创建数据库...")
    temp_conn = pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        charset=DB_CONFIG["charset"]
    )
    temp_cursor = temp_conn.cursor()
    
    # 创建数据库
    temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"数据库 {DB_CONFIG['database']} 已准备就绪")
    
    temp_cursor.close()
    temp_conn.close()
    
    # 连接到目标数据库
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 创建表结构
    print("正在创建表结构...")
    
    # 1. 建筑主表 buildings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buildings (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL COMMENT '建筑名称',
            name_en VARCHAR(100) COMMENT '英文名称',
            dynasty VARCHAR(50) NOT NULL COMMENT '朝代',
            location VARCHAR(200) COMMENT '地点',
            category VARCHAR(20) NOT NULL COMMENT '所属分类',
            summary TEXT COMMENT '简短描述（用于卡片）',
            cover_image VARCHAR(500) COMMENT '封面图片路径',
            height DECIMAL(5,2) COMMENT '高度（米）',
            bay_count VARCHAR(20) COMMENT '面阔间数，如"七间"',
            dougong_types VARCHAR(50) COMMENT '斗拱种类数，如"54种"',
            earthquake_resistance VARCHAR(50) COMMENT '抗震情况，如"经历40余次地震"',
            material VARCHAR(100) COMMENT '主要材料，如"木、砖"',
            preservation_status VARCHAR(50) COMMENT '保存状况，如"完好"',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='建筑主表'
    """)
    
    # 2. 建筑详情章节表 building_details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS building_details (
            id INT PRIMARY KEY AUTO_INCREMENT,
            building_id INT NOT NULL COMMENT '关联建筑ID',
            section_type VARCHAR(20) NOT NULL COMMENT '章节类型',
            title VARCHAR(200) NOT NULL COMMENT '章节标题',
            content TEXT COMMENT '详细描述',
            sort_order INT DEFAULT 0 COMMENT '排序',
            FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='建筑详情'
    """)
    
    # 3. 图片资源表 images
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INT PRIMARY KEY AUTO_INCREMENT,
            building_id INT NOT NULL COMMENT '所属建筑ID',
            image_path VARCHAR(500) NOT NULL COMMENT '图片存储路径（相对于public目录）',
            image_type VARCHAR(20) DEFAULT '其他' COMMENT '图片类型',
            caption VARCHAR(200) COMMENT '图片说明文字',
            sort_order INT DEFAULT 0 COMMENT '排序',
            is_cover BOOLEAN DEFAULT FALSE COMMENT '是否为封面',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE,
            INDEX idx_building (building_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图片资源表'
    """)
    
    # 4. 常见问题表 faq
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faq (
            id INT PRIMARY KEY AUTO_INCREMENT,
            question VARCHAR(200) NOT NULL,
            answer TEXT NOT NULL,
            sort_order INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='常见问题'
    """)
    
    # 清空表数据
    print("正在清空表数据...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE building_details")
    cursor.execute("TRUNCATE TABLE images")
    cursor.execute("TRUNCATE TABLE faq")
    cursor.execute("TRUNCATE TABLE buildings")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    print("表结构已创建并清空")
    
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
