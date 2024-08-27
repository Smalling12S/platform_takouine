import logging
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import authenticate, login
from .decorators import notLoggedUsers,allowedUsers,forAdmins
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json










def home(requset):
    return render(requset,"platformTK/home.html")



@notLoggedUsers
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.filter(name='Etudiants').exists():
                return redirect('/homeEtudiant')  # Redirect to student's home
            elif request.user.groups.filter(name='Prof').exists():
                return redirect('/homeProf')
            elif request.user.groups.filter(name='SuperAdmin').exists():
                return redirect('/homeSuperAdmin')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, "platformTK/login.html")




from django.contrib.auth.decorators import login_required

#Logout for all
def userLogout(request):
   logout(request)
   return redirect('home')



def homeEtudiant(requset):
    return render(requset,"platformTK/Etudiant/homeEtudiant.html")




@login_required(login_url='login')
@allowedUsers(allowedGroups=['Prof'])
def homeProf(request):
    try:
        current_prof = prof.objects.get(user=request.user)
        groups = Groups.objects.filter(profs=current_prof)
        competitions = Competitions.objects.filter(prof=current_prof)
    except prof.DoesNotExist:
        groups = Groups.objects.none()
        competitions = Competitions.objects.none()

    return render(request, "platformTK/Prof/homeProf.html", {"groups": groups, "competitions": competitions})




def Groupes(requset):
    groups = Groups.objects.all()
    context = {"groups":groups}
    return render(requset,"platformTK/Prof/Groupes.html",context)





@login_required(login_url='login')
@allowedUsers(allowedGroups=['Prof'])
def competitions_list(request):
    try:
        current_prof = prof.objects.get(user=request.user)
        groups = Groups.objects.filter(profs=current_prof)
        competitions = Competitions.objects.filter(prof=current_prof)
        
    except prof.DoesNotExist:
        groups = Groups.objects.none()
        competitions = Competitions.objects.none()

    context = {"competitions": competitions, "groups": groups}
    return render(request, "platformTK/Prof/Competitions.html", context)





@login_required(login_url='login')
@allowedUsers(allowedGroups=['Prof'])
def add_competition(request):
    try:
        current_prof = prof.objects.get(user=request.user)
        groups = Groups.objects.filter(profs=current_prof)
    except prof.DoesNotExist:
        groups = Groups.objects.none()
        current_prof = None  # Set to None if no prof is found

    if request.method == 'POST':
        name = request.POST.get('name')
        number_of_sections = request.POST.get('number_of_sections')
        selected_group = request.POST.get('group')  # Get selected group

        # Validate input
        if name and number_of_sections and selected_group:
            try:
                number_of_sections = int(number_of_sections)
                selected_group = Groups.objects.get(id=selected_group)  # Fetch the selected group

                if current_prof:
                    # Save the new competition to the database
                    competition = Competitions.objects.create(
                        name=name,
                        number_of_sections=number_of_sections,
                        group=selected_group,  # Associate the selected group
                        prof=current_prof  # Associate the competition with the logged-in professor
                    )

                    # Redirect to the add_section view with the new competition's ID
                    return redirect('add_section', competition_id=competition.id)
            except (ValueError, Groups.DoesNotExist):
                # Handle invalid number_of_sections or invalid group
                pass

    return render(request, 'platformTK/Prof/add_competition.html', {'groups': groups})  # Render a form to add a competition





from django.urls import reverse

