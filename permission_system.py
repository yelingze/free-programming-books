"""
A simple permission management system in Python.
This module defines basic User and Role classes and a function to check permissions.
"""

class User:
    """Represents a user with a name and a set of roles."""
    def __init__(self, name, roles=None):
        self.name = name
        self.roles = set(roles) if roles else set()

    def add_role(self, role):
        """Adds a role to the user."""
        self.roles.add(role)

    def remove_role(self, role):
        """Removes a role from the user."""
        self.roles.discard(role)

    def has_role(self, role):
        """Checks if the user has a specific role."""
        return role in self.roles

    def __str__(self):
        return f"User(name='{self.name}', roles={self.roles})"


class Role:
    """Represents a role with a name and a set of permissions."""
    def __init__(self, name, permissions=None):
        self.name = name
        self.permissions = set(permissions) if permissions else set()

    def add_permission(self, permission):
        """Adds a permission to the role."""
        self.permissions.add(permission)

    def remove_permission(self, permission):
        """Removes a permission from the role."""
        self.permissions.discard(permission)

    def has_permission(self, permission):
        """Checks if the role has a specific permission."""
        return permission in self.permissions

    def __str__(self):
        return f"Role(name='{self.name}', permissions={self.permissions})"


def check_permission(user, required_permission):
    """
    Checks if a user has a required permission.

    Args:
        user (User): The user to check.
        required_permission (str): The permission required.

    Returns:
        bool: True if the user has the permission, False otherwise.
    """
    # A superuser role grants all permissions
    if user.has_role('superuser'):
        return True

    # Check if any of the user's roles grants the required permission
    for role_name in user.roles:
        # In a real system, you would look up the Role object from a database or registry.
        # For this simple example, we'll assume a global `ROLES` dictionary exists.
        role = ROLES.get(role_name)
        if role and role.has_permission(required_permission):
            return True

    return False


# Global registry for roles (simplified for this example)
ROLES = {}

# Example usage and setup
if __name__ == "__main__":
    # Define some roles
    admin_role = Role("admin")
    admin_role.add_permission("read")
    admin_role.add_permission("write")
    admin_role.add_permission("delete")

    editor_role = Role("editor")
    editor_role.add_permission("read")
    editor_role.add_permission("write")

    viewer_role = Role("viewer")
    viewer_role.add_permission("read")

    # Register roles
    ROLES[admin_role.name] = admin_role
    ROLES[editor_role.name] = editor_role
    ROLES[viewer_role.name] = viewer_role

    # Create users and assign roles
    alice = User("Alice", ["admin"])
    bob = User("Bob", ["editor"])
    charlie = User("Charlie", ["viewer"])
    david = User("David") # No roles
    david.add_role("viewer")
    david.add_role("editor")

    # Test permissions
    print(f"Alice (admin) can delete: {check_permission(alice, 'delete')}")
    print(f"Bob (editor) can write: {check_permission(bob, 'write')}")
    print(f"Bob (editor) can delete: {check_permission(bob, 'delete')}")
    print(f"Charlie (viewer) can read: {check_permission(charlie, 'read')}")
    print(f"Charlie (viewer) can write: {check_permission(charlie, 'write')}")
    print(f"David (viewer+editor) can write: {check_permission(david, 'write')}")
    print(f"David (viewer+editor) can delete: {check_permission(david, 'delete')}")

    # Add superuser role to David
    david.add_role("superuser")
    print(f"David (now superuser) can delete: {check_permission(david, 'delete')}")