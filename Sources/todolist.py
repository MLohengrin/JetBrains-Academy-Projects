# To-Do List

from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}"


class ToDoList:
    menu = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit"

    def __init__(self, name) -> None:
        self.engine = create_engine(f'sqlite:///{name}.db?check_same_thread=False')
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)
        self.choices = {'1': self.get_today_tasks, '2': self.get_week_tasks, '3': self.get_all_tasks,
                        '4': self.missed_tasks, '5': self.add_task, '6': self.delete_task, '0': self.exit}
        self.running = True
        self.main()

    def exit(self):
        print("Bye!")
        self.running = False

    def missed_tasks(self):
        rows = self.session.query(Task).filter(Task.deadline < datetime.today()).order_by(Task.deadline).all()
        if rows:
            for n, row in enumerate(rows):
                print(f"{n + 1}. {row}. {row.deadline.strftime('%#d %b')}")
        else:
            print("Nothing is missed!")

    def delete_task(self):
        print("Choose the number of the task you want to delete:")
        rows = self.session.query(Task).order_by(Task.deadline).all()
        if rows:
            for n, row in enumerate(rows):
                print(f"{n + 1}. {row}. {row.deadline.strftime('%#d %b')}")
        else:
            print("Nothing to do!")
            return
        row = int(input())
        self.session.delete(rows[row - 1])
        self.session.commit()

    def get_today_tasks(self, input_date=datetime.today().date(), week_call=False):
        rows = self.session.query(Task).filter(Task.deadline == input_date).all()
        if week_call:
            print(f"{input_date.strftime('%A %d %b')}:")
        else:
            print(f"Today {datetime.today().date().strftime('%d %b')}:")
        if rows:
            for n, row in enumerate(rows):
                print(f"{n + 1}. {row}")
        else:
            print("Nothing to do!")

    def get_week_tasks(self):
        for n in range(7):
            self.get_today_tasks((datetime.today() + timedelta(days=n)).date(), True)
            print()

    def get_all_tasks(self):
        rows = self.session.query(Task).order_by(Task.deadline).all()
        if rows:
            for n, row in enumerate(rows):
                print(f"{n + 1}. {row}. {row.deadline.strftime('%#d %b')}")
        else:
            print("Nothing to do!")

    def add_task(self):
        task_input = input("Enter task\n")
        task_date_str = input("Enter deadline\n")
        task_date = [int(el) for el in task_date_str.split("-")]
        new_row = Task(task=task_input, deadline=datetime(task_date[0], task_date[1], task_date[2]))
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!")

    def main(self):
        while self.running:
            print(self.menu)
            self.choices.get(input(), self.exit)()
            print()


ToDoList('todo')
