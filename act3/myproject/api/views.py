import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# In-memory upload list
uploads = [
    
]

# Helper to get next upload ID
def get_next_upload_id():
    return max(upload['id'] for upload in uploads) + 1 if uploads else 1

# GET all uploads or search
def uploads_list(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    search = request.GET.get('search', '').lower()
    if search:
        filtered = [upload for upload in uploads if search in upload['description'].lower() or search in upload['name'].lower()]
        return JsonResponse(filtered, safe=False)

    return JsonResponse(uploads, safe=False)

# GET one upload
def get_upload(request, upload_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    for upload in uploads:
        if upload['id'] == upload_id:
            return JsonResponse(upload)
    return JsonResponse({'error': 'Upload not found'}, status=404)

# POST add upload
@csrf_exempt
def add_upload(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body.decode())
        name = data.get('name')
        upload_num = int(data.get('upload'))
        description = data.get('description')

        if not all([name, upload_num, description]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        new_upload = {
            'id': get_next_upload_id(),
            'name': name,
            'upload': upload_num,
            'description': description
        }

        uploads.append(new_upload)
        return JsonResponse(new_upload, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# PUT update upload
@csrf_exempt
def update_upload(request, upload_id):
    if request.method != 'PUT':
        return HttpResponseNotAllowed(['PUT'])

    try:
        data = json.loads(request.body.decode())
        for upload in uploads:
            if upload['id'] == upload_id:
                upload['name'] = data.get('name', upload['name'])
                upload['upload'] = int(data.get('upload', upload['upload']))
                upload['description'] = data.get('description', upload['description'])
                return JsonResponse(upload)

        return JsonResponse({'error': 'Upload not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# DELETE upload
@csrf_exempt
def delete_upload(request, upload_id):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])

    global uploads
    filtered = [upload for upload in uploads if upload['id'] != upload_id]
    if len(filtered) == len(uploads):
        return JsonResponse({'error': 'Upload not found'}, status=404)

    uploads = filtered
    return JsonResponse({'message': f'Upload {upload_id} deleted'})

# Frontend pages
def signup_page(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')

# POST signup
@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': f'User {user.username} created successfully.'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# POST login
@csrf_exempt
def user_login(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'message': f'User {username} logged in successfully'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
