from flask import Blueprint, request, render_template, session, redirect
from App.models import *
admin = Blueprint('admin', __name__)
# @admin.route('/hello/', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         list1 = User.query.filter(User.u_name == username, User.password == password).first()
#         print(list1)
#
#         if list1:
#             session['username'] = username
#             return render_template('index.html')
#         else:
#             return render_template('login.html')
#
#     return render_template('login.html')

# 头部
@admin.route('/head/', methods=['GET'])
def head():
    if request.method == 'GET':  # 如果请求的方式为get请求
        user = session.get('username')  # 在session存储中得到登录人的名字
        return render_template('head.html', user=user)  # 返回到头部页面并将登录人信息传递过去

# 左边
@admin.route('/left/', methods=['GET'])
def left():
    if request.method == 'GET':  # 如果请求的方式为get请求
        user = session.get('username')  # 在session存储中得到登录人的名字
        permissions = User.query.filter_by(u_name=user).first().role.permission  # 通过用户名在用户表中查询相应的角色所对应的权限
        return render_template('left.html', user=user, permissions=permissions)  # 返回到左边页面,并将用户名和权限信息传递过去

# 欢迎界面
@admin.route('/welcome/', methods=['GET'])
def welcome():
    if request.method == 'GET':  # 如果请求的方式为get请求
        return render_template('welcome.html')  # 返回到欢迎界面

# 登录界面
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':              # 请求方式是GET
        return render_template('login.html')  # 返回到login(登录)页面
    if request.method == 'POST':               # 请求方式是POST
        username = request.form.get('username')  # 从表单得到用户输入的用户名
        password = request.form.get('password')   # 从表单得到用户输入的密码
        if not all([username, password]):        # 如果用户名和密码都为空或者有一项为空
            msg = '*请填写好完整的信息'           # 定义msg信息
            return render_template('login.html', msg=msg)  # 返回到登录页面并显示该提示信息
        user = User.query.filter(User.u_name == username, User.password == password).first()  # 通过用户输入的信息进行查询
        if user:     # 如果有该用户
            session['user_id'] = user.u_id    # 通过session将用户id存储起来
            session['username'] = user.u_name    # 通过session将用户名存储起来
            return render_template('index.html')   # 返回到登录成功之后的首页
        else:                   # 没有该用户,意味着密码和用户名输入至少有一项有误
            msg = '*用户名或者密码不正确'    # 定义msg信息
            return render_template('login.html', msg=msg)  # 返回到登录页面,并将msg信息传递过去显示


# 班级列表
@admin.route('/grade/', methods=['GET', 'POST'])
def grad():
    # grades = Grade.query.all()
    page = int(request.args.get('page', 1))  # 通过get请求的取值从班级页面得到页面数,如果没有则默认为1
    per_page = 5    # 设置每页数量
    paginate = Grade.query.paginate(page, per_page, error_out=False)    # 当前页数,每页数量,是否打印错误
    grades = paginate.items      # 当前页面所有信息
    return render_template('grade.html', grades=grades, paginate=paginate)   # 返回到班级页面


# 修改班级信息
@admin.route('/edit_grade/', methods=['GET', 'POST'])
def edit_grades():
    if request.method == 'GET':          # 如果是GET请求
        g_id = request.args.get('g_id')   # 通过GET请求传值的方法,得到班级id
        # print(g_id)      测试语句,看可不可以得到班级id
        return render_template('edit_grades.html', g_id=g_id)  # 返回到编辑页面,并将班级id传过去
    else:           # 如果是POST请求
        g_id = request.form.get('g_id')     # 得到班级id
        g_name = request.form.get('g_name')   # 得到班级名称
        # print(g_name)   测试代码:是否有班级
        list1 = Grade.query.all()   # 查询所有班级
        list2 = []    # 定义一个空列表
        for i in list1:       # 循环遍历班级所有信息
            list2.append(i.g_name)   # 将班级名称添加到list2列表中
        # print(list2)   测试代码输出list2列表信息
        if g_name in list2:    # 如果通过POSTS请求得到的班级名称在该列表中
            msg = '输入的班级名不能和以前的班级名或其他班级名一样'   # 定义msg信息
            return render_template('edit_grades.html', msg=msg, g_id=g_id)  # 返回到编辑页面,并将msg和班级id传过去
        if g_name == '':      # 如果得到的班级名称为空
            msg = '不能输入空班级'  # 定义msg信息
            return render_template('edit_grades.html', msg=msg, g_id=g_id)   # 返回到编辑页面,并将msg和班级id传过去
        else:    # 如果既不为空也不重复
            new_gards = Grade.query.filter(Grade.g_id == g_id).first()   # 通过该班级id在班级表中查询出该条信息
            new_gards.g_name = g_name     # 将该班级名称进行修改
            db.session.commit()      # 进行提交
            msg = '编辑成功,可到班级列表查看'  # 定义msg信息
            return render_template('edit_grades.html', msg=msg, g_id=g_id)   # 返回到编辑页面,返回msg和班级id

