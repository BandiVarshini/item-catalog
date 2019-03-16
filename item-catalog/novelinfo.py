from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from novel_database import Novel, Base, Book, User
engine = create_engine('sqlite:///bookdata.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()

User1 = User(
    name="Varshini008",
    email="varshinibandi98@gmail.com",
    picture="https://plus.google.com/"
            "u/1/photos/117797260060813425788/albums/"
            "profile/6625538226519025762?iso=false"
    )
session.add(User1)
session.commit()

novel1 = Novel(name="Novel List", user_id=1)
session.add(novel1)
session.commit()

book1 = Book(
        book_name="A Prayer for Owen Meany",
        author="Irving, John",
        no_of_pages="200",
        genre="Literary",
        book_id=1,
        user_id=1
        )
session.add(book1)
session.commit()

book2 = Book(
        book_name="A Confederacy of Dunces",
        author="Toole, John Kennedy",
        no_of_pages="250",
        genre="Literary",
        book_id=1,
        user_id=1
    )
session.add(book2)
session.commit()

book3 = Book(
        book_name="A Separate Peace",
        author="Knowles, John",
        no_of_pages="250",
        genre="Young Adult",
        book_id=1,
        user_id=1
    )
session.add(book3)
session.commit()
print("List of books are added")
