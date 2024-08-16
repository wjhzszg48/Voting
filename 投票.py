#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:15:40 2024

@author: wjh
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 假设这是我们已经注册的学生及其密码
students_credentials = {
    "Alice": "password1",
    "Bob": "password2",
    "Charlie": "password3"
}

candidates = ["Candidate A", "Candidate B", "Candidate C"]
votes = {candidate: 0 for candidate in candidates}
voted_students = set()

# 登录页面
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in students_credentials and students_credentials[username] == password:
            session['username'] = username
            return redirect(url_for('vote'))
        else:
            return "用户名或密码错误，请重试。"
    return render_template_string('''
        <h2>登录</h2>
        <form method="post">
            用户名: <input type="text" name="username"><br>
            密码: <input type="password" name="password"><br>
            <input type="submit" value="登录">
        </form>
    ''')

# 投票页面
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == "POST":
        candidate = request.form.get("candidate")
        if username in voted_students:
            return f"<h3>{username} 已经投过票了，不能再次投票。</h3>"
        elif candidate not in candidates:
            return f"<h3>{candidate} 不是有效的候选人。</h3>"
        else:
            votes[candidate] += 1
            voted_students.add(username)
            return f"<h3>{username} 成功投票给 {candidate}！</h3>"

    return render_template_string('''
        <h2>投票页面</h2>
        <p>欢迎, {{username}}</p>
        <form method="post">
            候选人: <select name="candidate">
                {% for candidate in candidates %}
                <option value="{{candidate}}">{{candidate}}</option>
                {% endfor %}
            </select><br><br>
            <input type="submit" value="投票">
        </form>
    ''', username=username, candidates=candidates)

# 显示投票结果
@app.route("/results")
def results():
    result_html = "<h3>投票结果：</h3><ul>"
    for candidate, count in votes.items():
        result_html += f"<li>{candidate}: {count} 票</li>"
    result_html += "</ul>"
    return result_html

if __name__ == "__main__":
    app.run(debug=True)
