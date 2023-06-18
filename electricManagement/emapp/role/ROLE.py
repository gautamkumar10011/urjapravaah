from accounts.models import User 

KEY_CONTROL_PANEL = "control_panel"
KEY_FEEDER = "feeder"
KEY_STATION = "station"
KEY_FEEDER_STATION = "feederStation"

KEY_READ   = "Read"
KEY_CREATE = "Create"
KEY_UPDATE = "Update"
KEY_DELETE = "Delete"
CREATE = 8
READ   = 4
UPDATE = 2
DELETE = 1

def isValidOperation(roleKey, opertationType, username):
    user = User.objects.get(username=username)
    roleId = user.roleId
    if not roleId: return False

    if KEY_FEEDER ==roleKey:
        return isUserAllowedForOperation(roleId.feeder, opertationType)
    elif KEY_STATION ==roleKey:
        return isUserAllowedForOperation(roleId.station, opertationType)
    elif KEY_FEEDER_STATION ==roleKey:
        return isUserAllowedForOperation(roleId.feederStation, opertationType)                    
    elif KEY_CONTROL_PANEL ==roleKey:
        return isUserAllowedForOperation(roleId.control_panel, opertationType)
    else:
        return False    


def isUserAllowedForOperation(role, opertationType):
    if role:
        if KEY_READ == opertationType:
            return role.value & READ != 0               
        elif KEY_CREATE == opertationType:
            return role.value & CREATE != 0
        elif KEY_UPDATE == opertationType:
            return role.value & UPDATE != 0        
        elif KEY_DELETE == opertationType:
            return role.value & DELETE != 0 
    return False
