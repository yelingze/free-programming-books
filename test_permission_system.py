import unittest
from permission_system import User, Role, check_permission, ROLES

class TestPermissionSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up roles for testing
        admin_role = Role("admin")
        admin_role.add_permission("read")
        admin_role.add_permission("write")
        admin_role.add_permission("delete")

        editor_role = Role("editor")
        editor_role.add_permission("read")
        editor_role.add_permission("write")

        viewer_role = Role("viewer")
        viewer_role.add_permission("read")

        ROLES.clear()
        ROLES[admin_role.name] = admin_role
        ROLES[editor_role.name] = editor_role
        ROLES[viewer_role.name] = viewer_role

    def test_user_role_assignment(self):
        user = User("TestUser")
        self.assertFalse(user.has_role("admin"))
        user.add_role("admin")
        self.assertTrue(user.has_role("admin"))
        user.remove_role("admin")
        self.assertFalse(user.has_role("admin"))

    def test_role_permission_assignment(self):
        role = Role("test_role")
        self.assertFalse(role.has_permission("fly"))
        role.add_permission("fly")
        self.assertTrue(role.has_permission("fly"))
        role.remove_permission("fly")
        self.assertFalse(role.has_permission("fly"))

    def test_check_permission_admin(self):
        admin_user = User("AdminUser", ["admin"])
        self.assertTrue(check_permission(admin_user, "read"))
        self.assertTrue(check_permission(admin_user, "write"))
        self.assertTrue(check_permission(admin_user, "delete"))

    def test_check_permission_editor(self):
        editor_user = User("EditorUser", ["editor"])
        self.assertTrue(check_permission(editor_user, "read"))
        self.assertTrue(check_permission(editor_user, "write"))
        self.assertFalse(check_permission(editor_user, "delete"))

    def test_check_permission_viewer(self):
        viewer_user = User("ViewerUser", ["viewer"])
        self.assertTrue(check_permission(viewer_user, "read"))
        self.assertFalse(check_permission(viewer_user, "write"))
        self.assertFalse(check_permission(viewer_user, "delete"))

    def test_check_permission_multiple_roles(self):
        multi_user = User("MultiUser")
        multi_user.add_role("viewer")
        multi_user.add_role("editor")
        self.assertTrue(check_permission(multi_user, "read"))
        self.assertTrue(check_permission(multi_user, "write"))
        self.assertFalse(check_permission(multi_user, "delete"))

    def test_check_permission_superuser(self):
        super_user = User("SuperUser", ["viewer"]) # Starts with viewer
        self.assertTrue(check_permission(super_user, "read"))
        self.assertFalse(check_permission(super_user, "delete"))

        super_user.add_role("superuser")
        self.assertTrue(check_permission(super_user, "delete")) # Superuser grants all
        self.assertTrue(check_permission(super_user, "nonexistent_permission"))

    def test_check_permission_no_roles(self):
        no_role_user = User("NoRoleUser")
        self.assertFalse(check_permission(no_role_user, "read"))

    def test_check_permission_nonexistent_role(self):
        # User has a role that isn't in the global ROLES registry
        user_with_bad_role = User("BadRoleUser", ["ghost_role"])
        # Should not cause an error, just return False
        self.assertFalse(check_permission(user_with_bad_role, "read"))

if __name__ == '__main__':
    unittest.main()