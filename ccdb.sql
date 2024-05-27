

-- 管理员表
CREATE TABLE IF NOT EXISTS `managers` (
  `id` int NOT NULL AUTO_INCREMENT, -- 管理员唯一标识
  `name` varchar(255) NOT NULL, -- 姓名
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT, -- 用户唯一标识
  `name` varchar(255) NOT NULL, -- 姓名
  `gender` varchar(1) NOT NULL, -- 性别
  `student_id` varchar(255) NOT NULL, -- 学生ID
  `account_information` varchar(255) NOT NULL, -- 账户信息
  `role` varchar(255) NOT NULL, -- 用户角色
  `age` int NOT NULL, -- 
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
ALTER TABLE `users`
ADD COLUMN `password` varchar(255) NOT NULL;

-- 商户表
CREATE TABLE IF NOT EXISTS `merchants` (
  `id` int NOT NULL AUTO_INCREMENT, -- 商户唯一标识
  `name` varchar(255) NOT NULL, -- 姓名
  `address` varchar(255) NOT NULL, -- 地址
  `main_dish` varchar(255) NOT NULL, -- 主打菜品
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
ALTER TABLE `merchants`
ADD COLUMN `password` varchar(255) NOT NULL;

-- 菜品表
CREATE TABLE IF NOT EXISTS `dishes` (
  `id` int NOT NULL AUTO_INCREMENT, -- 菜品唯一标识
  `merchant_id` int NOT NULL, -- 商户
  `name` varchar(255) NOT NULL, -- 名称
  `price` decimal(10,2) NOT NULL, -- 价格
  `category` varchar(255) NOT NULL, -- 类别
  `description` text NOT NULL, -- 描述
  `image` varchar(255) NOT NULL, -- 图像
  `ingredients` text NOT NULL, -- 成分
  `nutrition_information` text NOT NULL, -- 营养信息
  `allergens` text NOT NULL, -- 过敏源
  `queue_sales` int NOT NULL DEFAULT 0, -- 现场排队销量
  `online_sales` int NOT NULL DEFAULT 0, -- 在线点餐销量
  `collection_count` int NOT NULL DEFAULT 0, -- 被收藏量
  PRIMARY KEY (`id`),
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- 收藏表
CREATE TABLE IF NOT EXISTS `collections` (
  `id` int NOT NULL AUTO_INCREMENT, -- 收藏唯一标识
  `user_id` int NOT NULL, -- 用户唯一标识
  `merchant_id` int NOT NULL, -- 商户唯一标识
  `dish_id` int, -- 菜品唯一标识
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 评价表
CREATE TABLE IF NOT EXISTS `comments` (
  `id` int NOT NULL AUTO_INCREMENT, -- 评价唯一标识
  `user_id` int NOT NULL, -- 用户唯一标识
  `merchant_id` int NOT NULL, -- 商户唯一标识
  `dish_id` int, -- 菜品唯一标识
  `score` int NOT NULL, -- 评分
  `content` text NOT NULL, -- 评价内容
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT, -- 订单唯一标识
  `method` varchar(255) NOT NULL, -- 下单方式
  `user_id` int NOT NULL, -- 用户唯一标识
  `merchant_id` int NOT NULL, -- 商户唯一标识
  `dish_id` int NOT NULL, -- 菜品唯一标识
  `order_status` varchar(255) NOT NULL, -- 订单状态
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE -- 去掉逗号
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





-- CREATE INDEX idx_dishes_merchant_id ON dishes(merchant_id);

-- CREATE INDEX idx_collections_user_id ON collections(user_id);
-- CREATE INDEX idx_collections_merchant_id ON collections(merchant_id);
-- CREATE INDEX idx_collections_dish_id ON collections(dish_id);

-- CREATE INDEX idx_comments_user_id ON comments(user_id);
-- CREATE INDEX idx_comments_merchant_id ON comments(merchant_id);
-- CREATE INDEX idx_comments_dish_id ON comments(dish_id);

-- CREATE INDEX idx_orders_user_id ON orders(user_id);
-- CREATE INDEX idx_orders_merchant_id ON orders(merchant_id);
-- CREATE INDEX idx_orders_dish_id ON orders(dish_id);
-- CREATE INDEX idx_orders_created_at ON orders(created_at);


/*-- 收藏自动增加
DELIMITER //
CREATE TRIGGER update_collection_count_after_insert
AFTER INSERT ON collections
FOR EACH ROW
BEGIN
    IF NEW.dish_id IS NOT NULL THEN
        UPDATE dishes
        SET collection_count = collection_count + 1
        WHERE id = NEW.dish_id;
    END IF;
END//
DELIMITER ;'''


'''--销量增加
DELIMITER //
CREATE TRIGGER update_sales_after_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.method = 'online' THEN
        UPDATE dishes
        SET online_sales = online_sales + 1
        WHERE id = NEW.dish_id;
    ELSEIF NEW.method = 'queue' THEN
        UPDATE dishes
        SET queue_sales = queue_sales + 1
        WHERE id = NEW.dish_id;
    END IF;
END//
DELIMITER ;*/


SET GLOBAL event_scheduler = ON;

DELIMITER //
CREATE EVENT IF NOT EXISTS update_order_status
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    UPDATE orders
    SET order_status = 'Finished'
    WHERE order_status != 'Finished'
    AND created_at <= NOW() - INTERVAL 2 MINUTE;
END//
DELIMITER ;

