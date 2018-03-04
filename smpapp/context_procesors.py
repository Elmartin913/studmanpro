import datetime
from .models import SCHOOL_CLASS


def my_cp(request):

    ctx = {
        'date': datetime.date.today(),
        'version': '2.1.18.03.03',
        'all_class': SCHOOL_CLASS,
    }
    return ctx