# 删除班级
@admin.route('/delete_grade/', methods=['GET', 'POST'])
def delete_grades():
    g_id = request.args.get('g_id')   # 通过get方式得到班级id
    Student.query.filter(Student.grade_id == g_id).delete()  # 先找到在该班级的学生进行删除
    # db.session.delete(list1)
    db.session.commit()    # 进行提交
    Grade.query.filter(Grade.g_id == g_id).delete()  # 通过班级id将该班级删除
    db.session.commit()    # 进行提交
    msg = '删除成功'     # 定义msg
    page = int(request.args.get('page', 1))    # 通过get方式得到当前页,如果没有设置为1
    per_page = 5  # 设置每页数量
    paginate = Grade.query.paginate(page, per_page, error_out=False)  # 当前页数,每页数量,是否打印错误
    grades = paginate.items   # 当前页面所有信息
    return render_template('grade.html', msg=msg, grades=grades, paginate=paginate)  # 返回到班级页面

# 删除班级里面的学生
@admin.route('/delete_grade_student/', methods=['GET', 'POST'])
def delete_grade_student():
    g_id = request.args.get('g_id')  # 通过get请求获得传递过来的班级id
    print(g_id)
    s_id = request.args.get('s_id')
    Student.query.filter(Student.s_id == s_id).delete()
    db.session.commit()
    page = int(request.args.get('page', 1))  # 获得通过get请求传递过来的页数,如果第一次进入该页面设置为第一页.
    per_page = 5  # 设置一页展示几条数据
    paginate = Student.query.filter(Student.grade_id == g_id).paginate(page, per_page, error_out=False)  # 通过该学生所在班级id和传递过来的id进行匹配,获得相应数据
    # paginate = students.
    stus = paginate.items  # 当前页面所有信息
    # return render_template('gradestudent.html')
    return render_template('gradestudent.html', stus=stus, paginate=paginate, g_id=g_id)


# @admin.route('/session/', methods=['GET', 'POST'])
# def session():
#     g_id = int(request.args.get('g_id'))
#     session['g_id'] = g_id
#     return redirect('/user/grade_student')


# 学生列表
@admin.route('/student/', methods=['GET', 'POST'])
def students():
    page = int(request.args.get('page', 1))  # 通过get得到当前页数
    per_page = 5   # 设置每页数量
    paginate = Student.query.paginate(page, per_page, error_out=False)  # 当前页数,每页数量,是否打印错误
    stus = paginate.items     # 当前页面所有信息
    # ******************以下代码用于测试**************************
    a = paginate.iter_pages()   # 当前所有页面列表
    print(a)
    for i in a:
        print(i)
    # ******************测试结束**************************
    return render_template('student.html', stus=stus, paginate=paginate)  # 返回到学生页面,并传递过去后面两个信息


# 班级学生
@admin.route('/grade_student/', methods=['GET', 'POST'])
def grade_students():
    g_id = request.args.get('g_id')  # 通过get请求获得传递过来的班级id
    # g_id = session.get('g_id')
    print(g_id)
    page = int(request.args.get('page', 1))  # 获得通过get请求传递过来的页数,如果第一次进入该页面设置为第一页.
    per_page = 5  # 设置一页展示几条数据
    paginate = Student.query.filter(Student.grade_id == g_id).paginate(page, per_page, error_out=False) # 通过该学生所在班级id和传递过来的id进行匹配,获得相应数据
    # paginate = students.
    stus = paginate.items  # 当前页面所有信息
    return render_template('gradestudent.html', stus=stus, paginate=paginate, g_id=g_id)  # 返回到该班级下的学生页面,并传递过去后面两个信息
#     g_id = int(request.args.get('g_id'))
#     print(g_id)
#
    #     print(stus)
