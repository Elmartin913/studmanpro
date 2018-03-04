import datetime


def my_cp(request):
    ctx = {
        'date': datetime.date.today(),
        'version': '2.1.18.03.03',

    }
    return ctx
