from django.contrib import admin

from zip_fleet.models import Aircraft, Airline

admin.site.register(Airline)
admin.site.register(Aircraft)