#     # stus = Student.query.filter(Student.s_id == 1).all()
#     # print(stus)
#     # for i in stus:
#     #     print(i.grade.g_name)
#     # for i in stus:
#     #     print(i.s_name)
#     page = int(request.args.get('page', 1))
#     per_page = 2
#     paginate = Student.query.paginate(page, per_page, error_out=False)
#     stus = paginate.items
#     # print(stus)
#
#     return render_template('student.html', stus=stus, paginate=paginate)  #paginate=paginate)
# 退出
@admin.route('/logout/', methods=['GET', 'POST'])
def logouts():
    return redirect('/user/login/')  # 通过重定向退出到登录页面


# 班级添加
@admin.route('/addgrade/', methods=['GET', 'POST'])
def addgrades():
    g_name = request.form.get('g_name')  # 通过表单提交获取到班级名称
    list1 = Grade.query.filter(Grade.g_name == g_name).first()  # 通过传递过来的班级名进行查询,获取信息
    if request.method == 'POST':  # 如果该请求是post请求
        if g_name != '':  # 如果该班级名称不为空,
            if list1:  # 如果查询出来了该结果
                msg = '该班级已经存在'  # 提示信息为该班级已存在
                return render_template('addgrade.html', msg=msg)  # 返回到班级添加页面
            else:  # 如果没有查询出该结果,证明传递过来的班级名还没有创建
                new_grade = Grade(g_name=g_name, g_create_time=datetime.now())  # 则创建一条新班级记录
                db.session.add(new_grade)  # 将该条记录添加到班级表中
                db.session.commit()  # 进行提交操作
                msg = '添加成功,请前往班级列表查看'  # 提示信息为添加成功,请前往班级列表查看
                return render_template('addgrade.html', msg=msg)  # 返回到添加班级页面,并传递提示信息过去
        else:  # 如果输入的班级名为空
            msg = '未输入班级,请重新输入'  # 则提示信息为未输入班级,请重新输入
            return render_template('addgrade.html', msg=msg)  # 返回到添加班级页面,并传递提示信息过去
    return render_template('addgrade.html')  # 如果是get请求,则直接展示添加班级页面

# 添加学生
@admin.route('/addstu/', methods=['POST', 'GET'])
def addstus():
    grades = Grade.query.all()  # 查询所有班级记录
    s_name = request.form.get('s_name')  # 获得通过form表单提交过来的学生姓名
    s_sex = request.form.get('s_sex')  # 获得通过form表单提交过来的学生性别
    g_name = request.form.get('g_name')  # 获得通过form表单提交过来的班级名称
    list1 = Student.query.filter(Student.s_name == s_name).first()  # 通过传递过来的学生姓名查询原有班级表中是否有该学生记录
    if request.method == 'POST':  # 如果是post请求
        if s_name != '':  # 如果学生姓名不为空
            if list1:  # 如果表中有此学生的记录
                msg = '该学生已经存在'  # 则提示信息为该学生已经存在
                return render_template('addstu.html', msg=msg, grades=grades)  # 返回到添加学生页面,并将提示信息和班级记录传递过去,因为该添加学生页面的班级选择需要该信息
            else:  # 如果表中没有此学生信息
                new_student = Student(s_name=s_name, s_sex=s_sex, grade_id=g_name)  # 创建新学生对象
                db.session.add(new_student)  # 将新学生对象添加到学生表中
                db.session.commit()  # 进行提交操作
                msg = '添加成功,请前往学生列表查看'  # 提示信息为添加成功,请前往学生列表查看
                return render_template('addstu.html', msg=msg, grades=grades)  # 返回到添加学生页面.并将并将提示信息和班级记录传递过去
        else:  # 如果传递过来的学生姓名为空
            msg = '未输入学生,请重新输入'  # 则提示未输入学生,请重新输入
            return render_template('addstu.html', msg=msg, grades=grades)  # 返回到添加学生页面,并将提示信息和班级记录传递过去
    return render_template('addstu.html', grades=grades)  # 如果是get请求,返回到添加学生页面,并将班级记录传递过去


# 角色列表
@admin.route('/roles/', methods=['POST', 'GET'])
def roless():
    roles = Role.query.all()  # 从角色表中查询出所有角色记录
    return render_template('roles.html', roles=roles)  # 返回到展示角色的页面并将所有查询结果返回

