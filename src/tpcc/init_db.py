from datetime import datetime
from random import choice, randint

from sqlalchemy.orm import sessionmaker

from tpcc.models import *
from tpcc.settings import WAREHOUSES


def populate(n):
    Session = sessionmaker(bind=engine)
    session = Session()

    cities = ('Moscow', 'St. Petersbrg', 'Pshkin', 'Oraneinbaum', 'Vladivostok')
    names = (
        'Ivan', 'Evgeniy', 'Alexander', 'Fedor', 'Julia', 'Stephany', 'Sergey', 'Natalya', 'Keanu', 'Jhon', 'Harry',
        'James')
    last_names = ('Petrov', 'Ivanov', 'Andreev', 'Mils', 'Smith', 'Anderson', 'Dominov', 'Tishenko', 'Zhitnikov')
    d_cnt = 0
    for i in range(1, n + 1):
        w = Warehouse(
            number=i,
            street_1='w_st %d' % i,
            street_2='w_st2 %d' % i,
            city=choice(cities),
            w_zip='w_zip %d' % i,
            tax=float(i),
            ytd=0
        )
        session.add(w)

        for j in range(10):
            d = District(
                warehouse_id=i,
                name='dist %d %d' % (w.number, j),
                street_1='d_st %d' % j,
                street_2='d_st2 %d' % j,
                city=w.city,
                d_zip='d_zip %d' % j,
                tax=float(j),
                ytd=0,
            )
            session.add(d)
            w.districts.append(d)
            d_cnt += 1

    for i in range(10 * n):
        c = Customer(
            first_name=choice(names),
            middle_name=choice(names),
            last_name=choice(last_names),
            street_1='c_st %d' % i,
            street_2='c_st2 %d' % i,
            city=choice(cities),
            c_zip='c_zip %d' % i,
            phone='phone',
            since=datetime(2005, 7, 14, 12, 30),
            credit='credit',
            credit_lim=randint(1000, 100000),
            discount=choice((0, 10, 15, 20, 30)),
            delivery_cnt=0,
            payment_cnt=0,
            balance=1000000,
            ytd_payment=0,
            data1='customer %d' % i,
            dtata2='hello %d' % i,
            district_id=randint(1, d_cnt),
        )
        session.add(c)
        d = session.query(District).filter(District.id == randint(1, d_cnt)).first()
        d.customers.append(c)
        session.commit()
    for i in range(1, n * 10 + 1):
        it = Item(
            name='item %d' % i,
            price=randint(1, 100000),
            data='data'
        )
        session.add(it)
        for j in range(1, n + 1):
            s = Stock(
                warehouse_id=j,
                item_id=i,
                quantity=100000,
                ytd=randint(1, 100000),
                order_cnt=0,
                remote_cnt=0,
                data="data",
            )
            session.add(s)
    session.commit()


def init_db(warehouses: int = WAREHOUSES):
    create_tables()
    populate(warehouses)


if __name__ == '__main__':
    init_db()
