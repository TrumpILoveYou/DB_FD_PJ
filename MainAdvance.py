from 数据库连接 import DB
from 管理员 import Manager
from 用户 import User
from 商户 import Merchant
from 菜品 import Dish
from 订单 import Order

db = DB()
maneger = Manager(1, "刘督")

#print(maneger.get_user_info(1,1,1))
#maneger.add_user(User(888,"ld","m","fd20","666","student",23))
#maneger.add_merchant(Merchant(65656556,"mayun","china","vege,fish"))

#merchant=Merchant(1,"mayun","china","vege,fish")
user = User(1, "ld", "m", "fd20", "666", "student", 23)
#user.comment(1,1,5,"nice")
print(user.getUserHistoryOrders(1, 2, 1)
      )


#user.createOrder(Order(10,"Queue",1,1,1,"dwada"))
#print(maneger.get_user_info(1,1,1))
#merchant.add_dish(Dish(1,1,"fish",10,"meat","delicious","baidu","danbai","wu","wu",0,0,0))
#user.comment(1,1,5,"好吃")
#user.createOrder(Order(5,"Queue",1,1,1,"false"))
#merchant.delete_dish(1)
def analyzeMerchantDishes(merchant_id):
    """菜品数据分析：某个商户所有菜品的评分 、销量以及购买该菜品次数最多的人"""
    sql = ("""
                WITH user_orders AS (
        SELECT
            o.dish_id,
            o.user_id,
            COUNT(o.id) AS order_count
        FROM
            orders o
        GROUP BY
            o.dish_id, o.user_id
    ), top_buyers AS (
        SELECT
            dish_id,
            user_id,
            MAX(order_count) AS top_buyer_order_count
        FROM
            user_orders
        GROUP BY
            dish_id
    )
    SELECT 
        d.id AS dish_id,
        d.name AS dish_name,
        IFNULL(AVG(c.score), 0) AS average_score,
        d.queue_sales + d.online_sales AS total_sales,
        tb.top_buyer_order_count,
        u.name AS top_buyer_name
    FROM
        dishes d
    LEFT JOIN
        comments c ON d.id = c.dish_id
    LEFT JOIN
        top_buyers tb ON d.id = tb.dish_id
    LEFT JOIN
        users u ON tb.user_id = u.id
    WHERE
        d.merchant_id = %s
    GROUP BY
        d.id, tb.top_buyer_order_count, u.name
    ORDER BY
        d.id, tb.top_buyer_order_count DESC;""")
    values = (merchant_id)
    result = db.execute(sql, values)
    db.close()
    return result


def analyzeUserDishSales(user_id, timeRange="1 WEEK"):
    """某用户收藏的各个菜品在一段时间（近一周，近一月，近一年）内不同点餐
方式的销量可进行筛选。界面上不要求用可视化图表来显示菜品销量对应关系。"""
    sql = ("""
                SET @start_date = DATE_SUB(CURDATE(), INTERVAL %s);
                SET @end_date = CURDATE();
                
                SELECT
                    d.id AS dish_id,
                    d.name AS dish_name,
                    d.queue_sales,
                    d.online_sales,
                    SUM(CASE WHEN o.order_status = 'queue' THEN 1 ELSE 0 END) AS queue_sales_within_period,
                    SUM(CASE WHEN o.order_status = 'online' THEN 1 ELSE 0 END) AS online_sales_within_period
                FROM
                    collections c
                JOIN
                    dishes d ON c.dish_id = d.id
                LEFT JOIN
                    orders o ON d.id = o.dish_id AND o.created_at BETWEEN @start_date AND @end_date
                WHERE
                    c.user_id = %s
                GROUP BY
                    d.id, d.name
                ORDER BY
                    d.name;""")
    values = (timeRange, user_id)
    result = db.execute(sql, values)
    db.close()
    return result


def analyzeMerchantFans(merchant_id, threshold):
    """一段时间内某个商户的忠实粉丝在该商户的消费分布。"""
    sql = ("""
                 -- 定义时间范围和商户ID
                SET @start_date = '2023-01-01';
                SET @end_date = '2025-12-31';
                
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
                    AND o.created_at BETWEEN @start_date AND @end_date
                    AND o.user_id IN (
                        SELECT
                            user_id
                        FROM
                            orders
                        WHERE
                            merchant_id = %s
                            AND created_at BETWEEN @start_date AND @end_date
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
    values = (merchant_id, merchant_id, threshold)
    result = db.execute(sql, values)
    db.close()
    return result


def analyzeUserActivity(user_id, choice: str):
    """用户活跃度分析：分析用户的活跃度模式，包括每周、每月点餐频率的变化
趋势，以及用户在不同时间段的活跃程度。"""
    if choice == "week":
        sql = ("""-- 每周订单数量
                SELECT 
                    'weekly' AS period_type,
                    YEARWEEK(created_at, 1) AS period, 
                    COUNT(*) AS orders_count
                FROM 
                    orders
                WHERE 
                    user_id = %s
                GROUP BY 
                    YEARWEEK(created_at, 1)
                UNION ALL""")
    else:
        #choice=="month":
        sql = ("""
        -- 每月订单数量
                SELECT 
                    'monthly' AS period_type,
                    DATE_FORMAT(created_at, '%Y-%m') AS period, 
                    COUNT(*) AS orders_count
                FROM 
                    orders
                WHERE 
                    user_id =%s
                GROUP BY 
                    DATE_FORMAT(created_at, '%Y-%m')
                UNION ALL
        """)
    values = (user_id)
    result = db.execute(sql, values)
    db.close()
    return result


def getTheMostPopularDish(merchant_id):
    sql = ("""
                SELECT 
                    d.id AS dish_id,
                    d.name AS dish_name,
                    d.merchant_id,
                    m.name AS merchant_name,
                    d.queue_sales,
                    d.online_sales,
                    (d.queue_sales + d.online_sales) AS total_sales
                FROM 
                    dishes d
                where d.merchant_id=%s
                JOIN 
                    merchants m ON d.merchant_id = m.id
                ORDER BY 
                    total_sales DESC
                """
           )
    values = (merchant_id)
    result = db.execute(sql, values)
    db.close()
    return result
