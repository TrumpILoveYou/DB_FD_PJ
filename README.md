# 一、ER建模图
![ER](/picture/ER建模图.png)

# 二、数据库表结构说明

        
        create database canteen;
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
          `age` int NOT NULL, -- 年龄
          `password` varchar(255) NOT null,  --  密码
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        
        
        -- 商户表
        CREATE TABLE IF NOT EXISTS `merchants` (
          `id` int NOT NULL AUTO_INCREMENT, -- 商户唯一标识
          `name` varchar(255) NOT NULL, -- 姓名
          `address` varchar(255) NOT NULL, -- 地址
          `main_dish` varchar(255) NOT NULL, -- 主打菜品
           `password` varchar(255) NOT null,  -- 密码
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        
        
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
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
          PRIMARY KEY (`id`),
          FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
          FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
          FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE -- 去掉逗号
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        
        
        
        
        -- 建立的一些索引
         CREATE INDEX idx_dishes_merchant_id ON dishes(merchant_id);
        
         CREATE INDEX idx_collections_user_id ON collections(user_id);
         CREATE INDEX idx_collections_merchant_id ON collections(merchant_id);
         CREATE INDEX idx_collections_dish_id ON collections(dish_id);
        
         CREATE INDEX idx_comments_user_id ON comments(user_id);
         CREATE INDEX idx_comments_merchant_id ON comments(merchant_id);
         CREATE INDEX idx_comments_dish_id ON comments(dish_id);
        
         CREATE INDEX idx_orders_user_id ON orders(user_id);
         CREATE INDEX idx_orders_merchant_id ON orders(merchant_id);
         CREATE INDEX idx_orders_dish_id ON orders(dish_id);
         CREATE INDEX idx_orders_created_at ON orders(created_at);
        
        
        -- 收藏自动增加
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
        DELIMITER ;
        
        
        --销量增加
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
        DELIMITER ;
        
        
        SET GLOBAL event_scheduler = ON;
        -- 状态每隔一段时间更新
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
        
        
         --  初始数据准备
        INSERT INTO merchants(name, address, main_dish, password) VALUES ('张三', '东区', '烤鸭', 123456);
        INSERT INTO merchants(name, address, main_dish, password) VALUES ('李四', '西区', '火锅', 123456);
        
        insert into users(name,gender,student_id,account_information,`role`,age,password) values("刘督","男",2130,"无","学生",20,123456);
        insert into users(name,gender,student_id,account_information,`role`,age,password) values("麦佳鸿","男",2200,"无","学生",20,123456);
        
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"烤鸭",100,"烤制品","好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","豆腐");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (2,"火锅",100,"麻辣类","不好吃","https://imgse.com/i/pk6AERS","蛋白质","增肌","豆腐");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"叉烧肉",100,"烤制品","特别好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","无");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"烤排骨",100,"烤制品","非常好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","无");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"烧鹅",100,"烤制品","非常好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","无");

# 三、索引定义说明
> 我们在这个数据库中最常调用的且占用时间的，是各个表的非主键属性中含有其他表外键的（带有id字眼）的属性，给这些属性增加索引

        CREATE INDEX idx_dishes_merchant_id ON dishes(merchant_id);
        
        CREATE INDEX idx_collections_user_id ON collections(user_id);
        CREATE INDEX idx_collections_merchant_id ON collections(merchant_id);
        CREATE INDEX idx_collections_dish_id ON collections(dish_id);
        
        CREATE INDEX idx_comments_user_id ON comments(user_id);
        CREATE INDEX idx_comments_merchant_id ON comments(merchant_id);
        CREATE INDEX idx_comments_dish_id ON comments(dish_id);
        
        CREATE INDEX idx_orders_user_id ON orders(user_id);
        CREATE INDEX idx_orders_merchant_id ON orders(merchant_id);
        CREATE INDEX idx_orders_dish_id ON orders(dish_id);
        CREATE INDEX idx_orders_created_at ON orders(created_at);

