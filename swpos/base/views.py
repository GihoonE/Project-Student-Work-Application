from django.shortcuts import render, redirect
from . import models as m
import mysql.connector
import logging

db_conn = mysql.connector.connect(host='localhost', user='root', password = '2003300509Tem_',
                              database='COMPSCI_310')
cursor = db_conn.cursor()
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def base_view(request):

    return render(request, "homepage.html")

def student_view(request):
    # Fetch all positions
    cursor.execute("""
        SELECT DISTINCT p.position_name, p.position_type, 
                        hd.application_deadline, hd.date_of_posting,
                        hd.status_position, hd.description_detail, 
                        hd.description_link, hd.requirements, 
                        hd.hiring_number, hd.working_hours, 
                        hd.hourly_wage, d.department_name, s.professor_name, p.position_id
        FROM position p
        JOIN hiring_details hd ON p.position_id = hd.position_id
        JOIN supervisor s ON p.supervisor_id = s.supervisor_id
        JOIN super_dept sd ON s.supervisor_id = sd.supervisor_id
        JOIN department d ON sd.department_id = d.department_id
    """)
    list_position = cursor.fetchall()

    # Fetch unique department names
    cursor.execute("""
        SELECT DISTINCT department_name 
        FROM department
    """)
    unique_offices = cursor.fetchall()

    # Get filters from request
    div = request.GET.get('Office', 'None')
    pos_type = request.GET.get('Type', 'None')
    open_box = request.GET.get('Status', 'None')
    # Print or log the values for debugging
    print(f"Filter values - Office: {div}, Type: {pos_type}, Status: {open_box}")
    # Build the query based on filters
    query = """
        SELECT DISTINCT p.position_name, p.position_type, 
                        hd.application_deadline, hd.date_of_posting,
                        hd.status_position, hd.description_detail, 
                        hd.description_link, hd.requirements, 
                        hd.hiring_number, hd.working_hours, 
                        hd.hourly_wage, d.department_name, s.professor_name, p.position_id
        FROM position p
        JOIN hiring_details hd ON p.position_id = hd.position_id
        JOIN supervisor s ON p.supervisor_id = s.supervisor_id
        JOIN super_dept sd ON s.supervisor_id = sd.supervisor_id
        JOIN department d ON sd.department_id = d.department_id
    """
    conditions = []
    params = []
    if div != 'None':
        conditions.append("d.department_name = %s")
        params.append(div)
    if pos_type != 'None':
        conditions.append("p.position_type = %s")
        params.append(pos_type)
    if open_box != 'None':
        conditions.append("status_position = %s")
        params.append(open_box)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Print the final query and parameters for debugging
    print(f"Final SQL Query: {query}")
    print(f"Parameters: {params}")

    # Execute the query with the correct parameters
    cursor.execute(query, params)
    filtered_list = cursor.fetchall()

    print(filtered_list)

    # Render the appropriate template
    template = "student_page.html" if all(
        param == 'None' for param in (div, pos_type, open_box)) else "student_search.html"
    return render(request, template, {'Position_list': filtered_list, 'Office_option': unique_offices})


def faculty_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Fetch the supervisor based on username and password
        cursor.execute("""
            SELECT * FROM supervisor 
            WHERE email = %s
        """, [username])
        faculty = cursor.fetchone()


        if faculty and str(faculty[1]) == password:
            # Fetch supervisor's posts
            request.session['id'] = faculty[0]
            cursor.execute("""
                SELECT DISTINCT p.position_name, p.position_type, 
                                hd.application_deadline, hd.date_of_posting,
                                hd.status_position, hd.description_detail, 
                                hd.description_link, hd.requirements, 
                                hd.hiring_number, hd.working_hours, 
                                hd.hourly_wage, s.supervisor_id, s.professor_name, p.position_id
                FROM position p
                JOIN hiring_details hd ON p.position_id = hd.position_id
                JOIN supervisor s ON p.supervisor_id = s.supervisor_id
                WHERE s.email = %s
            """, [username])
            posts = cursor.fetchall()
            return render(request, "f_page.html", {'posts': posts, 'f_name': faculty[1]})

        # Login fail
        return render(request, "f_login.html")

    return render(request, "f_login.html")

