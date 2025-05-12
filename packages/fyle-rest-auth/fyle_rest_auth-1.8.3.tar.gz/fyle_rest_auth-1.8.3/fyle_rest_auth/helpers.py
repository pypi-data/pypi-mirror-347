import logging
import traceback
from typing import Dict

from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.module_loading import import_string

from django_q.tasks import async_task

from .utils import AuthUtils, post_request, get_request
from .models import AuthToken

auth = AuthUtils()

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def get_cluster_domain_by_code(request):
    authorization_code = request.data.get('code')
    try:
        if not authorization_code:
            raise ValidationError('authorization code not found')

        tokens = auth.generate_fyle_refresh_token(authorization_code=authorization_code)

        cluster_domain = settings.API_URL.split('/api')[0] if settings.DEBUG \
            else get_cluster_domain(tokens['access_token'], auth.get_origin_address(request))

        return {
            'cluster_domain': cluster_domain,
            'tokens': tokens
        }

    except ValidationError as error:
        logger.info(error)
        raise

    except Exception as error:
        logger.error(traceback.format_exc())
        raise ValidationError(error) from error


def validate_code_and_login(request):
    authorization_code = request.data.get('code')
    try:
        if not authorization_code:
            raise ValidationError('authorization code not found')

        tokens = auth.generate_fyle_refresh_token(authorization_code=authorization_code)

        employee_info = get_fyle_admin(tokens['access_token'], auth.get_origin_address(request))
        logger.info('Employee Info %s', employee_info)
        users = get_user_model()

        user, _ = users.objects.get_or_create(
            user_id=employee_info['data']['user']['id']
        )

        if user and user.email != employee_info['data']['user']['email']:
            user.email = employee_info['data']['user']['email']
            user.full_name = employee_info['data']['user']['full_name']
            user.save()

        AuthToken.objects.update_or_create(
            user=user,
            defaults={
                'refresh_token': tokens['refresh_token']
            }
        )

        serializer = import_string(settings.FYLE_REST_AUTH_SERIALIZERS['USER_DETAILS_SERIALIZER'])
        tokens['user'] = serializer(user).data
        tokens['user']['full_name'] = employee_info['data']['user']['full_name']
        tokens['user']['org_id'] = employee_info['data']['org']['id']
        tokens['user']['org_name'] = employee_info['data']['org']['name']

        # Update Fyle Credentials with latest healthy token
        if 'async_update_user' in settings.FYLE_REST_AUTH_SETTINGS \
            and settings.FYLE_REST_AUTH_SETTINGS['async_update_user']:
            async_task(
                'apps.workspaces.tasks.async_update_fyle_credentials',
                employee_info['data']['org']['id'], tokens['refresh_token']
            )

        return tokens

    except ValidationError as error:
        logger.info(error)
        raise

    except Exception as error:
        logger.error(traceback.format_exc())
        raise ValidationError(error) from error


def validate_refresh_token_and_login(request):
    """
    Takes refresh_token from payload
    GET Fyle Admin info
    Get Or Create User
    Saves AuthToken
    Return Tokens
    """
    refresh_token = request.data.get('refresh_token')
    try:
        if not refresh_token:
            raise ValidationError('refresh token not found')

        tokens = auth.refresh_access_token(refresh_token)

        employee_info = get_fyle_admin(tokens['access_token'], auth.get_origin_address(request))
        users = get_user_model()

        user, _ = users.objects.get_or_create(
            user_id=employee_info['data']['user']['id']
        )

        if user and user.email != employee_info['data']['user']['email']:
            user.email = employee_info['data']['user']['email']
            user.full_name = employee_info['data']['user']['full_name']
            user.save()

        AuthToken.objects.update_or_create(
            user=user,
            defaults={
                'refresh_token': refresh_token
            }
        )

        serializer = import_string(settings.FYLE_REST_AUTH_SERIALIZERS['USER_DETAILS_SERIALIZER'])
        tokens['user'] = serializer(user).data
        tokens['user']['full_name'] = employee_info['data']['user']['full_name']
        tokens['user']['org_id'] = employee_info['data']['org']['id']
        tokens['user']['org_name'] = employee_info['data']['org']['name']
        tokens['refresh_token'] = refresh_token

        # Update Fyle Credentials with latest healthy token
        if 'async_update_user' in settings.FYLE_REST_AUTH_SETTINGS \
            and settings.FYLE_REST_AUTH_SETTINGS['async_update_user']:
            async_task(
                'apps.workspaces.tasks.async_update_fyle_credentials',
                employee_info['data']['org']['id'], tokens['refresh_token']
            )

        if 'async_update_user_settings_api' in settings.FYLE_REST_AUTH_SETTINGS \
            and settings.FYLE_REST_AUTH_SETTINGS['async_update_user_settings_api']:
            async_task(
                'apps.orgs.tasks.async_update_fyle_credentials',
                employee_info['data']['org']['id'], tokens['refresh_token']
            )

        return tokens

    except ValidationError as error:
        logger.info(error)
        raise

    except Exception as error:
        logger.error(traceback.format_exc())
        raise ValidationError(error) from error


def validate_and_refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    try:
        if not refresh_token:
            raise ValidationError('refresh token not found')

        tokens = auth.refresh_access_token(refresh_token)

        employee_info = get_fyle_admin(tokens['access_token'], auth.get_origin_address(request))
        users = get_user_model()

        user = users.objects.filter(
            email=employee_info['data']['user']['email'], user_id=employee_info['data']['user']['id']
        ).first()

        if not user:
            raise ValidationError('User record not found, please login')

        auth_token = AuthToken.objects.get(user=user)
        auth_token.refresh_token = refresh_token
        auth_token.save()

        serializer = import_string(settings.FYLE_REST_AUTH_SERIALIZERS['USER_DETAILS_SERIALIZER'])
        tokens['user'] = serializer(user).data
        tokens['refresh_token'] = refresh_token

        return tokens

    except ValidationError as error:
        logger.info(error)
        raise

    except Exception as error:
        logger.error(traceback.format_exc())
        raise ValidationError(error) from error


def get_cluster_domain(access_token: str, origin_address: str = None) -> str:
    """
    Get cluster domain name from fyle
    :param access_token: (str)
    :return: cluster_domain (str)
    """
    cluster_api_url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)

    return post_request(cluster_api_url, {}, access_token, origin_address)['cluster_domain']


def get_fyle_admin(access_token: str, origin_address: str = None) -> Dict:
    """
    Get user profile from fyle
    :param access_token: (str)
    :return: user_profile (dict)
    """
    cluster_domain = get_cluster_domain(access_token, origin_address)

    profile_api_url = '{}/platform/v1beta/spender/my_profile'.format(cluster_domain)
    employee_detail = get_request(profile_api_url, access_token, origin_address)

    if 'ADMIN' in employee_detail['data']['roles'] or \
        ('FYLE_MODULE' in settings.FYLE_REST_AUTH_SERIALIZERS and \
            settings.FYLE_REST_AUTH_SERIALIZERS['FYLE_MODULE'] == 'PARTNER_DASHBOARD'):
        return employee_detail
    else:
        raise ValidationError('User is not an admin')
