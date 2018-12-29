from bottle import route, run, template, static_file, get, post, delete, request,response
from sys import argv
import json
import pymysql
import os



connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='store',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

@get('/category/<id>/products')
def get_prod_by_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT prod_ID id,title,desc_prod description,price,img_url,cat_ID category,favorite from products where cat_ID = "+id + " order by 7 desc"
            cursor.execute(sql)
            result = cursor.fetchall()
        if not result:
            response.status = 404
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Category not found', 'CODE': 404})
        for index in range(len(result)):
            for key in result[index]:
                if key == 'price':
                    result[index][key] = float(result[index][key])
        return json.dumps({'STATUS':'SUCCESS','PRODUCTS':result,'CODE':200})
    except:
        response.status = 500
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


@get('/product/<id>')
def get_prod(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT prod_ID id,title,desc_prod description,price,img_url,cat_ID category,favorite from products where prod_ID = "+id
            cursor.execute(sql)
            result = cursor.fetchall()
        for index in range(len(result)):
            for key in result[index]:
                if key == 'price':
                    result[index][key] = float(result[index][key])
        return json.dumps({'STATUS':'SUCCESS','PRODUCT':result,'CODE':200})
    except:
        response.status = 500
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})

@get('/products')
def get_prod_list():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT prod_ID id,title,desc_prod description,price,img_url,cat_ID category,favorite from products"
            cursor.execute(sql)
            result = cursor.fetchall()
        for index in range(len(result)):
            for key in result[index]:
                if key == 'price':
                    result[index][key] = float(result[index][key])
        return json.dumps({'STATUS':'SUCCESS','PRODUCTS':result,'CODE':200})
    except:
        response.status = 500
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


@delete('/product/<id>')
def del_prod(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT title FROM products WHERE prod_ID = " + id
            cursor.execute(sql)
            result = cursor.fetchall()
        if result:
            with connection.cursor() as cursor:
                sql = "DELETE FROM products WHERE prod_ID = " + id
                cursor.execute(sql)
                connection.commit()
            response.status = 201
            return {'STATUS': 'SUCCESS', 'CODE': 201}
        else:
            response.status = 404
            return json.dumps({'STATUS': 'ERROR', 'MSG': 'Product not found', 'CODE': 404})
    except:
        response.status = 500
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


@post('/product')
def add_prod():
    try:
        if not request.forms.get("category") or not request.forms.get("title") or not request.forms.get("desc") or not request.forms.get("price") or not request.forms.get("img_url"):
            return json.dumps({'STATUS': 'ERROR', 'MSG': "Missing parameters", 'CODE': 400})
        id, title, desc, price, img_url, category, favorite = request.forms.get("id"), request.forms.get("title"), request.forms.get("desc"), request.forms.get("price"), request.forms.get("img_url"), request.forms.get("category"), request.forms.get("favorite")
        if not favorite:
            favorite = False
        else:
            favorite = True
        with connection.cursor() as cursor:
            sql = "SELECT cat_id FROM categories WHERE cat_ID = " + category
            cursor.execute(sql)
            category_from_db = cursor.fetchall()
        if not category_from_db:
            return json.dumps({'STATUS': 'ERROR', 'MSG': "Category not found", 'CODE': 404})
        if id:
            with connection.cursor() as cursor:
                sql = "SELECT prod_ID FROM products WHERE prod_ID = " + id
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    with connection.cursor() as cursor:
                        sql = "UPDATE products SET title='"+ title +"',desc_prod='"+ desc +"', price="+ str(price) +",img_url='"+ img_url +"',cat_ID="+ str(category) +",favorite="+ str(favorite) +" WHERE prod_ID = " + id
                        cursor.execute(sql)
                        connection.commit()
                        return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT_ID': id, 'CODE': 201})
                else:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO products () VALUES(" + str(id)+",'"+ title +"','"+ desc +"',"+str(price)+",'"+img_url+"',"+str(category)+","+favorite+")"
                        cursor.execute(sql)
                        connection.commit()
                    with connection.cursor() as cursor:
                        sql = "SELECT MAX(prod_ID) FROM products"
                        cursor.execute(sql)
                        id_from_db = cursor.fetchall()
                    return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT_ID': id_from_db, 'CODE': 201})
        else:
            with connection.cursor() as cursor:
                sql = "INSERT INTO products (title,desc_prod,price,img_url,cat_ID,favorite) VALUES('" + title + "','" + desc + "'," + str(price) + ",'" + img_url + "'," + str(category)+ "," + str(favorite) + ")"
                cursor.execute(sql)
                connection.commit()
                id_from_db = cursor.lastrowid
            return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT_ID': id_from_db, 'CODE': 201})
    except:
        response.status = 500
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


@get('/categories')
def list_of_cats():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT cat_ID as id,cat_name as name from categories"
            cursor.execute(sql)
            result = cursor.fetchall()
        return json.dumps({'STATUS':'SUCCESS','CATEGORIES':result,'CODE':200})
    except:
        response.status = 500
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


@delete('/category/<id>')
def del_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT cat_ID from categories where cat_ID = "+str(id)
            cursor.execute(sql)
            result = cursor.fetchall()
        if result:
            with connection.cursor() as cursor:
                sql = "DELETE FROM categories WHERE cat_ID = "+str(id)
                cursor.execute(sql)
                connection.commit()
            response.status = 201
            return {'STATUS': 'SUCCESS','CODE':201}
        else:
            response.status = 404
            return {'STATUS': 'ERROR', 'MSG': 'Category not found', 'CODE': 404}
    except:
        response.status = 500
        return {'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500}

@post('/category')
def create_cat():
    try:
        if request.params.get("name") == "":
            response.status = 400
            return {'STATUS':'ERROR','MSG':'Name parameter is missing','CODE':400}
        with connection.cursor() as cursor:
            sql = "SELECT cat_ID from categories where cat_name like '"+request.params.get("name")+"'"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                response.status = 200
                return {'STATUS':'ERROR','MSG':'Category already exists','CODE':200}
            else:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO categories (cat_name) VALUES('" + request.params.get('name') +"')"
                    cursor.execute(sql)
                    cat_id = cursor.lastrowid
                response.status = 201
                return {'STATUS': 'SUCCESS','CAT_ID':cat_id,'CODE':201}
    except:
        response.status = 500
        return {'STATUS': 'ERROR', 'MSG': 'Internal error','CODE':500}

@get("/admin")
def admin_portal():
	return template("pages/admin.html")



@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=os.environ.get('PORT', 7000))
#run(host='0.0.0.0', port=argv[1])