def faculty_add_poster(request):
    if request.method == 'POST':
        # Extract data from form
        id = request.session.get('id')
        position_name = request.POST.get('position_title')
        position_type = request.POST.get('position_type')
        application_deadline = request.POST.get('deadline')
        hiring_number = request.POST.get('hiring_number')
        monthly_working_hours = request.POST.get('monthly_working_hours')
        hourly_wage = request.POST.get('hourly_wage')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')

        # Validate the data (simple validation example)
        if not position_name or not position_type:
            # Handle invalid data - maybe display an error message
            return render(request, "f_add.html", {'error': 'Missing required fields'})

        # Insert the new job posting into the database
        cursor.execute("""
            INSERT INTO position (position_name, position_type, supervisor_id)  # Assuming supervisor_id is needed
            VALUES (%s, %s, %s)
        """, [position_name, position_type, id])  # Replace supervisor_id with actual value

        # Get the last inserted position_id for the position just added
        position_id = cursor.lastrowid

        # Insert into hiring_details table
        cursor.execute("""
            INSERT INTO hiring_details (position_id, application_deadline, hiring_number, working_hours, hourly_wage, description_detail, requirements, date_of_posting)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIME)
        """, [position_id, application_deadline, hiring_number, monthly_working_hours, hourly_wage, description, requirements])
        db_conn.commit()
        # Redirect or inform the user of successful addition
        return render(request, "f_add_success.html", {'message': 'Position added successfully'})

    # If it's a GET request, just display the form
    return render(request, "f_add.html")

def application(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume_link = request.POST.get('resume_link')
        position_id = request.GET.get('position_id', None)

        if not email or not name:
            # Handle invalid data - maybe display an error message
            return render(request, "application.html", {'error': 'Missing required fields'})

        cursor.execute("""
                    INSERT INTO applicant (name, email, resume_link)  # Assuming supervisor_id is needed
                    VALUES (%s, %s, %s)
                """, [name, email, resume_link])
        cursor.execute("SELECT LAST_INSERT_ID();")
        applicant_id = cursor.fetchone()[0]
        print(applicant_id)
        print(position_id)

        cursor.execute("""
                            INSERT INTO applicant_position (applicant_id, position_id, cover_letter_link, application_status)  # Assuming supervisor_id is needed
                            VALUES (%s, %s, %s, %s)
                        """, [applicant_id, position_id, resume_link, "Submitted"])

        db_conn.commit()

        return render(request, "a_success.html", {'message': 'Position added successfully'})

    return render(request, "application.html")


def delete_position(request, position_id):
    if request.method == 'POST':
        with db_conn.cursor() as cursor:
            # Delete from hiring_details table
            cursor.execute("DELETE FROM hiring_details WHERE position_id = %s", [position_id])

            # Delete from position table
            cursor.execute("DELETE FROM position WHERE position_id = %s", [position_id])
            db_conn.commit()

        # Redirect to the referring page (refresh the current page)
        return render(request, 'deleted.html')

def applicants(request):
    position_id = request.GET.get('position_id')

    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT a.applicant_id, a.name, a.email, a.resume_link, ap.application_status
            FROM applicant a
            JOIN applicant_position ap ON a.applicant_id = ap.applicant_id
            WHERE ap.position_id = %s
        """, [position_id])
        applicants = cursor.fetchall()


    context = {
        'applicants': applicants,
        'position_id': position_id
    }

    return render(request, 'applicants.html', context)

def interview(request, applicant_id, position_id):
    if request.method == 'POST':
        interview_date = request.POST.get('interview_date')
        interview_notes = request.POST.get('interview_notes')
        supervisor_id = request.session.get('id')  # Assuming supervisor_id is stored in session

        # Validate the data (simple validation example)
        if not interview_date or not interview_notes:
            # Handle invalid data - maybe display an error message
            return render(request, "interview.html", {'error': 'Missing required fields'})

        cursor.execute("""
            INSERT INTO interview (applicant_id, position_id, supervisor_id, interview_date, interview_notes)
            VALUES (%s, %s, %s, %s, %s)
        """, [applicant_id, position_id, supervisor_id, interview_date, interview_notes])

        db_conn.commit()

        return render(request, "i_success.html", {'message': 'Interview sent to applicant email'})

    # Load initial form data or handle GET request
    return render(request, "interview.html", {'applicant_id': applicant_id, 'position_id': position_id})
