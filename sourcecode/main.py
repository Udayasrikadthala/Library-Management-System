from flask import Flask, render_template, redirect, session, request
import pymysql
import os
import datetime
conn = pymysql.connect(host="localhost", user="root",password="Udayasri@123",db="library")
cursor =conn.cursor()

app = Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
BOOKS_PROFILES_PATH=APP_ROOT + "./static/books"
app.secret_key="library"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username=request.form.get("username")
    password=request.form.get("password")
    count = cursor.execute("select * from admin where username='"+str(username)+"' and password='"+str(password)+"'")
    
    if count > 0:
        admin = cursor.fetchall()
        session['admin_id'] = admin[0][0]
        session['role'] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("message.html", message="Invalid login details")



@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")




@app.route("/student_registration")
def student_registration():
    return render_template("student_registration.html")

@app.route("/student_registration_action", methods=['post'])
def student_registration_action():
    name=request.form.get("name")
    email=request.form.get("email")
    password=request.form.get("password")
    phone=request.form.get("phone")
    address=request.form.get("address")
    gender=request.form.get("gender")
    dob=request.form.get("dob")
    count=cursor.execute("select * from student where email='"+str(email)+"' and password='"+str(phone)+"'")
    if count > 0:
        return render_template("message.html", message="duplicate student details")

    cursor.execute("insert into student(name, email, password, phone, address, gender, dob) values('"+str(name)+"','"+str(email)+"','"+str(password)+"','"+str(phone)+"','"+str(address)+"', '"+str(gender)+"', '"+str(dob)+"')")
    conn.commit()
    return render_template("message.html", message="student registration successfully")



@app.route("/student_login")
def student_login():
    return render_template("student_login.html")


@app.route("/student_login_action" , methods=['post'])
def student_login_action():
    email=request.form.get("email")
    password=request.form.get("password")
    count = cursor.execute("select * from student where email='"+str(email)+"' and password='"+str(password)+"'")
    if count > 0:
        student = cursor.fetchall()
        session['student_id']= student[0][0]
        session['role']='student'
        return redirect("/student_home")
    else:
        return render_template("message.html", message="Invalid Login Details")


@app.route("/student_home")
def student_home():
    return render_template("student_home.html")

@app.route("/librarian_login")
def librarian_login():
    return render_template("librarian_login.html")

@app.route("/librarian_login_action", methods=['post'])
def librarian_login_action():
    email=request.form.get("email")
    password=request.form.get("password")
    count=cursor.execute("select * from librarian where email='"+str(email)+"' and password='"+str(password)+"'")
    if count > 0:
        librarian=cursor.fetchall()
        session['librarian_id'] = librarian[0][0]
        session['role']='librarian'
        return redirect("/librarian_home")
    else:
        return  render_template("message.html", message="Invalid Login Details")


@app.route("/librarian_home")
def librarian_home():
    return render_template("librarian_home.html")

def get_location_by_location_id(location_id):
    cursor.execute("select * from location where location_id='"+str(location_id)+"'")
    locations=cursor.fetchall()
    return locations[0]



@app.route("/locations")
def locations():
    message=request.args.get("message")
    if message == None:
        message = ""
    cursor.execute("select * from location")
    locations=cursor.fetchall()
    return render_template("locations.html", message=message, locations=locations)


@app.route("/location_action", methods=["post"])
def location_action():
    location_name=request.form.get("location_name")
    count=cursor.execute("select * from location where location_name='"+str(location_name)+"'")
    if count >0:
        return redirect("locations?message=duplicate location")
    cursor.execute("insert into location(location_name) value('"+str(location_name)+"')")
    conn.commit()
    return redirect("locations?message=Location Add Successfully")

@app.route("/book_categories")
def book_categories():
    message=request.args.get("message")
    if message == None:
        message=""
    cursor.execute("select * from book_categories")
    book_categories=cursor.fetchall()
    return render_template("book_categories.html", message=message, book_categories=book_categories)