# 四、触发器说明
> 我们对于几个有必要的点增加了三个触发器，见注释说明

        --收藏自动增加，触发条件：收藏表被插入时，dishes表的对应条目collection_count属性加一
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
        DELIMITER ;
        
        --销量增加，触发条件：每次下单时（orders表被插入），dishes表的对应条目销量属性加一（下单方式为online则online_sales + 1）（下单方式为queue则queue_sales + 1）
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
        DELIMITER ;
        
        --（定时事件）更新订单信息，2分钟后，将订单的状态改为“Finished”
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

# 五、自备初始化数据

> 初始数据准备，两个商户，两个用户以及一些菜品。剩下的表单的数据都由上述数据、角色操作产生

        INSERT INTO merchants(name, address, main_dish, password) VALUES ('张三', '东区', '烤鸭', 123456);
        INSERT INTO merchants(name, address, main_dish, password) VALUES ('李四', '西区', '火锅', 123456);
        
        insert into users(name,gender,student_id,account_information,`role`,age,password) values("刘督","男",2130,"无","学生",20,123456);
        insert into users(name,gender,student_id,account_information,`role`,age,password) values("麦佳鸿","男",2200,"无","学生",20,123456);
        
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"烤鸭",100,"烤制品","好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","豆腐");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (2,"火锅",100,"麻辣类","不好吃","https://imgse.com/i/pk6AERS","蛋白质","增肌","豆腐");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"叉烧肉",100,"烤制品","特别好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","无");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"烤排骨",100,"烤制品","非常好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","无");
        INSERT INTO dishes  (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens)
                         VALUES (1,"烧鹅",100,"烤制品","非常好吃","https://imgse.com/i/pk6AAG8","脂肪","增肥","无");

# 六、运行方式

*  执行环境python+PyQt5
*  先运行脚本`ccdb.sql`创建数据库以及相关表单和初始数据。然后在`数据库连接.py`文件中修改
 
       self.conn = Connection(
            host="localhost",
            port=3306,
            user="root",
            password="", # password
            autocommit=True,
        )
* 最后点击`login.py`文件运行即可。选择对应角色后登入。对于每个操作功能，在各个文本域填写适当的数据后点击对应操作按钮（如果不对会弹窗提示），所有查询类输入相关的id即可
所有插入类需要完整信息，所有删除类也是输入id即可

# 七、核心功能SQL语句说明

> 选择了一些相对复杂的sql语句，对那些很简单的查询不做说明
*     下面的代码实现评论，对于没有提供菜品id的评论视为对商家的评论（增加收藏也是类似的处理，不赘述）   

       if dish_id:
            sql = "INSERT INTO comments (user_id,merchant_id,dish_id,score,content) VALUES (%s, %s, %s, %s,%s)"
            values = (self.id, merchant_id, dish_id, score, content)
        else:
            sql = "INSERT INTO comments (user_id,merchant_id,score,content) VALUES (%s, %s, %s, %s)"
            values = (self.id, merchant_id, score, content)
*   下面的代码实现读取目标商户的所有信息，将merchant表和菜品表连接，以及获取对商家的评价（所有dishid需要为null）

        sql = ("SELECT merchants.id, merchants.name, merchants.address, merchants.main_dish, dishes.id AS dish_id, dishes.name AS dish_name, "
            "dishes.description, comments.score, comments.content "
            "FROM merchants "
            "JOIN dishes ON dishes.merchant_id = merchants.id "
            "LEFT JOIN comments ON comments.merchant_id = merchants.id AND comments.dish_id IS NULL "
            "WHERE merchants.id = %s")
        values = (merchant_id,)
> 下面是进阶部分

