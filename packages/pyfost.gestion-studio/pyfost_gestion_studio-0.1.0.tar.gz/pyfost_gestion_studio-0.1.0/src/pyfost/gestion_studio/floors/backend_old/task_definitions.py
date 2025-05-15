from .models import ResourceCategoryEnum

# Define which tasks are needed for each resource type assignment
# This could be stored in the database for more flexibility
TASK_TEMPLATES = {
    ResourceCategoryEnum.USER: [
        "Create/Enable User Account",
        "Assign Group Permissions",
        "Provide Login Credentials",
        "Inform User of Seat Location",
    ],
    ResourceCategoryEnum.WORKSTATION: [
        "Install Workstation Hardware",
        "Connect Peripherals (Monitor, Keyboard, Mouse)",
        "Network Configuration",
        "Install Standard OS/Software",
        "Asset Tagging",
    ],
    ResourceCategoryEnum.SOFTWARE_LICENSE: [
        "Assign License Key",
        "Verify License Activation",
        "Document Assignment",
    ],
    ResourceCategoryEnum.OTHER: [
        "Generic Setup Task",
        "Clean Desk Area",
    ],
}


def get_tasks_for_resource_type(resource_category: ResourceCategoryEnum) -> list[str]:
    """Returns a list of task type strings for a given resource category."""
    return TASK_TEMPLATES.get(
        resource_category, TASK_TEMPLATES[ResourceCategoryEnum.OTHER]
    )
