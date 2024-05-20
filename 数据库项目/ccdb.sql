-- 管理员表
CREATE TABLE IF NOT EXISTS `managers` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 管理员唯一标识
  `name` varchar(255) NOT NULL, -- 姓名
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 用户唯一标识
  `name` varchar(255) NOT NULL, -- 姓名
  `gender` varchar(1) NOT NULL, -- 性别
  `student_id` varchar(255) NOT NULL, -- 学生ID
  `account_information` varchar(255) NOT NULL, -- 账户信息
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 商户表
CREATE TABLE IF NOT EXISTS `merchants` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 商户唯一标识
  `name` varchar(255) NOT NULL, -- 姓名
  `address` varchar(255) NOT NULL, -- 地址
  `main_dish` varchar(255) NOT NULL, -- 主打菜品
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 菜品表
CREATE TABLE IF NOT EXISTS `dishes` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 菜品唯一标识
  `name` varchar(255) NOT NULL, -- 名称
  `price` decimal(10,2) NOT NULL, -- 价格
  `category` varchar(255) NOT NULL, -- 类别
  `description` text NOT NULL, -- 描述
  `image` varchar(255) NOT NULL, --图像
  `ingredients` text NOT NULL, -- 成分
  `nutrition_information` text NOT NULL, -- 营养信息
  `allergens` text NOT NULL, -- 过敏源
  `queue_sales` int(11) NOT NULL, -- 现场排队销量
  `online_sales` int(11) NOT NULL, -- 在线点餐销量
  `collection_count` int(11) NOT NULL, -- 被收藏量
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 收藏表
CREATE TABLE IF NOT EXISTS `collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 收藏唯一标识
  `user_id` int(11) NOT NULL, -- 用户唯一标识
  `merchant_id` int(11) NOT NULL, -- 商户唯一标识
  `dish_id` int(11) NOT NULL, -- 菜品唯一标识
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`),
  FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 评价表
CREATE TABLE IF NOT EXISTS `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 评价唯一标识
  `user_id` int(11) NOT NULL, -- 用户唯一标识
  `merchant_id` int(11) NOT NULL, -- 商户唯一标识
  `dish_id` int(11) NOT NULL, -- 菜品唯一标识
  `score` int(11) NOT NULL, -- 评分
  `content` text NOT NULL, -- 评价内容
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`),
  FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 订单表
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 订单唯一标识
  `user_id` int(11) NOT NULL, -- 用户唯一标识
  `merchant_id` int(11) NOT NULL, -- 商户唯一标识
  `dish_id` int(11) NOT NULL, -- 菜品唯一标识
  `quantity` int(11) NOT NULL, -- 数量
  `order_status` varchar(255) NOT NULL, -- 订单状态
  `message_id` int(11) NOT NULL, -- 消息唯一标识
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`),
  FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`),
  FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 消息表
CREATE TABLE IF NOT EXISTS `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT, -- 消息唯一标识
  `type` varchar(255) NOT NULL, -- 消息类型
  `content` text NOT NULL, -- 消息内容
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
