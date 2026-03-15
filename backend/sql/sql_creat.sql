-- 创建数据库（如果尚未创建）
CREATE DATABASE IF NOT EXISTS ancient_building 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ancient_building;

-- 1. 建筑主表 buildings
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='建筑主表';

-- 2. 建筑详情章节表 building_details
CREATE TABLE IF NOT EXISTS building_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    building_id INT NOT NULL COMMENT '关联建筑ID',
    section_type VARCHAR(20) NOT NULL COMMENT '章节类型',
    title VARCHAR(200) NOT NULL COMMENT '章节标题',
    content TEXT COMMENT '详细描述',
    sort_order INT DEFAULT 0 COMMENT '排序',
    FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='建筑详情';

-- 3. 图片资源表 images
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图片资源表';

-- 4. 常见问题表 faq
CREATE TABLE IF NOT EXISTS faq (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(200) NOT NULL,
    answer TEXT NOT NULL,
    sort_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='常见问题';