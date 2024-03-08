from project import db, create_app, user_models

with create_app().app_context():
    db.create_all()

    # db.session.add(User('admin', 'admin@example.com'))
    # db.session.add(User('guest', 'guest@example.com'))
    # db.session.commit()

    # users = User.query.all()
    # print(users)
