from 数据库连接 import DB
from 管理员 import Manager
from 用户 import User
from 商户 import Merchant

db=DB()


def count_meals_by_merchant_and_age_group():
    """
    按年龄段统计各商户的用餐次数
    """
    sql = ("""
                SELECT 
                  CASE
                    WHEN age < 18 THEN 'Under 18'
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 45 THEN '36-45'
                    ELSE '46 and above'
                  END AS age_group,
                  merchants.name AS merchant_name,
                  COUNT(orders.id) AS order_count
                FROM 
                  users
                JOIN 
                  orders ON users.id = orders.user_id
                JOIN 
                  merchants ON orders.merchant_id = merchants.id
                GROUP BY 
                  age_group, merchant_name
                ORDER BY 
                  age_group, order_count DESC;
                """)
    result = db.execute(sql)
    db.close()
    return result

def count_dish_purchases_by_role():
    """
    按角色统计某一菜品的购买数量
    """
    sql = ("""
                SELECT 
                  users.role,
                  dishes.name AS dish_name,
                  COUNT(orders.id) AS purchase_count
                FROM 
                  users
                JOIN 
                  orders ON users.id = orders.user_id
                JOIN 
                  dishes ON orders.dish_id = dishes.id
                GROUP BY 
                  users.role, dishes.name
                ORDER BY 
                  users.role, purchase_count DESC;
                """)
    result = db.execute(sql)
    db.close()
    return result

def count_meals_by_merchant_and_gender():
    """
    按性别统计各商户的用餐次数
    """
    sql = ("""
                SELECT 
                  users.gender,
                  merchants.name AS merchant_name,
                  COUNT(orders.id) AS order_count
                FROM 
                  users
                JOIN 
                  orders ON users.id = orders.user_id
                JOIN 
                  merchants ON orders.merchant_id = merchants.id
                GROUP BY 
                  users.gender, merchant_name
                ORDER BY 
                  users.gender, order_count DESC;
                """)
    result = db.execute(sql)
    db.close()
    return result

def count_and_average_comments_by_age_group():
    """
    按年龄段统计评价数量和平均评分
    """
    sql = ("""
                SELECT 
                  CASE
                    WHEN age < 18 THEN 'Under 18'
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 45 THEN '36-45'
                    ELSE '46 and above'
                  END AS age_group,
                  COUNT(comments.id) AS comment_count,
                  AVG(comments.score) AS average_score
                FROM 
                  users
                JOIN 
                  comments ON users.id = comments.user_id
                GROUP BY 
                  age_group
                ORDER BY 
                  age_group;
                """)
    result = db.execute(sql)
    db.close()
    return result

def count_and_average_comments_by_role():
    """
    按角色统计评价数量和平均评分
    """
    sql = ("""
                SELECT 
                  users.role,
                  COUNT(comments.id) AS comment_count,
                  AVG(comments.score) AS average_score
                FROM 
                  users
                JOIN 
                  comments ON users.id = comments.user_id
                GROUP BY 
                  users.role
                ORDER BY 
                  users.role;
                """)
    result = db.execute(sql)
    db.close()
    return result

def count_and_average_comments_by_gender():
    """
    按性别统计评价数量和平均评分
    """
    sql = ("""
                SELECT 
                  users.gender,
                  COUNT(comments.id) AS comment_count,
                  AVG(comments.score) AS average_score
                FROM 
                  users
                JOIN 
                  comments ON users.id = comments.user_id
                GROUP BY 
                  users.gender
                ORDER BY 
                  users.gender;
                """)
    result = db.execute(sql)
    db.close()
    return result