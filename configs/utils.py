def numeric(s):
    return ''.join([n for n in s if n in '0123456789'])

def is_empty(s):
    if s in [None, '', 'null']:
        return True
    return False

def str_to_bool(s):
    if s in [1, True, 'TRUE', 'True', 'true', '1']:
        return True
    return False

def set_context(request):
    return {
        'request': request,
        'user': request.user,
    }

def serializer_context(resource):
    context = resource.get('context', None)

    ret = {
        'context': None,
        'request': None,
        'user': None,
    }

    if context is None:
        return ret

    user = context.get('user', None)
    if user is None or not user.is_authenticated:
        return ret

    return ret


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.MultipleObjectsReturned as e:
        print(e)
    except classmodel.DoesNotExist:
        return None


def obj_isset(obj, key):
    if key in dir(obj):
        return True
    return False