def add_section(request, competition_id):
    competition = get_object_or_404(Competitions, id=competition_id)
    
    # Get all students in the competition's group
    all_students = competition.group.etudiants.all()

    # Get students already assigned to any section in this competition
    assigned_students = Etudiant.objects.filter(sections__competition=competition).distinct()

    # Exclude assigned students from the list of available students
    available_students = all_students.exclude(id__in=assigned_students.values_list('id', flat=True))

    # Get the current number of sections for this competition
    current_sections_count = competition.sections.count()

    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        selected_students_str = request.POST.get('students')  # Get the string of selected students

        # Clean the string to remove any trailing comma and split into a list of IDs
        selected_students = list(map(int, selected_students_str.strip(',').split(',')))

        # Check if the current number of sections is less than the allowed number of sections
        if current_sections_count < competition.number_of_sections:
            if section_name:
                # Create the new section for the competition
                section = Sections.objects.create(
                    competition=competition,
                    section_name=section_name
                )

                # Add selected students to the section
                section.etudiants.set(selected_students)
                section.save()

                # Redirect back to the same page to add more sections if needed
                return redirect('add_section', competition_id=competition.id)
        else:
            # Build the competition_sections URL
            competition_sections_url = reverse('competition_sections', args=[competition.id])

            # Display an error message with a link to the competition sections page
            error_message = f"You cannot add more sections than the allowed number. <a href='{competition_sections_url}'>Go to Competition Sections</a>"
            return render(request, 'platformTK/Prof/add_section.html', {
                'competition': competition,
                'students': available_students,
                'error_message': error_message,
                'current_sections_count': current_sections_count,
            })

    return render(request, 'platformTK/Prof/add_section.html', {
        'competition': competition,
        'students': available_students,  # Use the filtered list of available students
        'current_sections_count': current_sections_count,
    })




def competition_sections(request, competition_id):
    competition = get_object_or_404(Competitions, id=competition_id)
    sections = competition.sections.all().order_by('-points')  # Get all sections related to the competition
    return render(request, 'platformTK/Prof/competition_sections.html', {'competition': competition, 'sections': sections})





def finish_competition(request, competition_id):
    competition = get_object_or_404(Competitions, id=competition_id)

    # Check if the competition has already been finished
    if competition.is_finished:
        # Redirect to the results page without awarding points again
        return redirect('competition_results', competition_id=competition.id)
    
    # Get sections ordered by points in descending order
    top_sections = competition.sections.all().order_by('-points')[:3]  # Get top 3 sections
    
    # Points distribution for 1st, 2nd, and 3rd places
    points_distribution = [10, 5, 1]
    
    # Award points to the etudiants in each of the top 3 sections
    for index, section in enumerate(top_sections):
        points_to_add = points_distribution[index]  # Points based on rank (1st, 2nd, 3rd)
        for etudiant in section.etudiants.all():
            etudiant.points = (etudiant.points or 0) + points_to_add  # Add points
            etudiant.save()  # Save the updated points

    # Mark the competition as finished
    competition.is_finished = True
    competition.save()

    # Redirect to the results page after finishing the competition
    return redirect('competition_results', competition_id=competition.id)





def competition_results(request, competition_id):
    competition = get_object_or_404(Competitions, id=competition_id)
    sections = competition.sections.all().order_by('-points')  # Order sections by points descending

    return render(request, 'platformTK/Prof/competition_results.html', {
        'competition': competition,
        'sections': sections,
    })





def rank_competition(request, competition_id):
    competition = get_object_or_404(Competitions, id=competition_id)
    return redirect('competition_results', competition_id=competition.id)