# 角色列表里面的查看权限
@admin.route('/userperlist/', methods=['POST', 'GET'])
def userperlists():
    r_id = request.args.get('r_id')  # 通过get请求获得角色id
    pers = Role.query.filter(Role.r_id == r_id).first().permission  # 通过角色id查询角色对应的权限
    if len(pers) == 0:  # 如果查询出来的长度为0
        msg = '该角色没有权限'  # 提示信息为该角色没有权限
        return render_template('user_per_list.html', pers=pers, r_id=r_id, msg=msg)
    return render_template('user_per_list.html', pers=pers, r_id=r_id)  # 返回到角色列表的权限页面将权限和角色id传递过去


# 角色列表里面的查看权限时删除权限
@admin.route('/deleteuserperlist/', methods=['POST', 'GET'])
def deleteuserperlist():
    r_id = request.args.get('r_id')  # 通过get请求获得角色id
    p_id = request.args.get('p_id')  # 通过get请求获得权限id
    # permissions = Role.query.filter(Role.r_id == r_id).first().permission
    permission1 = Permission.query.get(p_id)  # 从permission权限表中得到该条id对应的数据
    role = Role.query.get(r_id)  # 从role角色表中得到该条id对应的数据
    permission1.roles.remove(role)  # 进行中间表的数据删除
    # db.session.remove(permission1)
    # db.session.delete()
    db.session.commit()  # 进行提交保存
    pers = Role.query.filter(Role.r_id == r_id).first().permission  # 通过角色id查询角色对应的权限
    if len(pers) == 0:  # 如果查询出来的长度为0
        msg = '该角色没有权限'  # 提示信息为该角色没有权限
        return render_template('user_per_list.html', pers=pers, r_id=r_id, msg=msg)  # 返回到角色列表的权限页面将权限和角色id和提示信息传递过去
    return render_template('user_per_list.html', pers=pers, r_id=r_id)  # 返回到角色列表的权限页面将权限和角色id传递过去


# 角色列表里面的添加权限
@admin.route('/adduserper/', methods=['POST', 'GET'])
def adduserpers():
    permissions = Permission.query.all()  # 查询所有权限数据
    if request.method == 'GET':  # 如果请求方式为get请求
        r_id = request.args.get('r_id')  # 通过get请求获得该角色id
        # r_id = r_id
        print(r_id)
        return render_template('add_user_per.html', permissions=permissions, r_id=r_id)  # 返回到添加角色权限页面并将所有权限数据和角色id传递过去
    else:  # 如果是post请求
        r_id = request.form.get('r_id')  # 从add_user_per.html中获得对应的角色id
        p_id = int(request.form.get('p_id'))  # 从add_user_per.html中获得对应的权限id
        # r_id = request.form.get('r_id')
        print(r_id)
        list1 = Role.query.filter(Role.r_id == r_id).first().permission  # 从角色表中通过角色id查询出对应的权限
        print(list1)
        list2 = []  # 定义一个空列表来存储权限id
        for i in list1:  # 循环遍历查询出来的权限
            list2.append(i.p_id)  # 将权限id添加到list2列表中
            # print(i.p_id)
        # print(list2)
        if p_id in list2:  # 如果该权限id在该列表中,
            msg = '该用户已有该权限'  # 提示信息为该用户已有该权限
            return render_template('add_user_per.html', permissions=permissions, msg=msg, r_id=r_id)  # 返回到添加角色权限页面并将权限和提示信息角色id传递过去
        else:  # 如果不在该列表中
            # new_r_p = r_p(role_id=r_id, permission_id=p_id)
            # db.session.add(new_r_p)
            # db.session.commit()
            # msg = '已成功添加权限,可到该角色下查看权限'
            # list1 = r_p.query.all()
            # print(list1)
            # new_p = r_p(role_id=r_id, permission=p_id)
            # db.session.add(new_p)
            # db.session.commit()
            role = Role.query.get(r_id)  # 查询出该角色id对应的数据
            permission1 = Permission.query.get(p_id)  # 查询出该权限id对应的数据
            permission1.roles.append(role)  # 在对应数据添加在一起
            db.session.add(permission1)  # 将对应数据添加到中间表中
            db.session.commit()  # 进行提交保存
            permissions = Permission.query.all()  # 查询所有权限数据
            return render_template('add_user_per.html', permissions=permissions, r_id=r_id)   # 返回到添加角色权限页面,将权限数据和角色id传递过去


