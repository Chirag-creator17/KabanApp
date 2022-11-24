from sendEmail import send_email
import os
import jwt
from functools import wraps
from flask import Flask, request, jsonify, send_file
from models import *
from datetime import datetime, timedelta
import requests
from celery import Celery
from celery.schedules import crontab
tz = pytz.timezone('Asia/Kolkata')
app.config['SECRET_KEY'] = 'chirag'

CORS(app)
celery = Celery("app")


class MyCeleryTasks(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.conf.update(broker_url="redis://localhost:6379/1",
                   result_backend="redis://localhost:6379/2", result_expires=60, timezone='Asia/Kolkata')
celery.Task = MyCeleryTasks

@app.route("/")
def trys():
    jobid=mains.delay()
    return str(jobid)

@celery.task()
def mains():
    print("hiii")
    return "<h1> Hello World </h1>"


# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, mains.s(), name='fast')


@app.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    # test = User.query.filter_by(email=email).first()
    user_info = User.query.filter_by(email=email).all()
    # Checking if user does not exist if not redirect to signup page
    if (len(user_info) != 0):
        return jsonify(message="User Already Exist"), 409
    else:
        name = request.json["name"]
        u_name = request.json["u_name"]
        password = request.json["password"]
        add_user = User(user_name=u_name, public_id=str(uuid.uuid4()), name=name, email=email,
                        password=password)  # Adding user to database
        db.session.add(add_user)
        db.session.commit()
        return jsonify(message="User added sucessfully"), 201


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]
    test = User.query.filter_by(email=email).first()
    # print(test)
    if (test is None):
        return jsonify(message="User does not exist"), 409
    elif (test.password == password):
        token = jwt.encode({
            'public_id': test.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=80)
        }, app.config['SECRET_KEY'])
        # access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", token=token.decode('UTF-8')), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


@app.route("/lists", methods=["GET", "POST", "PUT", "DELETE"])
@token_required
def lists(current_user):
    if (request.method == "GET"):
        lists = List.query.filter_by(user_id=current_user.user_id).all()
        results = [
            {
                "list_id": list.list_id,
                "list_name": list.list_name,
            } for list in lists]
        return jsonify(results), 200
    if (request.method == "POST"):
        # name = request.form['name']
        name = request.json['name']
        # print(name)
        add_list = List(list_name=name, user_id=current_user.user_id)
        db.session.add(add_list)
        db.session.commit()
        return jsonify(message="List added sucessfully"), 201
    if (request.method == "PUT"):
        list_id = request.json['list_id']
        list_name = request.json['list_name']
        list = List.query.filter_by(
            user_id=current_user.user_id, list_id=list_id).first()
        list.list_name = list_name
        db.session.commit()
        return jsonify(message="List updated sucessfully"), 201
    if (request.method == "DELETE"):
        list_id = request.json['list_id']
        list = List.query.filter_by(
            list_id=list_id, user_id=current_user.user_id).first()
        db.session.delete(list)
        db.session.commit()
        return jsonify(message="List deleted sucessfully"), 201


