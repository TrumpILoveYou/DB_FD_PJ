from datetime import datetime, timedelta
from 数据库连接 import DB
from 管理员 import Manager
from 用户 import User

db = DB()

def analyzeMerchantDishes(merchant_id):
    #  菜品数据分析：某个商户所有菜品的评分、销量以及购买该菜品次数最多的人。
    sql = ("""
              WITH user_orders(dish_id,user_id,name,order_count) as(
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
              
              
              )
              
              
              
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
                      user_orders ON d.id = user_orders.dish_id
                LEFT JOIN
                        users u ON user_orders.user_id = u.id
                where
                    u.id=%s
                GROUP BY
                  d.id, u.id
                ORDER BY
                  d.id, top_buyer_order_count DESC;""")
    ""
    values = (merchant_id)
    result = db.execute(sql, values)
    db.close()
    return result

def analyzeUserDishSales(user_id,time_range_type="week"):
    # 用户收藏各个菜品在一段时间各个点餐方式销量

    # 获取当前时间
    end_date = datetime.now()

    # 格式化时间为 'YYYY-MM-DD' 形式
    end = end_date.strftime('%Y-%m-%d')

    # 减去一
    if time_range_type=="week":
        one_ago = end_date - timedelta(weeks=1)
    elif time_range_type=="month":
        one_ago = end_date - timedelta(weeks=4.3)
    elif time_range_type == "year":
        one_ago = end_date - timedelta(weeks=4.3*12)
    else:
        one_ago = end_date

    # 格式化日期为 'YYYY-MM-DD' 形式
    start = one_ago.strftime('%Y-%m-%d')
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
    result = db.execute(sql, values)
    db.close()
    return result


def analyzeMerchantFans(merchant_id, threshold, start_date='2023-01-01', end_date='2024-12-31'):
    # 某商户忠实粉丝各个菜品购买次数
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
    result = db.execute(sql, values)
    db.close()
    return result


def analyzeUserActivity(choice="week"):
    # 用户活跃度分析
    # 获取当前时间
    end_date = datetime.now()

    # 修正
    end_date=end_date + timedelta(weeks=0.2)
    # 格式化时间为 'YYYY-MM-DD' 形式
    end = end_date.strftime('%Y-%m-%d')

    # 减去一
    if choice == "week":
        one_ago = end_date - timedelta(weeks=1)
    else:
        one_ago = end_date - timedelta(weeks=4.3)

    # 格式化日期为 'YYYY-MM-DD' 形式
    start = one_ago.strftime('%Y-%m-%d')


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
    result = db.execute(sql, values)
    db.close()
    return result


def getTheMostPopularDish(merchant_id):
    # 取得商家最受欢迎的菜品
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
    result = db.execute(sql, values)
    db.close()
    return result


if __name__ == '__main__':
    maneger = Manager(1, "刘督")

    user = User("ld", "男", "2130", "6", "学生", 20)

    # user.addFavorites(1,1)
    print(analyzeMerchantDishes(1))