@app.route("/book_categories_action",methods=['post'])
def book_categories_action():
    book_category_name=request.form.get("book_category_name")
    count=cursor.execute("select * from  book_categories where book_category_name='"+str(book_category_name)+"'")
    if count > 0:
        return redirect("book_categories?message=duplicate category")
    cursor.execute("insert into book_categories (book_category_name) value('"+str(book_category_name)+"')")
    conn.commit()
    return redirect("book_categories?message=book category add successfully")

@app.route("/librarians")
def librarians():
    message=request.args.get("message")
    if message==None:
        message = ""
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    cursor.execute(" select * from librarian")
    librarians=cursor.fetchall()
    return render_template("librarians.html", message=message,  librarians=librarians, locations=locations, get_location_by_location_id=get_location_by_location_id)

@app.route("/librarians_action", methods=['post'])
def librarians_action():
    name=request.form.get("name")
    phone=request.form.get("phone")
    email=request.form.get("email")
    password=request.form.get("password")
    address=request.form.get("address")
    location_id=request.form.get("location_id")
    count=cursor.execute("select * from librarian where username='"+str(email)+"' or phone='"+str(phone)+"'")
    if count > 0:
        return redirect("/librarians?message=duplicate librarian details")
    cursor.execute("insert into librarian(name, phone, email, password, address, location_id)values('"+str(name)+"', '"+str(phone)+"', '"+str(email)+"', '"+str(password)+"', '"+str(address)+"', '"+str(location_id)+"')")
    conn.commit()
    return redirect("/librarians?message=librarian add successfully")

@app.route("/add_books")
def add_books():
    message=request.args.get("message")
    if message == None:
        message=" "
    cursor.execute("select * from  book_categories")
    book_categories=cursor.fetchall()
    return render_template("add_books.html", message=message, book_categories=book_categories)

@app.route("/add_books_action", methods=['post'])
def add_books_action():
    book_title=request.form.get("book_title")
    author=request.form.get("author")
    year=request.form.get("year")
    description=request.form.get("description")
    book_category_id = request.form.get("book_category_id")
    picture=request.files.get("picture")
    path = BOOKS_PROFILES_PATH +"/"+picture.filename
    picture.save(path)
    cursor.execute("insert into books(book_title, author, year,description, picture, book_category_id)values('"+str(book_title)+"', '"+str(author)+"', '"+str(year)+"', '"+str(description)+"','"+str(picture.filename)+"', '"+str(book_category_id)+"')")
    conn.commit()
    return redirect("/add_books?message=Book Added Successfully")

@app.route("/view_books")
def view_books():
    keyword=request.args.get("keyword")
    if keyword == None:
        keyword = ""
    query="select * from books where book_title like  '%"+str(keyword)+"%' or author like '%"+str(keyword)+"%' or book_category_id in(select book_category_id from book_categories where book_category_name like '%"+str(keyword)+"%')"
    cursor.execute(query)
    books=cursor.fetchall()
    return render_template("view_books.html", is_borrowed_by_book_id=is_borrowed_by_book_id, books=books, get_book_category_by_book_category_id=get_book_category_by_book_category_id)

def get_book_category_by_book_category_id(book_category_id):
    cursor.execute("select * from book_categories where book_category_id='"+str(book_category_id)+"'")
    book_categories = cursor.fetchall()
    return book_categories[0]


@app.route("/add_book_copies")
def add_book_copies():
    book_id = request.args.get("book_id")
    cursor.execute("select * from books where book_id='"+str(book_id)+"'")
    books = cursor.fetchall()
    count = cursor.execute("select * from book_copies where book_id='"+str(book_id)+"'  ")
    return render_template("add_book_copies.html",count=count, book_id=book_id, book=books[0], str=str)


@app.route("/add_book_copies_action")
def add_book_copies_action():
    book_id=request.args.get("book_id")
    number_of_copies=request.args.get("number_of_copies")
    number_of_copies=int(number_of_copies)
    librarian_id=session['librarian_id']
    for i in range(1, number_of_copies+1):
        book_copy_number=request.args.get("book_copy_number"+str(i))
        cursor.execute("insert into book_copies(book_copy_number, book_id, librarian_id)values('"+str(book_copy_number)+"', '"+str(book_id)+"', '"+str(librarian_id)+"')")
        conn.commit()
    return redirect("/view_books")