@app.route("/cards/<int:list_id>", methods=["GET", "POST", "PUT", "DELETE"])
@token_required
def cards(current_user, list_id):
    if (request.method == "GET"):
        card = Cards.query.filter_by(
            user_id=current_user.user_id, list_id=list_id).all()
        results = [
            {
                "list_id": card.list_id,
                "card_id": card.card_id,
                "card_title": card.card_title,
                "card_content": card.card_content,
                "card_deadline": card.card_deadline,
                "card_status": card.card_status,
                "card_completion_date": card.card_completion_date,
            } for card in card]
        return jsonify(results), 200
    if (request.method == "POST"):
        card_title = request.json['card_title']
        card_content = request.json['card_content']
        card_deadline = request.json['card_deadline']
        card_status = request.json['card_status']
        if (card_status == "False"):
            add_card = Cards(card_title=card_title, card_content=card_content, card_status=card_status,
                             list_id=list_id, card_deadline=card_deadline, user_id=current_user.user_id)
        else:
            card_completion_date = request.json['card_completion_date']
            add_card = Cards(card_title=card_title, card_content=card_content, card_status=card_status, list_id=list_id,
                             card_deadline=card_deadline, user_id=current_user.user_id, card_completion_date=card_completion_date)
        db.session.add(add_card)
        db.session.commit()
        return jsonify(message="Card added sucessfully"), 201
    if (request.method == "PUT"):
        card_id = request.json['card_id']
        card_title = request.json['card_title']
        card_content = request.json['card_content']
        card_deadline = request.json['card_deadline']
        card_status = request.json['card_status']
        if (card_status == "False"):
            card = Cards.query.filter_by(
                user_id=current_user.user_id, list_id=list_id, card_id=card_id).first()
            card.card_title = card_title
            card.card_content = card_content
            card.card_deadline = card_deadline
            card.card_status = card_status
            db.session.commit()
            return jsonify(message="Card updated sucessfully"), 201
        else:
            card_completion_date = request.json['card_completion_date']
            card = Cards.query.filter_by(
                user_id=current_user.user_id, list_id=list_id, card_id=card_id).first()
            card.card_title = card_title
            card.card_content = card_content
            card.card_deadline = card_deadline
            card.card_status = card_status
            card.card_completion_date = card_completion_date
            db.session.commit()
            return jsonify(message="Card updated sucessfully"), 201
    if (request.method == "DELETE"):
        card_id = request.json['card_id']
        card = Cards.query.filter_by(
            card_id=card_id, user_id=current_user.user_id, list_id=list_id).first()
        db.session.delete(card)
        db.session.commit()
        return jsonify(message="Card deleted sucessfully"), 201


@app.route("/downloadList/<int:list_id>", methods=["GET"])
@token_required
def downloadList(current_user, list_id):
    user = User.query.filter_by(user_id=current_user.user_id).first()
    lists = List.query.filter_by(
        user_id=current_user.user_id, list_id=list_id).first()
    cards = Cards.query.filter_by(
        user_id=current_user.user_id, list_id=list_id).all()
    no_of_completed = 0
    card_list = ""
    for card in cards:
        if (card.card_status == "True"):
            no_of_completed += 1
        card_list += (str(card.card_title)+" ")
    no_of_cards = len(cards)
    msg = "List Name: "+lists.list_name+"\nCards: " + \
        str(card_list)+"\nNo of cards: "+str(no_of_cards) + \
        "\nNo of completed cards: "+str(no_of_completed)
    title = lists.list_name + " Summary"
    file_name = lists.list_name+".csv"
    f = open(file_name, "w+")
    f.write("ListName,Cards,NoOfCards,NoOfCompletedCards\n")
    f.write("{},{},{},{}".format(lists.list_name,
            card_list, no_of_cards, no_of_completed))
    f.close()
    send_email(user.email, title, msg, file_name)
    os.remove(file_name)
    return "Downloaded"


@app.route("/downloadCard/<int:list_id>/<int:card_id>", methods=["GET"])
@token_required
@celery.task()
def downloadCard(current_user, list_id, card_id):
    user = User.query.filter_by(user_id=current_user.user_id).first()
    card = Cards.query.filter_by(
        user_id=current_user.user_id, list_id=list_id, card_id=card_id).first()
    lists = List.query.filter_by(
        user_id=current_user.user_id, list_id=list_id).first()
    file_name = card.card_title+".csv"
    f = open(file_name, "w+")
    f.write(
        "ListName,CardTitle,CardContent,CardDeadline,CardStatus,CardCompletionDate\n")
    f.write("{},{},{},{},{},{}".format(lists.list_name, card.card_title,
            card.card_content, card.card_deadline, card.card_status, card.card_completion_date))
    f.close()
    msg = "In List: "+lists.list_name+"\nCard Title: "+card.card_title+"\nCard Content: "+card.card_content+"\nCard Deadline: " + \
        str(card.card_deadline)+"\nCard Status: "+card.card_status + \
        "\nCard Completion Date: "+str(card.card_completion_date)
    title = card.card_title + " Summary"
    send_email(user.email, title, msg, file_name)
    os.remove(file_name)
    return "Downloaded"


chat_url = "https://chat.googleapis.com/v1/spaces/AAAAgU1jlvs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FaqDLwCpOo94YHAluK4nkk432m3iIogFYDqYx1t1zfk%3D"


@celery.task()
def massChat():
    message = {'text': "hello"}
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    requests.post(chat_url, data=json.dumps(message), headers=headers)
    return ""


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18), massChat.s(), name='Daily Reminder')


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
