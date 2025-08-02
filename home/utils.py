import csv
from django.core.management.base import BaseCommand
from .models import *

class Command(BaseCommand):
    help = 'Import fort details from CSV file'

    def handle(self, *args, **kwargs):
        with open('home/fort_details.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fort = Forts(
                    fort_district=row['district'],
                    fort_name=row['fort_name'],
                    fort_latitude=row['lat'],
                    fort_longitude=row['lon'],
                    link=row['link']
                )
                fort.save()
        self.stdout.write(self.style.SUCCESS('Successfully imported fort details.'))


# This is for retriving accurate lat long data from forts.csv that i have downloaded 
def add_lat_lon():
    with open('home/forts.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                 fort = Forts.objects.filter(fort_name__icontains=row['name']).first()
                 if fort:
                    fort.fort_latitude = row['latitude']
                    fort.fort_longitude = row['longitude']
                    fort.save()
                    count += 1
                    print(f"Add lat long for {fort.fort_name}")
            print(count)


import os
def add_fort_images():
    count= 0
    for filename in os.listdir("public/media/img/fort_images"):
        # Get file name without extension and its extension
        base_name, ext = os.path.splitext(filename)
        
        # Search the fortname in fort_obj
        fort_obj = Forts.objects.filter(fort_name__icontains=base_name).first()
        if fort_obj:
            fort_obj.fort_image = f"img/fort_images/{filename}"
            fort_obj.save()
            count += 1
    print(count)


def lat_long_transfer():
    forts_obj = Forts.objects.all()

    for i in forts_obj:
        DistMatrix_fort_lat_long.objects.create(
            matrix_fort_name = i.fort_name,
            matrix_fort_district = i.fort_district,
            matrix_fort_latitude = i.fort_latitude,
            matrix_fort_longitude = i.fort_longitude
        )


from django.http import JsonResponse
from django.db import connection

def keep_db_alive(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")  # Simple query to keep DB active
        return JsonResponse({"status": "success", "message": "Database is awake!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


    """
    Iterates through fort images, removes spaces from their filenames,
    renames the files on the filesystem, and updates the corresponding
    database records.
    """
    count = 0
    # Define the directory where images are stored
    image_dir = os.path.join(settings.MEDIA_ROOT, 'img', 'fort_images')

    for filename in os.listdir(image_dir):
        # Proceed only if there is a space in the filename
        if ' ' in filename:
            # --- 1. Prepare Paths and New Filename ---
            old_path = os.path.join(image_dir, filename)
            new_filename = filename.replace(' ', '')
            new_path = os.path.join(image_dir, new_filename)

            # --- 2. Rename the Physical File ---
            os.rename(old_path, new_path)

            # --- 3. Update the Database Record ---
            # Get the fort name from the original filename (before removing spaces)
            base_name, ext = os.path.splitext(filename)
            fort_obj = Forts.objects.filter(fort_name__icontains=base_name).first()
            
            if fort_obj:
                # Update the image field with the new filename path
                fort_obj.fort_image = f"img/fort_images/{new_filename}"
                fort_obj.save()
                count += 1
                
    print(f"Successfully updated and renamed {count} files.")