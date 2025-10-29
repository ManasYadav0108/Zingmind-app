# from django.shortcuts import render, redirect
# import mysql.connector as sql

# def login_view(request):
#     msg = ""
#     if request.method == "POST":
#         em = request.POST.get("email")
#         pwd = request.POST.get("password")

#         try:
#             m = sql.connect(host="localhost", user="root", password="Sharad@19", database="zingmind")
#             cursor = m.cursor(dictionary=True)

#             cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (em, pwd))
#             user = cursor.fetchone()

#             if user:
#                 return redirect("welcome")  # <-- add this in urls.py
#             else:
#                 msg = "Invalid email or password"

#         except Exception as e:
#             msg = f"Database error: {str(e)}"

#     return render(request, "login.html", {"msg": msg})
