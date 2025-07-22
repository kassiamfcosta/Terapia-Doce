from rest_framework import permissions

class IsAdminStaff(permissions.BasePermission):
    """
    Permissão personalizada que permite acesso apenas para usuários staff (administradores).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Permite que usuários não autenticados criem registros (POST),
    mas exige autenticação para outras operações.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated