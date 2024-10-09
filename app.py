from flask import Flask, render_template, jsonify, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# بيانات المحلات مع حالة كل محل
shops = [
    {"id": 1, "name": "محل البطاطا", "status": "مفتوح"},
    {"id": 2, "name": "محل 2", "status": "مغلق"},
    {"id": 3, "name": "محل 3", "status": "مفتوح"}
]

# بيانات أصحاب المحلات
owners = {
    "owner1": {"password": "password1", "shop_id": 1},
    "owner2": {"password": "password2", "shop_id": 2},
    "owner3": {"password": "password3", "shop_id": 3}
}

@app.route('/')
def index():
    return render_template('index.html', shops=shops)

# صفحة تسجيل الدخول لأصحاب المحلات
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # التحقق من بيانات تسجيل الدخول
        if username in owners and owners[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('owner_dashboard'))

        return "اسم المستخدم أو كلمة المرور غير صحيحة"

    return render_template('login.html')

# لوحة تحكم صاحب المحل
@app.route('/owner_dashboard')
def owner_dashboard():
    # التحقق من وجود جلسة تسجيل دخول
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    shop_id = owners[username]['shop_id']
    shop = next((shop for shop in shops if shop['id'] == shop_id), None)
    
    return render_template('owner_dashboard.html', shop=shop)

# تغيير حالة المحل من لوحة التحكم
@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    shop_id = owners[username]['shop_id']
    
    new_status = request.form['status']
    for shop in shops:
        if shop['id'] == shop_id:
            shop['status'] = new_status
            break

    return redirect(url_for('owner_dashboard'))

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