@csrf_exempt
def increment_section_points(request, section_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount', 0)
        try:
            section = Sections.objects.get(id=section_id)
            # Ensure amount is an integer
            amount = int(amount)
            section.points += amount
            section.save()
            return JsonResponse({'success': True, 'new_points': section.points})
        except Sections.DoesNotExist:
            return JsonResponse({'error': 'Section not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)



@csrf_exempt
def decrement_section_points(request, section_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount', 0)
        try:
            section = Sections.objects.get(id=section_id)
            # Ensure amount is an integer
            amount = int(amount)
            section.points -= amount
            section.save()
            return JsonResponse({'success': True, 'new_points': section.points})
        except Sections.DoesNotExist:
            return JsonResponse({'error': 'Section not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)









def Store(requset):
    return render(requset,"platformTK/Prof/Store.html")




def Profil(requset):
    return render(requset,"platformTK/Prof/Profil.html")




def group_detail(request, code_group):
    # Retrieve the group using the unique code_group
    group = get_object_or_404(Groups, code_group=code_group)
    # Get all students associated with this group
    students = group.etudiants.all()
    return render(request, "platformTK/Prof/group_detail.html", {"group": group, "students": students})





def Répartition_points(request, code_group):
    # Retrieve the group using the unique code_group
    group = get_object_or_404(Groups, code_group=code_group)
    # Get all students associated with this group
    students = group.etudiants.all().order_by('-points')
    return render(request, "platformTK/Prof/Répartition_points.html", {"group": group, "students": students})





@csrf_exempt  
def update_points(request, student_id):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        amount = data.get('amount')
        
        try:
            student = Etudiant.objects.get(id=student_id)
            student.points += int(amount)
            student.save()
            return JsonResponse({'success': True})
        except Etudiant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})





@csrf_exempt  
def subtract_points(request, student_id):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        amount = abs(int(data.get('amount')))  

        try:
            student = Etudiant.objects.get(id=student_id)
            if student.points >= amount:
                student.points -= amount  
                student.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Insufficient points'})
        except Etudiant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})





def homeSuperAdmin(requset):
    return render(requset,"platformTK/SuperAdmin/homeSuperAdmin.html")



def add_groupe(requset):
    etudiants = Etudiant.objects.all()
    profs = prof.objects.all()
    groups = Groups.objects.all()
    return render(requset,"platformTK/SuperAdmin/add_groupe.html", {
        'groups': groups,
        'etudiants': etudiants,
        'profs': profs
    })




def add_student(requset):
    etudiants = Etudiant.objects.all()
    profs = prof.objects.all()
    groups = Groups.objects.all()
    return render(requset,"platformTK/SuperAdmin/add_student.html", {
        'groups': groups,
        'etudiants': etudiants,
        'profs': profs
    })



def group_list(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        description = request.POST.get('description')
        student_ids_str = request.POST.get('students', '')  # Get the comma-separated student IDs as a string
        prof_ids_str = request.POST.get('profs', '')  # Get the comma-separated professor IDs as a string

        # Convert the comma-separated strings into lists of integers
        student_ids = [int(id) for id in student_ids_str.split(',') if id.isdigit()]
        prof_ids = [int(id) for id in prof_ids_str.split(',') if id.isdigit()]

        # Debugging output to verify received data
        print("Group Name:", group_name)
        print("Description:", description)
        print("Selected Students IDs:", student_ids)
        print("Selected Professors IDs:", prof_ids)

        # Create and save the new group
        group = Groups(name=group_name, description=description)
        group.save()

        # Add students and professors to the group
        students = Etudiant.objects.filter(id__in=student_ids)
        profs = prof.objects.filter(id__in=prof_ids)
        
        group.etudiants.set(students)
        group.profs.set(profs)
        group.save()

        return redirect('add_groupe')  # Ensure 'add_groupe' is defined in your URL patterns

    etudiants = Etudiant.objects.all()
    profs = prof.objects.all()
    groups = Groups.objects.all()

    return render(request, 'platformTK/SuperAdmin/add_groupe.html', {
        'groups': groups,
        'etudiants': etudiants,
        'profs': profs
    })


def add_etudiant(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        date_de_naissance = request.POST.get('date_de_naissance')
        email = request.POST.get('email')
        numéro_de_téléphone = request.POST.get('numéro_de_téléphone')
        avatar = request.FILES.get('avatar')

        if not username or not password or not prenom or not nom or not date_de_naissance or not email:
            # Handle missing fields (return an error message or redirect to a form with errors)
            return render(request, "platformTK/SuperAdmin/add_student.html", {'error': 'Please fill in all required fields.'})

        try:
            # Create User
            user = User.objects.create_user(username=username, password=password)

            # Create Etudiant
            Etudiant.objects.create(
                user=user,
                prenom=prenom,
                nom=nom,
                date_de_naissance=date_de_naissance,
                email=email,
                numéro_de_téléphone=numéro_de_téléphone,
                avatar=avatar
            )
            
            group = Group.objects.get(name="Etudiants")
            user.groups.add(group)


            return redirect('add_student')  # Ensure 'add_student' is a valid URL name

        except Exception as e:
            # Handle any exceptions (return an error message or log the error)
            return render(request, "platformTK/SuperAdmin/add_student.html", {'error': str(e)})

    return render(request, "platformTK/SuperAdmin/add_student.html")








import csv
import pandas as pd



logger = logging.getLogger(__name__)

def add_students_from_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        
        if not file:
            messages.error(request, 'No file uploaded.')
            return render(request, "platformTK/SuperAdmin/add_student.html")

        if file.name.endswith('.csv'):
            try:
                data = csv.reader(file.read().decode('utf-8').splitlines())
                next(data)  # Skip the header row

                for row in data:
                    if len(row) < 6:
                        continue  # Skip rows with insufficient data

                    username, password, prenom, nom, date_de_naissance, email, *rest = row
                    numéro_de_téléphone = rest[0] if rest else ""
                    avatar = None  # Handling avatar from CSV is complex; assume it's not provided

                    if not username or not password or not prenom or not nom or not date_de_naissance or not email:
                        continue  # Skip rows with missing required fields

                    try:
                        user = User.objects.create_user(username=username, password=password)
                        Etudiant.objects.create(
                            user=user,
                            prenom=prenom,
                            nom=nom,
                            date_de_naissance=date_de_naissance,
                            email=email,
                            numéro_de_téléphone=numéro_de_téléphone,
                            avatar=avatar
                        )
                        
                        group = Group.objects.get(name="Etudiants")
                        user.groups.add(group)
                        
                    except Exception as e:
                        # Log the error with more user-friendly output
                        logger.error(f"Error processing row with username '{username}': {e}")
                        messages.error(request, f"Error processing row with username '{username}': {e}")

            except Exception as e:
                logger.error(f"Error reading CSV file: {e}")
                messages.error(request, 'An error occurred while reading the CSV file.')
                return redirect('add_student')

            messages.success(request, 'Students added successfully from the CSV file.')
            return redirect('add_student')

        elif file.name.endswith('.xlsx'):
            try:
                df = pd.read_excel(file)

                # Drop irrelevant or unnamed columns
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                
                for _, row in df.iterrows():
                    username = row.get('username')
                    password = row.get('password')
                    prenom = row.get('prenom')
                    nom = row.get('nom')
                    date_de_naissance = row.get('date_de_naissance')
                    email = row.get('email')
                    numéro_de_téléphone = row.get('numéro_de_téléphone', '')
                    avatar = None  # Handling avatar from Excel is complex; assume it's not provided

                    # Skip rows with missing required fields
                    if pd.isna(username) or pd.isna(password) or pd.isna(prenom) or pd.isna(nom) or pd.isna(date_de_naissance) or pd.isna(email):
                        logger.warning(f"Skipping row due to missing data: {row.to_dict()}")
                        continue

                    try:
                        user = User.objects.create_user(username=username, password=password)
                        Etudiant.objects.create(
                            user=user,
                            prenom=prenom,
                            nom=nom,
                            date_de_naissance=date_de_naissance,
                            email=email,
                            numéro_de_téléphone=numéro_de_téléphone,
                            avatar=avatar
                        )
                        group = Group.objects.get(name="Etudiants")
                        user.groups.add(group)
                        
                    except Exception as e:
                        # Log the error with more user-friendly output
                        logger.error(f"Error processing row with username '{username}': {e}")
                        messages.error(request, f"Error processing row with username '{username}': {e}")
            
            except Exception as e:
                logger.error(f"Error reading Excel file: {e}")
                messages.error(request, 'An error occurred while reading the Excel file.')
                return redirect('add_student')

            messages.success(request, 'Students added successfully from the Excel file.')
            return redirect('add_student')

        else:
            messages.error(request, 'Unsupported file type. Please upload a CSV or Excel file.')
            return render(request, "platformTK/SuperAdmin/add_student.html")

    return render(request, "platformTK/SuperAdmin/add_student.html")