# 角色列表里面的减少权限
@admin.route('/subuserper/', methods=['POST', 'GET'])
def subuserper():
    if request.method == 'GET':  # 如果请求方式是get请求
        r_id = request.args.get('r_id')  # 通过get请求方式获得角色id
        permissions = Role.query.filter(Role.r_id == r_id).first().permission  # 通过角色id获得相应权限数据
        return render_template('sub_user_per.html', r_id=r_id, permissions=permissions)  # 返回到减少角色权限的页面,并将角色id和权限数据传递过去
    else:  # 如果是post请求
        r_id = request.form.get('r_id')  # 通过表单提交得到角色id
        p_id = request.form.get('p_id')  # 通过表单提交得到权限id
        # permissions = Role.query.filter(Role.r_id == r_id).first().permission
        if p_id:  # 如果有权限id
            permission1 = Permission.query.get(p_id)  # 通过权限id得到该对应数据
            role = Role.query.get(r_id)  # 通过角色id到底对应数据
            permission1.roles.remove(role)  # 进行中间表的数据删除
            # db.session.remove(permission1)
            # db.session.delete()
            db.session.commit()  # 进行提交保存
            permissions = Role.query.filter(Role.r_id == r_id).first().permission  # 查询出该角色id对应的权限数据
            return render_template('sub_user_per.html', permissions=permissions, r_id=r_id)  # 返回到减少角色权限列表并将权限数据和角色id传递过去
        else:  # 如果没有权限id
            msg = '该角色已没有任何权限'  # 提示信息为该角色已没有任何权限
            return render_template('sub_user_per.html', r_id=r_id, msg=msg)  # 返回到减少角色权限页面并将角色id和提示信息传递过去



# 添加角色
@admin.route('/addroles/', methods=['POST', 'GET'])
def addroless():
    if request.method == 'GET':  # 如果请求方式是get请求
        return render_template('addroles.html')  # 返回到添加角色页面
    else:  # 如果是post请求
        r_name = request.form.get('r_name')  # 通过表单提交得到角色名称
        list1 = Role.query.filter(Role.r_name == r_name).first()  # 通过角色名称得到对应数据
        if list1:  # 如果可以查询到
            msg = '已有该角色,请重新添加'  # 提示信息为已有该角色,请重新添加
            return render_template('addroles.html', msg=msg)  # 返回到添加角色页面,并将提示信息传递过去
        else:  # 如果不能查询到
            if r_name == '':  # 如果角色名称为空
                msg = '添加为无效角色'  # 提示信息为添加无效信息
                return render_template('addroles.html', msg=msg)  # 返回到添加角色页面并将提示信息传递过去
            else:  # 如果不为空
                new_role = Role(r_name=r_name)  # 创建新角色
                db.session.add(new_role)  # 将新创建的角色添加到角色表中
                db.session.commit()  # 进行提交保存
                msg = '添加成功'  # 提示信息为添加成功
                return render_template('addroles.html', msg=msg)  # 返回到添加角色页面并将提示信息传递过去

