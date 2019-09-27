import pytest
import event
from datetime import datetime, timedelta

ref_date = datetime(2014, 2, 14, 11, 31, 51)


def test_event():
    e1 = event.Event("s1", "e1", ref_date, ref_date + timedelta(minutes=15),
                     "ended")
    e2 = event.Event("s2", "e2", ref_date + timedelta(20),
                     ref_date + timedelta(40), "ended")
    e3 = event.Event("s2", "e3", ref_date + timedelta(40),
                     ref_date + timedelta(100), "ended")

    l = event.EventList()
    l.add(e1)
    l.add(e3)
    l.add(e2)
    l.write()



if __name__ == "__main__":
    pytest.main()
