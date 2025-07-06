""" Permission Values """
ORGANIZATION_PERMISSIONS = (
    {"name": "organization:read_details",
     "description": "View the organization's name, description, and settings."},
    {"name": "organization:update_settings", "description":
        "Update the organization's name, description, and settings."},
    {"name": "organization:delete",
     "description": "Delete the entire organization (typically owner-only)."},
    {"name": "organization:manage_members",
     "description": "Invite, remove, and view members of the organization."},
    {"name": "organization:manage_roles", "description": "Assign roles to members."},
    {"name": "organization:create_custom_roles",
     "description": "Create new custom roles within the organization."},
    {"name": "organization:manage_custom_roles",
     "description": "Edit and delete custom roles within the organization."},
    {"name": "organization:view_audit_log", "description": "View the organization's audit log."},
    {"name": "organization:manage_billing",
     "description": "View and manage billing information and subscription."},
)

TEAM_PERMISSIONS = (
    {'name': 'team:create', 'description': 'Create new teams within the organization.'},
    {'name': 'team:read', 'description': 'View teams and their basic details.'},
    {'name': 'team:update', 'description': "Update a team's name and description."},
    {'name': 'team:delete', 'description': 'Delete a team.'},
    {'name': 'team:manage_members', 'description': 'Add or remove members from a team.'}
)

PROJECT_PERMISSIONS = (
    {'name': 'project:create', 'description': 'Create new projects.'},
    {'name': 'project:read', 'description': 'View project details, tasks, and members.'},
    {'name': 'project:update',
     'description': 'Update project details (name, description, due dates).'},
    {'name': 'project:delete', 'description': 'Delete a project.'},
    {'name': 'project:manage_members', 'description': 'Add or remove members from a project.'},
    {'name': 'project:change_status',
     'description': 'Change the status of a project (e.g., Active, Archived, Completed).'}
)

TASK_PERMISSIONS = (
    {'name': 'task:create', 'description': 'Create new tasks within a project.'},
    {'name': 'task:read', 'description': 'View task details, comments, and attachments.'},
    {'name': 'task:update',
     'description': 'Update task details (title, description, status, priority).'},
    {'name': 'task:delete', 'description': 'Delete a task.'},
    {'name': 'task:assign_user', 'description': 'Assign or unassign users to a task.'},
    {'name': 'task:change_status',
     'description': "Change a task's status (e.g., To Do, In Progress, Done)."},
    {'name': 'task:comment', 'description': 'Add comments to a task.'},
    {'name': 'task:manage_attachments', 'description': 'Add or delete attachments on a task..'}
)

REPORT_PERMISSIONS = (
    {'name': 'reports:view', 'description': 'View project and organization analytics dashboards.'},
    {'name': 'reports:export', 'description': 'Export reports as CSV or PDF.'}
)

ALL_PERMISSIONS = (ORGANIZATION_PERMISSIONS +
                   TEAM_PERMISSIONS +
                   PROJECT_PERMISSIONS +
                   TASK_PERMISSIONS +
                   REPORT_PERMISSIONS)


ORGANIZATION_ROLES = {
    "owner": {
        "name": "Owner",
        "description": "The creator of the organization. This role is hard-coded and not editable.",
        "permissions": [
            perm['name'] for perm in ORGANIZATION_PERMISSIONS + TEAM_PERMISSIONS +
                                     PROJECT_PERMISSIONS + TASK_PERMISSIONS + REPORT_PERMISSIONS
        ]
    },
    "admin":  {
        "name": "Administrator",
        "description": "A high-level role for managing the organization's workspace.",
        "permissions": [
            'organization:read_details',
            'organization:update_settings',
            'organization:manage_members',
            'organization:manage_roles',
            'organization:create_custom_roles',
            'organization:view_audit_log',
            'team:create',
            'team:update',
            'team:delete',
            'team:manage_members',
            'project:create',
            'project:delete'
        ]
    },
    "member": {
        "name": "Member",
        "description": "he default role for most users, "
                       "allowing them to collaborate on projects they are a part of.",
        "permissions":[
            'organization:read_details',
             'team:read',
             'project:read',
             'task:create',
             'task:read',
             'task:update',
             'task:assign_user',
             'task:change_status',
             'task:comment',
             'task:manage_attachments'
        ]
    },
    "team_lead": {
        "name": "Team Lead",
        "description": "A specialized role for managing a specific team and its projects."
                       " This could also be a custom role created by an org admin.",
        "permissions":[
            'organization:read_details',
            'team:read',
            'project:read',
            'task:create',
            'task:read',
            'task:update',
            'task:assign_user',
            'task:change_status',
            'task:comment',
            'task:manage_attachments',
            'team:update',
            'team:manage_members',
            'project:create',
            'project:update',
            'project:manage_members'
        ]
    },
    "viewer": {
        "name": "Viewer",
        "description": "A read-only role, perfect for clients or stakeholders who"
                       " need to see progress without making changes.",
        "permissions": [
            'team:update',
             'team:manage_members',
             'project:create',
             'project:update',
             'project:manage_members'
        ]
    }
}


TEAM_ROLES = {
    "owner": {
        "name": "Team Owner",
        "description": "The creator or main administrator of the team. Has full "
                       "control over the team.",
        "permissions": [
            perm['name'] for perm in TEAM_PERMISSIONS + PROJECT_PERMISSIONS + TASK_PERMISSIONS
        ]
    },
    "lead": {
        "name": "Team Lead",
        "description": "Manages the team and its projects. Can update team info and"
                       "manage members.",
        "permissions": [
            'team:read',
            'team:update',
            'team:manage_members',
            'project:create',
            'project:read',
            'project:update',
            'project:manage_members',
            'task:create',
            'task:read',
            'task:update',
            'task:assign_user',
            'task:change_status',
            'task:comment',
            'task:manage_attachments'
        ]
    },
    "member": {
        "name": "Team Member",
        "description": "A regular member who can participate in projects and tasks.",
        "permissions": [
            'team:read',
            'project:read',
            'task:create',
            'task:read',
            'task:update',
            'task:assign_user',
            'task:change_status',
            'task:comment',
            'task:manage_attachments'
        ]
    },
    "viewer": {
        "name": "Team Viewer",
        "description": "Read-only access to team, projects, and tasks.",
        "permissions": [
            'team:read',
            'project:read',
            'task:read'
        ]
    }
}
