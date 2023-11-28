from django.shortcuts import render, redirect
from . import models as m
import mysql.connector

db_conn = mysql.connector.connect(user='root', password='kihun87522099@',
                              host='127.0.0.1',
                              database='CS310_Project')
cursor = db_conn.cursor()
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse

def base_view(request):

    return render(request, "homepage.html")

def student_view(request):
    cursor.execute("""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                      from position natural join hiring_details natural join position_detail natural join position_timeline""")
    list_position = cursor.fetchall()

    cursor.execute('select distinct office_name, count(*) from hiring_details group by office_name')
    unique_offices = cursor.fetchall()

    div= request.GET.get('Office')
    pos_type= request.GET.get('Type')
    open_box = request.GET.get('Status')

    if ((div is None and pos_type is None and open_box is None) or (div == "None" and pos_type == "None" and open_box is None)):
        # default list
        return render(request, "student_page.html",{'Position_list':list_position,'Office_option': unique_offices})
    else:
        if div == "None" and open_box == "None":
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where position_type = '{pos_type}'""")
            filtered_list = cursor.fetchall()
        elif pos_type == "None" and open_box == "None":
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where office_name = '{div}'""")
            filtered_list = cursor.fetchall()
        elif div == "None" and pos_type == "None":
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where status_position = '{open_box}'""")
            filtered_list = cursor.fetchall()
        elif div == "None":
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where position_type = '{pos_type}' and status_position = '{open_box}'""")
            filtered_list = cursor.fetchall()
        elif pos_type == "None":
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where office_name = '{div}' and status_position = '{open_box}'""")
            filtered_list = cursor.fetchall()
        elif open_box == "None":
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where position_type = '{pos_type}' and office_name = '{div}'""")
            filtered_list = cursor.fetchall()
        else:
            cursor.execute(f"""select distinct position_name, position_type, 
				                      office_name, application_deadline,
				                      date_of_posting,status_position,
				                      position_description, description_link,
				                      requirements, hiring_number, working_hours, hourly_wage
				                from position natural join hiring_details natural join position_detail natural join position_timeline
                                where position_type = '{pos_type}' and office_name = '{div}' and status_position = '{open_box}'""")
            filtered_list = cursor.fetchall()
        return render(request, "student_search.html",{'Position_list':filtered_list, 'Office_option': unique_offices})


def faculty_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cursor.execute("""select * from supervisor""")
        faculty = cursor.fetchall()
        for f in faculty:
            if f[1] == username and f[0]==int(password):
                cursor.execute(f"""select distinct position_name, position_type, 
				                                  office_name, application_deadline,
				                                  date_of_posting,status_position,
				                                  position_description, description_link,
				                                  requirements, hiring_number,
				                                  working_hours, hourly_wage,
				                                  supervisor_id, professor_name
				                    from position natural join hiring_details natural join position_detail natural join position_timeline natural join supervisor
                                    where professor_name ='{username}' and supervisor_id = '{password}'""")
                posts = cursor.fetchall()
                return render(request, "f_page.html",{'posts':posts, 'f_name':f[1]})
        #Login fail
        return render(request,"f_login.html")

    return render(request,"f_login.html")

def faculty_add_poster(request):

    return render(request,"f_add.html")