@app.route("/view_book_copies")
def view_book_copies():
    book_id=request.args.get("book_id")
    librarian_id=session['librarian_id']
    cursor.execute("select * from  book_copies where book_id='"+str(book_id)+"' and  librarian_id='"+str(librarian_id)+"'")
    book_copies=cursor.fetchall()
    return render_template("view_book_copies.html", book_copies=book_copies)

@app.route("/send_book_request")
def send_book_request():
    book_id=request.args.get("book_id")
    cursor.execute("select librarian_id,count(*) from book_copies where  book_id='"+str(book_id)+"' group by librarian_id ")
    librarian_books=cursor.fetchall()
    books= cursor.execute("select * from books where book_id=('"+str(book_id)+"')")
    return render_template("send_book_request.html",book_id=book_id, librarian_books=librarian_books, get_librarian_by_librarian_id=get_librarian_by_librarian_id,get_available_books_by_book_id=get_available_books_by_book_id,int=int)


@app.route("/send_request_action")
def send_request_action():
    book_id=request.args.get("book_id")
    librarian_id=request.args.get("librarian_id")
    student_id=session['student_id']
    cursor.execute("insert into borrowings(student_id, librarian_id, book_id) values('"+str(student_id)+"', '"+str(librarian_id)+"', '"+str(book_id)+"')")
    conn.commit()
    return redirect("/borrowings")


@app.route("/borrowings")
def borrowings():
    view_type=request.args.get("view_type")
    query=""
    if session['role'] == 'student':
        student_id=session['student_id']
        query="select * from borrowings where student_id='"+str(student_id)+"'"
    elif session['role'] == 'librarian':
        librarian_id=session['librarian_id']
        if view_type == 'requests':
            query="select * from  borrowings where  librarian_id='"+str(librarian_id)+"' and (status='Book Requested' or status='Book Request Accepted') "
        elif view_type == 'borrowings':
            query="select * from  borrowings where  librarian_id='"+str(librarian_id)+"' and (status='Book Assigned' or status='Book Return Requested' or status='Book Renewed')"
        elif view_type == 'history':
            query="select * from  borrowings where  librarian_id='"+str(librarian_id)+"' and (status='Book Request Rejected' or status='Book Request cancelled' or status='Book Returned')"
    cursor.execute(query)
    borrowings=cursor.fetchall()
    print(borrowings)
    return render_template("borrowings.html", borrowings=borrowings, get_fine_by_return_date=get_fine_by_return_date, get_book_copy_by_book_copy_id=get_book_copy_by_book_copy_id, get_student_by_student_id=get_student_by_student_id, get_librarian_by_librarian_id=get_librarian_by_librarian_id, get_book_by_book_id=get_book_by_book_id)


def get_book_by_book_id(book_id):
    cursor.execute("select * from books where book_id='"+str(book_id)+"'")
    books=cursor.fetchall()
    return books[0]


def get_librarian_by_librarian_id(librarian_id):
    cursor.execute("select * from librarian where librarian_id='"+str(librarian_id)+"'")
    librarians=cursor.fetchall()
    return librarians[0]


def get_student_by_student_id(student_id):
    cursor.execute("select * from student where student_id='"+str(student_id)+"'")
    students=cursor.fetchall()
    return students[0]



def get_book_copy_by_book_copy_id(book_copy_id):
    cursor.execute("select * from book_copies where book_copy_id='"+str(book_copy_id)+"'")
    book_copies =cursor.fetchall()
    return book_copies[0]


@app.route("/set_status", methods=['post'])
def set_status():
    borrowing_id=request.form.get("borrowing_id")
    status=request.form.get("status")
    cursor.execute("update borrowings set status='"+str(status)+"' where borrowing_id='"+str(borrowing_id)+"' ")
    conn.commit()
    return redirect("borrowings?view_type=requests")


@app.route("/assign_book", methods=["post"])
def  assign_book():
    borrowing_id=request.form.get("borrowing_id")
    book_id=request.form.get("book_id")
    librarian_id=session['librarian_id']
    cursor.execute("select * from book_copies where   librarian_id='"+str( librarian_id)+"' and  book_id='"+str(book_id)+"' ")
    book_copies=cursor.fetchall()
    return render_template("assign_book.html",  book_copies= book_copies, borrowing_id=borrowing_id)

