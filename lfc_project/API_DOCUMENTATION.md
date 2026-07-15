LFC Church Management System API Documentation

Base URL

/api/

Authentication

Authentication uses JWT Bearer Tokens.

Header:

Authorization: Bearer <access_token>

⸻

Accounts Module

Login

POST

/api/accounts/login/

Request

{
    "email": "father@lfcchurch.com",
    "password": "Password@123"
}

Response

{
    "refresh": "jwt_refresh_token",
    "access": "jwt_access_token"
}

Permission

Public

⸻

Current User

GET

/api/accounts/me/

Permission

Authenticated User

⸻

Security Settings Module

Active Sessions

GET

/api/accounts/settings/sessions/

Permission

Authenticated User

Response

[
    {
        "id": 1,
        "session_id": "uuid",
        "ip_address": "127.0.0.1",
        "user_agent": "PostmanRuntime",
        "last_activity": "2026-06-21T10:00:00Z",
        "is_active": true,
        "created_at": "2026-06-21T09:00:00Z"
    }
]

⸻

Login History

GET

/api/accounts/settings/login-history/

Permission

Authenticated User

⸻

Logout Current Session

POST

/api/accounts/settings/logout/

Permission

Authenticated User

⸻

Logout All Devices

POST

/api/accounts/settings/logout-all/

Permission

Authenticated User

⸻

Force Logout Session

POST

/api/accounts/settings/sessions/<id>/force-logout/

Permission

SuperAdmin

⸻

Parish Module

Parish Details

GET

/api/parish/

Permission

Public

⸻

Update Parish

PUT

/api/parish/

PATCH

/api/parish/

Permission

SuperAdmin

⸻

Dashboard Module

Dashboard Statistics

GET

/api/parish/dashboard/

Permission

CanViewReports

Response

{
    "staffs": {},
    "family_units": {},
    "families": {},
    "family_members": {},
    "events": {},
    "notices": {},
    "gallery": {}
}

⸻

Permission Management Module

List Permissions

GET

/api/parish/permissions/

Permission

SuperAdmin

⸻

Assign Permission

POST

/api/parish/permissions/

Request

{
    "user_id": 5,
    "permission": "MANAGE_EVENTS"
}

Permission

SuperAdmin

⸻

User Permissions

GET

/api/parish/users/<user_id>/permissions/

Permission

SuperAdmin

⸻

Delete Permission

DELETE

/api/parish/permissions/<id>/

Permission

SuperAdmin

⸻

Bulk Update Permissions

PUT

/api/parish/permissions/bulk-update/

Request

{
    "user_id": 5,
    "permissions": [
        "MANAGE_FAMILIES",
        "MANAGE_EVENTS",
        "MANAGE_GALLERY"
    ]
}

Permission

SuperAdmin

⸻

Family Unit Module

Endpoints

GET     /api/families/family-units/
POST    /api/families/family-units/
GET     /api/families/family-units/<id>/
PUT     /api/families/family-units/<id>/
PATCH   /api/families/family-units/<id>/
DELETE  /api/families/family-units/<id>/

⸻

Family Module

Endpoints

GET     /api/families/families/
POST    /api/families/families/
GET     /api/families/families/<id>/
PUT     /api/families/families/<id>/
PATCH   /api/families/families/<id>/
DELETE  /api/families/families/<id>/

⸻

Family Member Module

Endpoints

GET     /api/families/family-members/
POST    /api/families/family-members/
GET     /api/families/family-members/<id>/
PUT     /api/families/family-members/<id>/
PATCH   /api/families/family-members/<id>/
DELETE  /api/families/family-members/<id>/

⸻

Parish Groups Module

Group Endpoints

GET     /api/parish-groups/groups/
POST    /api/parish-groups/groups/
GET     /api/parish-groups/groups/<id>/
PUT     /api/parish-groups/groups/<id>/
PATCH   /api/parish-groups/groups/<id>/
DELETE  /api/parish-groups/groups/<id>/

⸻

Group Member Endpoints

GET     /api/parish-groups/group-members/
POST    /api/parish-groups/group-members/
GET     /api/parish-groups/group-members/<id>/
PUT     /api/parish-groups/group-members/<id>/
PATCH   /api/parish-groups/group-members/<id>/
DELETE  /api/parish-groups/group-members/<id>/

⸻

Events Module

Endpoints

GET     /api/events/
POST    /api/events/
GET     /api/events/<id>/
PUT     /api/events/<id>/
PATCH   /api/events/<id>/
DELETE  /api/events/<id>/
GET     /api/events/featured/

⸻

Notices Module

Endpoints

GET     /api/notices/
POST    /api/notices/
GET     /api/notices/<id>/
PUT     /api/notices/<id>/
PATCH   /api/notices/<id>/
DELETE  /api/notices/<id>/
GET     /api/notices/featured/

⸻

Gallery Module

Album Endpoints

GET     /api/gallery/albums/
POST    /api/gallery/albums/
GET     /api/gallery/albums/featured/
GET     /api/gallery/albums/<id>/
PUT     /api/gallery/albums/<id>/
PATCH   /api/gallery/albums/<id>/
DELETE  /api/gallery/albums/<id>/

⸻

Photo Endpoints

GET     /api/gallery/photos/
POST    /api/gallery/photos/
GET     /api/gallery/photos/<id>/
PUT     /api/gallery/photos/<id>/
PATCH   /api/gallery/photos/<id>/
DELETE  /api/gallery/photos/<id>/

⸻

Staff Module

Endpoints

GET     /api/staffs/
POST    /api/staffs/
GET     /api/staffs/<id>/
PUT     /api/staffs/<id>/
PATCH   /api/staffs/<id>/
DELETE  /api/staffs/<id>/

⸻

Pagination

All list endpoints support:

?page=1&page_size=20

Default:

page_size = 20

Maximum:

page_size = 100

⸻

File Upload Validation

Supported image formats:

jpg
jpeg
png
webp

Maximum upload size:

5 MB

Supported document formats:

pdf
doc
docx

Maximum document size:

10 MB

⸻

Roles

SUPERADMIN
STAFF
FAMILY_UNIT_PRESIDENT
GROUP_LEADER
USER

⸻

System Version

LFC Church Management System
Backend Version: 1.0.0
Framework: Django + Django REST Framework
Authentication: JWT + Session Validation


