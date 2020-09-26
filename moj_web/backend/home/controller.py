from flask import Blueprint, render_template, request

## pre DB
from moj_web.backend.models import db
from moj_web.backend.models import Quote #import tab Quote

home= Blueprint("home", __name__)

@home.route('/')
def view_homepage():
    page = request.args.get("page", 1, type=int)
    paginate = Quote.query.order_by(Quote.id.desc()).paginate(page, 2, False)
    return render_template("/home/home.jinja",
    quotes=paginate.items, ##pre zobrazenie citátov
    paginate=paginate) ## potrebné pre zobrazenie číslovania)