# 添加权限
@admin.route('/addpermission/', methods=['POST', 'GET'])
def addpermission():
    if request.method == 'GET':  # 如果请求方式为get请求
        pers = Permission.query.all()  # 查询所有权限信息
        return render_template('addpermission.html', pers=pers)  # 返回到添加权限页面,并将权限信息传递过去
    else:  # 如果是post请求
        p_name = request.form.get('p_name')  # 通过form表单提交得到权限名称
        p_er = request.form.get('p_er')  # 通过form表单提交得到权限简写
        if p_name == '' and p_er == '':  # 如果权限名称和权限简写都为空
            msg = '权限名称不能为空'  # 提示信息为权限名称不能空
            msg1 = '权限简写不能为空'  # 提示信息为权限简写不能空
            pers = Permission.query.all()  # 查询所有权限数据
            return render_template('addpermission.html', msg=msg, pers=pers, msg1=msg1)  # 返回到添加权限页面并将提示信息和权限数据传递过去
        elif p_name == '':  # 如果权限名称为空
            msg = '权限名称不能为空'  # 提示信息为权限名称不能空
            pers = Permission.query.all()   # 查询所有权限数据
            return render_template('addpermission.html', msg=msg, pers=pers)  # 返回到添加权限页面并将提示信息和权限数据传递过去
        elif p_er == '':   # 如果权限简写为空
            msg1 = '权限简写不能为空'  # 提示信息为权限简写不能空
            pers = Permission.query.all()  # 查询所有权限数据
            return render_template('addpermission.html', msg1=msg1, pers=pers)  # 返回到添加权限页面并将提示信息和权限数据传递过去
        else:  # 如果都不为空
            list3 = Permission.query.filter(Permission.p_name == p_name, Permission.p_er == p_er).first()  # 通过权限名称和权限简写进行查询得到数据
            if list3:  # 如果有该数据
                msg = '该权限名称已存在'  # 提示信息为该权限名称已存在
                msg1 = '该权限简写已存在'  # 提示信息为该权限简写已存在
                pers = Permission.query.all()  # 查询所有权限数据
                return render_template('addpermission.html', msg=msg, msg1=msg1, pers=pers)  # 返回到添加权限页面并将提示信息和权限数据传递过去
            else:  # 如果没有该数据
                list1 = Permission.query.filter(Permission.p_name == p_name).first()  # 通过权限名称进行查询得到数据
                list2 = Permission.query.filter(Permission.p_er == p_er).first()  # 通过权限简写进行查询得到数据
                if list1 or list2:  # 如果两条查询结果中有一个为真
                    if list1:  # 如果通过权限名称进行查询得到数据为真
                        msg = '该权限名称已存在'  # 提示信息为该权限名称已存在
                        pers = Permission.query.all()  # 查询所有权限数据
                        return render_template('addpermission.html', msg=msg, pers=pers)  # 返回到添加权限页面并将提示信息和权限数据传递过去
                    if list2:  # 如果通过权限简写进行查询得到的数据为真
                        msg1 = '该权限简写已存在'  # 提示信息为该权限简写已存在
                        pers = Permission.query.all()  # 查询所有权限数据
                        return render_template('addpermission.html', msg1=msg1, pers=pers)  # 返回到添加权限页面并将提示信息和权限数据传递过去
                else:
                    new_permission = Permission(p_name=p_name, p_er=p_er)  # 创建新权限数据
                    db.session.add(new_permission)  # 将创建的权限数据添加到权限表中
                    db.session.commit()  # 进行提交保存
                    msg = '添加权限成功'  # 提示信息为添加权限成功
                    pers = Permission.query.all()  # 查询所有权限数据
                    return render_template('addpermission.html', msg=msg, pers=pers)  # 返回到添加权限页面并将提示信息和权限数据传递过去


# 权限列表
@admin.route('/permissions/')
def permissions():
    page = int(request.args.get('page', 1))  # 通过get请求得到页数,如果是第一次则规定为1
    per_page = 5  # 规定每页数据为5条
    paginate = Permission.query.paginate(page, per_page, error_out=False)  # 当前页数,每页数量,是否打印错误
    # permissions = Permission.query.all()
    permissions = paginate.items  # 得到所有数据
    return render_template('permissions.html', permissions=permissions, paginate=paginate)  # 返回到权限页面所有数据和页面数据

# 编辑权限
@admin.route('/eidtorpermission/', methods=['POST', 'GET'])
def eidtorpermission():
    if request.method == 'GET':  # 如果请求方式为get请求
        p_id = request.args.get('p_id')  # 通过get请求得到权限id
        return render_template('edit_permission.html', p_id=p_id)  # 返回到编辑权限页面并将权限id传递过去
    else:  # 如果为post请求
        p_id = request.form.get('p_id')  # 通过form表单提交得到权限id
        p_name = request.form.get('p_name')  # 得到权限名称
        # print(p_name)   测试代码:是否有权限
        list1 = Permission.query.all()  # 查询所有权限
        list2 = []  # 定义一个空列表
        for i in list1:  # 循环遍历权限所有信息
            list2.append(i.p_name)  # 将权限名称添加到list2列表中
        # print(list2)   测试代码输出list2列表信息
        if p_name in list2:  # 如果通过POSTS请求得到的权限名称在该列表中
            msg = '输入的权限名不能和以前的权限名或其他权限名一样'  # 定义msg信息
            return render_template('edit_permission.html', msg=msg, p_id=p_id)  # 返回到编辑页面,并将msg和权限id传过去
        if p_name == '':  # 如果得到的权限名称为空
            msg = '不能输入空权限名称'  # 定义msg信息
            return render_template('edit_permission.html', msg=msg, p_id=p_id)  # 返回到编辑页面,并将msg和权限id传过去
        else:  # 如果既不为空也不重复
            new_permissions = Permission.query.filter(Permission.p_id == p_id).first()  # 通过该权限id在权限表中查询出该条信息
            new_permissions.p_name = p_name  # 将该权限名称进行修改
            db.session.commit()  # 进行提交
            msg = '编辑成功,可到权限列表查看'  # 定义msg信息
            return render_template('edit_grades.html', msg=msg, p_id=p_id)  # 返回到编辑页面,返回msg和权限id


