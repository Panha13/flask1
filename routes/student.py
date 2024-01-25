from flask import jsonify, request

from app import app, connection, text, render_template


@app.route('/admin/student')
def indexStudent():
    return render_template(
        'admin/student/index.html',
        module='student',
    )


@app.route('/api/student')
def get_students():
    # Assuming you have a table named 'students'
    query = text("SELECT * FROM students")
    result = connection.execute(query)
    students = [dict(row) for row in result]
    return jsonify(students)