* 下面的代码实现菜品数据分析：某个商户所有菜品的评分、销量以及购买该菜品次数最多的人。将菜品、评论、用户连接，再连接嵌套子查询（获取用户点某个菜品的次数），
分组聚集后获得菜品平均得分,MAX(order_count)确定了选择点单最多的人。

      sql = ("""


        SELECT 
                                 d.id AS dish_id,
                                 d.name AS dish_name,
                                 IFNULL(AVG(c.score), 0) AS average_score,
                                 d.queue_sales + d.online_sales AS total_sales,
                                 u.id AS top_buyer_id,
                                 u.name AS top_buyer_name,
                                 MAX(order_count) AS top_buyer_order_count
                           FROM
                                 dishes d
                           LEFT JOIN
                                 comments c ON d.id = c.dish_id
                           LEFT JOIN
                                 (
                                    SELECT
                                      o.dish_id,
                                      o.user_id,
                                      u.name,
                                      COUNT(o.id) AS order_count
                                    FROM
                                      orders o
                                    INNER JOIN
                                      users u ON o.user_id = u.id
                                    GROUP BY
                                      o.dish_id, o.user_id, u.name
                                  ) AS user_orders ON d.id = user_orders.dish_id
                            LEFT JOIN
                                    users u ON user_orders.user_id = u.id
                            WHERE
                              d.merchant_id = %s
                            GROUP BY
                              d.id, u.id
                            ORDER BY
                              d.id, top_buyer_order_count DESC;""")
                ""
                values = (merchant_id)
* 下面的代码实现用户收藏各个菜品在一段时间各个点餐方式销量

        sql = ("""
        
                        SELECT
                            d.id AS dish_id,
                            d.name AS dish_name,
                            d.queue_sales,
                            d.online_sales
                        FROM
                            collections c
                        JOIN
                            dishes d ON c.dish_id = d.id
                        LEFT JOIN
                            orders o ON d.id = o.dish_id AND o.created_at BETWEEN %s AND %s
                        WHERE
                            c.user_id = %s
                        GROUP BY
                            d.id, d.name
                        ORDER BY
                            d.name;""")
            values = (start, end, user_id)
* 下面的代码实现某商户忠实粉丝各个菜品购买次数，嵌套子查询是确定购买量大于阈值

        sql = ("""
                        
                        -- 查询忠实粉丝在各个菜品上的购买次数分布
                        SELECT
                            u.id AS user_id,
                            u.name AS user_name,
                            d.id AS dish_id,
                            d.name AS dish_name,
                            COUNT(o.id) AS purchase_count
                        FROM
                            orders o
                        JOIN
                            users u ON o.user_id = u.id
                        JOIN
                            dishes d ON o.dish_id = d.id
                        WHERE
                            o.merchant_id = %s
                            AND o.created_at BETWEEN %s AND %s
                            AND o.user_id IN (
                                SELECT
                                    user_id
                                FROM
                                    orders
                                WHERE
                                    merchant_id = %s
                                    AND created_at BETWEEN %s AND %s
                                GROUP BY
                                    user_id
                                HAVING
                                    COUNT(id) > %s
                            )
                        GROUP BY
                            u.id, d.id
                        ORDER BY
                            u.id, d.id;
                        """
                   )
            values = (merchant_id, start_date, end_date, merchant_id, start_date, end_date, threshold)

* 下面的代码实现用户活跃度分析，很简单，不赘述

        sql = ("""
                        SELECT 
                            user_id,
                            name,
                            COUNT(*) AS orders_count
                        FROM 
                            orders
                        join users on orders.user_id=users.id
                        where created_at between %s and %s
                        GROUP BY
                           user_id,name
                        """)
            values = (start,end)
* 下面的代码实现取得商家最受欢迎的菜品，很简单，让总销量倒序排列即可，限制只显示TOP3

        sql = ("""
                        SELECT 
                            d.id AS dish_id,
                            d.name AS dish_name,
                            (d.queue_sales + d.online_sales) AS total_sales
                        FROM 
                            dishes d
                        JOIN 
                            merchants m ON d.merchant_id = m.id
                        WHERE 
                            m.id=%s
                        ORDER BY 
                            (d.queue_sales + d.online_sales) DESC
                        LIMIT 3;
                        """
                   )
            values = (merchant_id)