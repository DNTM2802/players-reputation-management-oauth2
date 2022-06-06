#from oauth2_provider.models import AbstractAccessToken, AbstractApplication, AbstractGrant, AbstractRefreshToken, AbstractIDToken
from django.db import models


# class AccessToken(AbstractAccessToken):
#     usages = models.IntegerField(default=0)
#
#     def is_valid(self, scopes=None):
#         print(f"Usages: {self.usages}")
#         print(f"Scopes: {self.scopes}")
#         if super().is_valid(scopes) and not self.is_usage_expired():
#             self.usages += 1
#             self.save()
#             return True
#         return False
#
#     def is_usage_expired(self):
#         return self.usages > 1
#
#
# class Application(AbstractApplication):
#     pass
#
#
# class Grant(AbstractGrant):
#     pass
#
#
# class RefreshToken(AbstractRefreshToken):
#     pass
#
#
# class IDToken(AbstractIDToken):
#     pass