# 删除权限
@admin.route('/deletepermission/', methods=['POST', 'GET'])
def deletepermissions():
    p_id = request.args.get('p_id')  # 通过get请求得到权限id
    print(p_id)
    permissions1 = Permission.query.get(p_id)  # 通过权限id查询得到该条数据
    role = Role.query.all()  # 查询所有角色信息
    for i in role:  # 遍历角色信息
        if permissions1 in i.permission:  # 如果该条数据在该角色权限中
            print(i.permission)
            permissions1.roles.remove(i)  # 移除中间表的数据
    Permission.query.filter(Permission.p_id == p_id).delete()  # 删除权限表中该权限id对应的数据
    db.session.commit()  # 提交保存数据
    page = request.args.get('page', 1)  # 通过get请求得到页数,如果是第一次则规定为1
    pre_page = 5  # 每页显示2条数据
    paginate = Permission.query.paginate(page, pre_page, error_out=False)  # 当前页数,每页显示条数,是否显示错误
    permissions = paginate.items  # 所有数据
    msg = '删除成功'  # 提示信息为删除成功
    return render_template('permissions.html', permissions=permissions, paginate=paginate, msg=msg)  # 返回到权限页面并将权限信息,页面信息提示信息传递过去


# 修改密码
@admin.route('/changepwd/', methods=['POST', 'GET'])
def changepwds():
    user_id = session.get('user_id')  # 将保存在session中的用户id取出来
    user = User.query.filter(User.u_id == user_id).first()  # 通过用户id在用户表中查询信息
    if request.method == 'GET':  # 如果请求方式为get请求
        return render_template('changepwd.html', user=user)  # 返回到改变密码页面并将查询信息传递过去
    else:  # 如果是post请求
        pwd1 = request.form.get('pwd1')  # 通过form表单提交得到密码
        pwd2 = request.form.get('pwd2')  # 通过form表单提交得到密码
        pwd3 = request.form.get('pwd3')  # 通过form表单提交得到密码
        pwd = User.query.filter(User.u_id == user_id).first().password  # 通过用户id在用户表中得到密码
        print(pwd)
        print(pwd1)
        print(pwd2)
        print(pwd3)
        if pwd != pwd1:  # 如果该用户对应的密码和输入密码不相等
            msg = '输入的旧密码不正确'  # 提示信息为输入的旧密码不正确
            return render_template('changepwd.html', user=user, msg=msg)  # 返回到改变密码页面并将用户信息和提示信息传递过去
        else:
            if pwd2 != pwd3:  # 如果后两次输入的密码不一致
                msg = '两次新密码输入不一致'  # 提示信息为两次新密码输入不一致
                return render_template('changepwd.html', user=user, msg=msg)  # 返回到改变密码页面并将用户信息和提示信息传递过去
            else:
                user = User.query.filter(User.u_id == user_id).first()  # 通过用户id在用户表中查询数据
                user.password = pwd2  # 设置新密码为pwd2表单中输入的密码
                db.session.commit()  # 进行提交保存
                user = User.query.filter(User.u_id == user_id).first()  # 通过用户id在用户表中查询数据
                msg = '修改成功'  # 提示信息为修改成功
                return render_template('changepwd.html', user=user, msg=msg)  # 返回到改变密码页面并将用户信息和提示信息传递过去


# 用户列表
@admin.route('/userlist/', methods=['GET'])
def userlists():
    page = int(request.args.get('page', 1))  # 通过get请求得到页数,如果是第一次则规定为1
    per_page = 5  # 每页显示5条数据
    paginate = User.query.paginate(page, per_page, error_out=False)  # 当前页数,每页显示条数,是否显示错误
    users = paginate.items  # 所有数据
    return render_template('users.html', users=users, paginate=paginate)  # 返回到用户页面并将用户信息和页面信息传递过去

