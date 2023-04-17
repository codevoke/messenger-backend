from flask import Flask, render_template, request, make_response, redirect
import db
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def search():
    # automatically redirect authorized user
    if validate_user(request):
        return redirect('/chat')

    if request.method == 'POST':
        email, password, *_ = request.form.values()
        login = db.login(email, password)
        print(login)
        if not login[0]:
            return render_template("login.html", errors=login[1], values=[email, password])
        response = make_response(redirect('/chat'))
        _id, _token = login[1], login[2]
        response.set_cookie('id', str(_id))
        response.set_cookie('token', _token)
        return response
    return render_template("login.html")


# вроде оно работает, лучше не трогать
@app.route('/registration', methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        # reg stage 1
        if request.form.get("email"):
            email, password = request.form.values()
            result = db.registry(email, password)
            print("result")
            if True in result:
                response = make_response(render_template('acc_start.html'))
                response.set_cookie('id', str(result[1]), max_age=60 ** 2 * 24)
                response.set_cookie('token', result[2], max_age=60 ** 2 * 24)
                print("resp-> ", response)
                return response
            else:
                # return values and errors
                return render_template('reg.html', values=[email, password], errors=result[1])

        # reg stage 2
        if request.form.get("firstname"):
            # validating user's registration part 1
            id = int(request.cookies.get('id'))
            token = request.cookies.get('token')
            print(id, token)
            if not db.validate_token(id, token):
                response = make_response(render_template('reg.html'))
                response = clear_cookie(response)
                return response

            file = request.files['file']
            firstname, lastname = request.form.values()
            db.registry_2(id, firstname, lastname, file)
            return redirect('/chat')

    return render_template("reg.html")


@app.route('/try-register', methods=['POST', 'GET'])
def try_reg():
    data = request.json
    json_schema = db.try_reg(data['email'], data['password'])
    return json_schema


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    # validate user
    if not validate_user(request):
        response = make_response(redirect('/login'))
        response = clear_cookie(response)
        return response
    # ну явно не просто рендер темплэйт
    return render_template('chat.html')


def validate_user(user_request):
    if user_request.cookies.get('id') is None or \
            user_request.cookies.get('token') is None:
        return False
    id = int(user_request.cookies.get('id'))
    token = user_request.cookies.get('token')
    if not db.validate_token(id, token):
        return False
    return True


def clear_cookie(data_response):
    data_response.delete_cookie('id')
    data_response.delete_cookie('token')
    return data_response


if __name__ == '__main__':
    app.run()