@app.route("/assign_book_action", methods=["post"])
def assign_book_action():
    borrowing_id=request.form.get("borrowing_id")
    book_copy_id=request.form.get("book_copy_id")
    assigned_date = datetime.datetime.now()
    return_date = assigned_date + datetime.timedelta(days=15)
    assigned_date = assigned_date.strftime("%Y-%m-%d %H:%M")
    return_date = return_date.strftime("%Y-%m-%d %H:%M")
    cursor.execute("update book_copies set status='Assigned' where book_copy_id='"+str(book_copy_id)+"' ")
    cursor.execute("update borrowings set book_copy_id='"+str(book_copy_id)+"', status='Book Assigned', assigned_date='"+str(assigned_date)+"', return_date='"+str(return_date)+"'  where borrowing_id='"+str( borrowing_id)+"'")
    conn.commit()
    return redirect("borrowings?view_type=borrowings")


@app.route("/renewal_book", methods=['post'])
def renewal_book():
    borrowing_id=request.form.get("borrowing_id")
    cursor.execute("select * from  borrowings where  borrowing_id='"+str(borrowing_id)+"'")
    borrowings=cursor.fetchall()
    return_date=borrowings[0][3]
    return_date = return_date + datetime.timedelta(days=15)
    cursor.execute("update  borrowings set  return_date='"+str(return_date)+"', status='Book Renewed' where borrowing_id='"+str(borrowing_id)+"' ")
    conn.commit()
    return redirect("/borrowings")


def get_fine_by_return_date(return_date):
    today = datetime.datetime.now()
    diff = today - return_date
    days_diff = diff.days
    if days_diff > 0:
         fine = 10 * days_diff
    else:
        fine=0
    return fine

@app.route("/return_book", methods=['POST'])
def return_book():
    borrowing_id = request.form.get("borrowing_id")
    status = request.form.get("status")
    cursor.execute("select * from  borrowings where  borrowing_id='" + str(borrowing_id) + "'")
    borrowings = cursor.fetchall()
    return_date = borrowings[0][3]
    today = datetime.datetime.now()
    diff = today - return_date
    days_diff = diff.days
    if days_diff > 0:
         fine = 10 * days_diff
         return render_template("return_book.html", fine=fine, borrowing_id=borrowing_id, status=status)
    else:
         fine=0
         cursor.execute("update book_copies set status='Available' where book_copy_id in (select book_copy_id from borrowings where  borrowing_id='" + str(borrowing_id) + "') ")
         conn.commit()
         cursor.execute("update borrowings set status='" + str(status) + "' where borrowing_id='" + str(borrowing_id) + "' ")
         conn.commit()
    return redirect("borrowings?view_type=requests")



@app.route("/return_book_action", methods=['post'])
def return_book_action():
    borrowing_id = request.form.get("borrowing_id")
    status = request.form.get("status")
    fine = request.form.get("fine")
    cursor.execute("update book_copies set status='Available' where book_copy_id in (select book_copy_id from borrowings where borrowing_id='"+str(borrowing_id)+"') ;")
    conn.commit()
    cursor.execute("update borrowings set status='" + str(status) + "', fine='"+str(fine)+"' where borrowing_id='" + str(borrowing_id) + "' ")
    conn.commit()
    return redirect("borrowings?view_type=history")

def is_borrowed_by_book_id(book_id):
    student_id = session['student_id']
    count=cursor.execute("select * from borrowings where  student_id='"+str(student_id)+"' and  book_id='"+str(book_id)+"' and (status='Book Requested' or status='Book Request Accepted' or status='Book Assigned' or status='Book Renewed' or status='Book Return Requested')")
    if count >0:
        return True
    else:
        return False


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


def get_available_books_by_book_id(book_id,librarian_id):
    print(book_id)
    print(librarian_id)
    count= cursor.execute("select * from book_copies where book_id ='"+str(book_id)+"' and librarian_id ='"+str(librarian_id)+"' and (status='Assigned') ")
    print(count)
    return count


app.run(debug=True)


























