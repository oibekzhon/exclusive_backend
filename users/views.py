import json
import hashlib
import secrets
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .models import PasswordResetRequest, UserProfile

PUBLIC_ALLOWED_ROLES = {'CUSTOMER', 'SELLER'}
HIDDEN_ROLES = {'ADMIN', 'OPERATOR', 'COURIER'}


def reset_token_digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


def user_data(user):
    profile = getattr(user, 'profile', None)
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'role': profile.role if profile else 'CUSTOMER',
        'status': profile.status if profile else 'ACTIVE',
    }


def request_data(request):
    try:
        return json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return None


@require_GET
def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@require_GET
def users_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required.'}, status=401)

    users = [user_data(user) for user in User.objects.order_by('id')]
    return JsonResponse({'users': users, 'count': len(users)})


@require_POST
def register(request):
    data = request_data(request)
    if data is None:
        return JsonResponse({'detail': 'Request body must be valid JSON.'}, status=400)

    username = str(data.get('username', '')).strip()
    email = str(data.get('email', '')).strip().lower()
    password = data.get('password', '')
    requested_role = str(data.get('role', 'CUSTOMER')).strip().upper()

    if not username or not email or not password:
        return JsonResponse(
            {'detail': 'username, email and password are required.'},
            status=400,
        )
    if len(password) < 8:
        return JsonResponse(
            {'detail': 'Password must contain at least 8 characters.'},
            status=400,
        )
    if requested_role in HIDDEN_ROLES:
        return JsonResponse(
            {'detail': 'Admin, Operator and Courier cannot be created through public registration.'},
            status=400,
        )
    if requested_role not in PUBLIC_ALLOWED_ROLES:
        return JsonResponse(
            {'detail': 'Public registration allows only CUSTOMER or SELLER roles.'},
            status=400,
        )
    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Username is already in use.'}, status=409)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'detail': 'Email is already in use.'}, status=409)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=str(data.get('firstName', '')).strip(),
        last_name=str(data.get('lastName', '')).strip(),
    )
    UserProfile.objects.create(
        user=user,
        role=requested_role,
        status='ACTIVE',
    )
    login(request, user)
    return JsonResponse({'user': user_data(user)}, status=201)


@require_POST
def login_user(request):
    data = request_data(request)
    if data is None:
        return JsonResponse({'detail': 'Request body must be valid JSON.'}, status=400)

    username = str(data.get('username', '')).strip()
    password = data.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Invalid username or password.'}, status=401)

    login(request, user)
    return JsonResponse({'user': user_data(user)})


@require_POST
def request_password_reset(request):
    data = request_data(request)
    if data is None:
        return JsonResponse({'detail': 'Request body must be valid JSON.'}, status=400)

    email = str(data.get('email', '')).strip().lower()
    if not email:
        return JsonResponse({'detail': 'email is required.'}, status=400)

    user = User.objects.filter(email__iexact=email).first()
    if user:
        code = f'{secrets.randbelow(1_000_000):06d}'
        PasswordResetRequest.objects.filter(user=user, verified_at__isnull=True).delete()
        PasswordResetRequest.objects.create(
            user=user,
            code_hash=make_password(code),
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        send_mail(
            subject='Password reset code',
            message=f'Your password reset code is {code}. It expires in 10 minutes.',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

    return JsonResponse({'detail': 'If an account exists for this email, a reset code has been sent.'})


@require_POST
def verify_password_reset_code(request):
    data = request_data(request)
    if data is None:
        return JsonResponse({'detail': 'Request body must be valid JSON.'}, status=400)

    email = str(data.get('email', '')).strip().lower()
    code = str(data.get('code', '')).strip()
    reset_request = PasswordResetRequest.objects.filter(
        user__email__iexact=email,
        verified_at__isnull=True,
    ).select_related('user').order_by('-created_at').first()
    if not reset_request or reset_request.is_expired() or not check_password(code, reset_request.code_hash):
        return JsonResponse({'detail': 'Invalid or expired reset code.'}, status=400)

    reset_token = secrets.token_urlsafe(32)
    reset_request.reset_token_hash = reset_token_digest(reset_token)
    reset_request.verified_at = timezone.now()
    reset_request.save(update_fields=['reset_token_hash', 'verified_at'])
    return JsonResponse({'resetToken': reset_token})


@require_POST
def reset_password(request):
    data = request_data(request)
    if data is None:
        return JsonResponse({'detail': 'Request body must be valid JSON.'}, status=400)

    reset_token = str(data.get('resetToken', '')).strip()
    username = str(data.get('username', '')).strip()
    password = data.get('password', '')
    if not reset_token or not username or not password:
        return JsonResponse({'detail': 'resetToken, username and password are required.'}, status=400)
    if len(password) < 8:
        return JsonResponse({'detail': 'Password must contain at least 8 characters.'}, status=400)

    reset_request = PasswordResetRequest.objects.filter(
        reset_token_hash=reset_token_digest(reset_token),
        verified_at__isnull=False,
    ).select_related('user').first()
    if not reset_request:
        return JsonResponse({'detail': 'Invalid or expired reset token.'}, status=400)
    if User.objects.exclude(pk=reset_request.user.pk).filter(username=username).exists():
        return JsonResponse({'detail': 'Username is already in use.'}, status=409)

    user = reset_request.user
    user.username = username
    user.set_password(password)
    user.save(update_fields=['username', 'password'])
    reset_request.delete()
    return JsonResponse({'detail': 'Username and password updated successfully.'})


@require_POST
def logout_user(request):
    logout(request)
    return JsonResponse({'detail': 'Logged out successfully.'})


@require_GET
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required.'}, status=401)
    return JsonResponse({'user': user_data(request.user)})