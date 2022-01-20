# This file is needed because MemberManaagement (where the command actually lives)
# is not in INSTALLED_APPS (and shouldn't be!)
from MemberManagement.management.commands.gen_local_settings import Command
__all__ = ["Command"]