# 分配角色
@admin.route('/assignrole/', methods=['POST', 'GET'])
def assignroles():
    if request.method == 'GET':  # 如果请求方式是get请求
        u_id = request.args.get('u_id')  # 通过get请求得到用户id
        roles = Role.query.all()  # 查询所有角色信息
        return render_template('assign_user_role.html', roles=roles, u_id=u_id)  # 返回分配角色页面,并将角色信息和用户id传递过去
    else:  # 如果是post请求
        u_id = request.form.get('u_id')  # 通过form表单提交得到用户id
        r_id = request.form.get('r_id')  # 通过form表单提交得到角色id
        use = User.query.filter(User.u_id == u_id).first()  # 通过用户id在用户表中查询信息
        use.role_id = r_id  # 将用户的角色id设置为表单提交的角色id
        db.session.commit()  # 进行提交保存
        msg = '角色分配成功'  # 提示信息为角色分配成功
        roles = Role.query.all()  # 查询所有角色信息
        return render_template('assign_user_role.html', msg=msg, roles=roles)  # 返回到分配角色页面并将提示信息和角色信息传递过去


# 添加用户
@admin.route('/adduser/', methods=['POST', 'GET'])
def addusers():
    if request.method == 'GET':  # 如果是get请求
        return render_template('adduser.html')  # 返回到添加用户界面
    else:  # 如果是post请求
        username = request.form.get('username')  # 通过form表单提交得到用户名
        password1 = request.form.get('password1')  # 通过form表单提交得到密码
        password2 = request.form.get('password2')  # 通过form表单提交得到密码
        if username == '':  # 如果用户名为空
            msg = '用户名不能为空'  # 提示信息为用户名不能为空
            return render_template('adduser.html',  msg=msg)  # 返回到添加用户页面
        list1 = User.query.filter(User.u_name == username).first()  # 通过该用户名在用户表中查询信息
        if list1:  # 如果查询到该信息
            msg = '已有该用户'  # 提示信息为已有该用户
            return render_template('adduser.html', msg=msg)  # 返回到添加用户页面并将提示信息传递过去
        else:  # 如果没有该条信息
            if password1 == '' or password2 == '':  # 如果两次输入表单中有任意一条为空
                msg = '密码不能为空'  # 提示信息为密码不能为空
                return render_template('adduser.html', msg=msg)  # 返回到添加用户页面并将提示信息传递过去
            if password1 != password2:  # 如果两次输入表单中提交的密码不相等
                msg = '两次密码不一致'  # 提示信息为两次密码不一致
                return render_template('adduser.html', msg=msg)  # 返回到添加用户页面并将提示信息传递过去
            else:  # 如果相等
                list1 = User(u_name=username, password=password1, role_id=2)  # 默认分配角色为用户
                db.session.add(list1)  # 将该信息添加到用户表中
                db.session.commit()  # 进行提交保存
                msg = '添加成功'  # 提示信息为添加成功
                return render_template('adduser.html', msg=msg)  # 返回到添加用户页面,并将提示信息传递过去

# 删除用户
@admin.route('/userdelete/')
def userdeletes():
    u_id = request.args.get('u_id')  # 通过get请求得到用户id
    User.query.filter(User.u_id == u_id).delete()  # 在用户表中删除该用户id对应的数据
    db.session.commit()  # 进行提交保存
    page = request.args.get('page', 1)  # 通过get请求得到页数,如果是第一次则规定为1
    per_page = 5  # 每页显示数据条数为5
    paginate = User.query.paginate(page, per_page, error_out=False)  # 当前页数,每页显示条数,是否显示错误
    users = paginate.items  # 当前页面所有信息
    msg = '删除成功'  # 提示信息为删除成功
    return render_template('users.html', msg=msg, paginate=paginate, users=users)  # 返回到用户页面并将提示信息和页面信息和页面所有信息传递过去

# 删除学生
@admin.route('/delete_student/', methods=['POST', 'GET'])
def delete_students():
    s_id = request.args.get('s_id')  # 通过git请求获得当前传递过来的id,即要删除的学生id
    Student.query.filter(Student.s_id == s_id).delete()  # 通过id从学生表中查找出要删除的学生进行删除
    db.session.commit()  # 进行提交
    msg = '删除成功'  # 定义msg
    page = int(request.args.get('page', 1))  # 通过get方式得到当前页,如果没有设置为1
    per_page = 5  # 设置每页数量
    paginate = Student.query.paginate(page, per_page, error_out=False)  # 当前页数,每页数量,是否打印错误
    stus = paginate.items  # 当前页面所有信息
    return render_template('student.html', msg=msg, stus=stus, paginate=paginate)  # 返回到班级页面



























