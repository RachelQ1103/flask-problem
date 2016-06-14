from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from problem import Problem


app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('problem'))


@app.route('/problem/list')
def problems():
    problem_list = Problem.query.all()
    # print('问题列表: ', problem_list)
    tr_list = []
    for p in problem_list:
        tr = p.table_row()
        tr_list.append(tr)
    return render_template('problems.html', problems=tr_list)


@app.route('/problem')
def problem():
    r = render_template('new_problem.html')
    # print(r)
    return r


@app.route('/problem/new', methods=['POST'])
def problem_new():
    p = Problem(request.form)
    p.save()
    # query = Problem.query.filter_by(link=request.form.get('link', '')).first()
    # print('刚存的问题: ', query)
    return redirect(url_for('problem'))


# /problem/update
# {
#   'id': 1
#   'status': true/false
# }
@app.route('/problem/update', methods=['POST'])
def problem_update():
    form = request.form[0]
    id = form.get('id', '')
    status = form.get('status', '')

    p = Problem.query.filter_by(id=id).first()
    p.solved = status
    p.save()
    print(p, p.status())
    return redirect(url_for('problems'))


if __name__ == '__main__':
    app.run(debug=True)

