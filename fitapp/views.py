from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Exercise
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


# Create your views here.
# home page  views
def index(request):
    return render(request, 'index.html')

# register page views
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')

        if not terms:
            messages.error(request, 'You must agree to the Terms of Service.')
            return redirect('register')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already in use')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account successfully created')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    return render(request, 'register.html')
    

# login views
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User not found')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
# logout views
def logout(request):
    auth.logout(request)
    return redirect('/')

# fitness views
def fitness(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to create your workout plan')
        return redirect('login')

    # Fetch existing exercises for the user
    saved_exercises = Exercise.objects.filter(user=request.user)

    if request.method == 'POST':
        try:
            # Get the arrays of exercise data
            exercise_names = request.POST.getlist('exercise_name[]')
            exercise_targets = request.POST.getlist('exercise_target[]')
            exercise_units = request.POST.getlist('exercise_unit[]')
            preset_type = request.POST.get('preset_type')

            # Validate input
            if not exercise_names or not preset_type:
                messages.error(request, 'Please select a preset and add at least one exercise')
                return render(request, 'fitness.html', {'saved_exercises': saved_exercises})

            # Delete old exercises for the user to avoid duplicates
            saved_exercises.delete()

            # Save each exercise for the current user
            for name, target, unit in zip(exercise_names, exercise_targets, exercise_units):
                Exercise.objects.create(
                    user=request.user,
                    exercise_name=name,
                    exercise_target=int(target),
                    exercise_unit=unit,
                    preset_type=preset_type
                )

            messages.success(request, 'Workout plan successfully updated')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error in creating workout plan: {str(e)}')
    
    # If no exercises exist for the user, provide a default preset
    if not saved_exercises.exists():
        default_preset = [
            {'exercise_name': '', 'exercise_target': '', 'exercise_unit': 'minutes'}
        ]
        return render(request, 'fitness.html', {'default_preset': default_preset})
    
    return render(request, 'fitness.html', {'saved_exercises': saved_exercises})


# dashboard views
def dashboard(request):
    if request.user.is_authenticated:
        # Fetch all exercises for the logged-in user
        exercises = Exercise.objects.filter(user=request.user)
        
        # Optional: Calculate some additional statistics
        total_exercises = exercises.count()
        completed_exercises = exercises.filter(completed__gt=0)
        
        context = {
            'exercises': exercises,
            'total_exercises': total_exercises,
            'completed_exercises': completed_exercises
        }
        
        return render(request, 'dashboard.html', context)
    else:
        messages.warning(request, 'Please log in to view your dashboard')
        return redirect('login')
    
# update exercise view.
@require_POST
def update_exercise(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        exercise_id = data.get('exercise_id')
        completed_count = data.get('completed_count')

        # Validate input
        if not exercise_id or completed_count is None:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        # Fetch the specific exercise for the current user
        try:
            exercise = Exercise.objects.get(id=exercise_id, user=request.user)
        except Exercise.DoesNotExist:
            return JsonResponse({'error': 'Exercise not found'}, status=404)

        # Update the completed count
        exercise.completed += completed_count
        exercise.save()

        # Calculate remaining 
        total = exercise.exercise_target
        completed = exercise.completed
        remaining = max(0, total - completed)

        return JsonResponse({
            'exercise_id': exercise.id,
            'completed': completed,
            'total': total,
            'remaining': remaining,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)