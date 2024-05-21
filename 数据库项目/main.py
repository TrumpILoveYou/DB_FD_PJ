from 数据库连接 import DB
from 管理员 import Manager
from 用户 import User
from 商户 import Merchant

db=DB()
maneger=Manager(3,"刘督")

print(maneger.get_user_info(1,1,1))
#maneger.add_user(("cxk","m","fd00001","jntm"))



def analyzeMerchantDishes(merchant_id):
    sql = ("""SELECT 
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
    result = db.execute(sql, values)
    db.close()
    return result

def analyzeUserDishSales(user_id, timeRange="1 WEEK"):
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
    values = (timeRange,user_id)
    result = db.execute(sql, values)
    db.close()
    return result

def analyzeMerchantFans(merchant_id, threshold):
    sql = ("""
                 -- 定义时间范围和商户ID
                SET @start_date = '2023-01-01';
                SET @end_date = '2023-12-31';
                SET @merchant_id = 1; -- 替换为目标商户的ID
                SET @threshold = 5; -- 替换为忠实粉丝的消费次数阈值
                
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
    values = (merchant_id,merchant_id,threshold)
    result = db.execute(sql, values)
    db.close()
    return result

def analyzeUserActivity(user_id,choice:str):

    if choice=="week":
        sql=("""-- 每周订单数量
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
        sql=("""
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

def getTheMostPopularDish(merchant_id, threshold):
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
                JOIN 
                    merchants m ON d.merchant_id = m.id
                ORDER BY 
                    total_sales DESC
                LIMIT 10;
                """
           )
    values = (merchant_id, merchant_id, threshold)
    result = db.execute(sql, values)
    db.close()
    return result
