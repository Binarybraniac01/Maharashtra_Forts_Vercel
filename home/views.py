from django.shortcuts import render, redirect
from django.http import JsonResponse

# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from home.models import *
from user.models import *
from recommendations.models import all_trips


# other imports
import urllib3
import json
import requests
import time
import datetime
import math
import os
import sys



from django.http import JsonResponse

def search_api(request):

    if not request.user.is_authenticated:
            return redirect("/login-page/")
    
    query = request.GET.get('q', '')
    # Filtering items from  database
    if query:
        results = list(
            set(Forts.objects.filter(fort_district__icontains=query)
            .values_list('fort_district', flat=True)
            .distinct()[:10])  
        )

        """
        values_list() method is used to retrieve specific fields from a queryset, rather than retrieving the entire model instance.
        'fort_district': The field you want to include in the results.
        flat=True: This simplifies the output to a flat list rather than a list of tuples (default behavior).
        [:10] : gives first 10 entries
        (e.g., <QuerySet ['Raigad Fort', 'Pratapgad Fort']>).
        
        """

    else:
        results = []

    return JsonResponse({'results': results})





def home_view(request):

    active1 = "active"
    display = "none"
    found = "none"
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/login-page/")

        print(request.method)
        
        data = request.POST
        # Get user district name from the submited form
        user_district = data.get('user_district')
        print(user_district)

        # Get district_name from database
        fortsname = Forts.objects.filter(fort_district=user_district)
        if fortsname:
            # declaring district name for later use
            # global district_name
            # district_name = user_district

            # adding district of current user
            if request.user.is_authenticated:
                user_data, created = UserData.objects.get_or_create(user=request.user)
                user_data.user_district = user_district
                user_data.curr_lat = 0.0
                user_data.curr_log = 0.0
                user_data.save()

            # variable for showing container or simple text
            found = "found"
            display = "block"

            # Rendering Template if district name is found
            return render(request, "index.html", context = {"display":display, "active1":active1, "fortsname":fortsname,
                                   "found":found, "user_district":user_district})

        else:
            # if wrong district name is entered !!!
            print("District not found !!!")
            found = "nodata"
            return render(request, "index.html", context= {"display":display, "active1":active1, "found":found})


    # This will load the index file at start , when no entry is entered
    return render(request, "index.html", context= {"display":display, "active1":active1, "found":found})



@login_required(login_url="/login-page/")
def send_coordinates(request):
    if request.method == "POST":

        usr_latitude = request.POST.get("latitude")
        usr_longitude = request.POST.get("longitude")
        print(usr_latitude)
        print(usr_longitude)

        # deleting database data if already existed
        latitude_longitude.objects.filter(user= request.user).delete()

        # Inserting user location to database
        user_lat_long = latitude_longitude.objects.create(user=request.user, origin_latitude=usr_latitude, origin_longitude=usr_longitude)
        user_lat_long.save()
        print("Co-ordinated recieved")

        # Deleting user locations table
        # user_location.objects.all().delete()
        # new_user_lat_long = user_location.objects.create(user_latitude=usr_latitude, user_longitude=usr_longitude)
        # new_user_lat_long.save()

        # adding data in Userdata table
        user_data = UserData.objects.get(user=request.user)
        user_data.curr_lat = usr_latitude
        user_data.curr_log = usr_longitude
        user_data.save()

        # deleting route table data
        Route.objects.filter(user= request.user).delete()
        print("deleted route table vales ")

        # deleting result table data
        Result.objects.filter(user= request.user).delete()
        print("deleted result table vales ")

        data = {"success_msg": "Coordinates recieved successfully!"} # json response need data argument for the our data to load

        return JsonResponse(data= data, safe=False) # safe to be false is need for django to serialize the data 



@login_required(login_url="/login-page/")
def generateplan(request):
    # Integrated below block of code here to avoid wirting same function again in recommendations 
    # if 'recommgenerateplan' in request.path:
    #     template_name = "ourplans.html" # Todo: Errors are showing on index page fix that
    #     active_tab = "active2"
    # else:
    #     # Use a default template 
    #     template_name = "index.html"
    #     active_tab = "active1"
    #------------------End-----------------#
    try: 
        triggerplan = "none"
        found = "none"
        ltlg = "none"
        fort_sel = "none"
        if request.method == "POST":

            formdata = request.POST
            milage = formdata.get('milage')
            p_liter = formdata.get('p_liter')

            print(f"Method {request.method} of generate plan")
            # print(f"Got user district {district_name}")            # Getting access of user district

            selected_forts = formdata.getlist('selected_checkbox')
            print("This is selected forts", selected_forts)
            if not selected_forts:
                fort_sel = "none"
                print("fort none")

                abcd = UserData.objects.get(user= request.user)
                if abcd.curr_lat == 0.0:
                    print("no lt-lg")
                    ltlg = "nolocation"

                return render(request, "index.html", context= {"active1":"active", "ltlg":ltlg, "fort_sel":fort_sel})


            else:
                fort_sel = "selected"

                # added another table containing user location ()

                user_lat_long = UserData.objects.get(user=request.user)

                if user_lat_long is not None and user_lat_long.curr_lat != 0.0 :
                    user_lat = user_lat_long.curr_lat
                    user_long = user_lat_long.curr_log

                    # deleting user loaction table
                    # user_location.objects.all().delete()
                    # print("deleted  user location table vales in user location table ")
                    print(f"User location : user_lt: {user_lat} user_lg: {user_long}")


                    # -----------------------------------------------------------------------------------------------------------------------
                    # Adding function for getting best path to visit various destinations
                    path_id_name = []
                    plan_sorted_locatons = []

                    def optimal_path():
                        URL = "https://api.routific.com/v1/vrp"

                        visits = {}
                        fleet = {}

                        temp_fleet = {
                            "vehicle_1": {
                                "start_location": {
                                    "id": "depot",
                                    "name": "Your Location",
                                    "lat": user_lat,
                                    "lng": user_long
                                }
                            }
                        }

                        fleet.update(temp_fleet)

                        for i in selected_forts:
                            # print(i)
                            user_sel_fort = Forts.objects.filter(fort_id=i).first()

                            user_sel_fort_lat = user_sel_fort.fort_latitude
                            user_sel_fort_long = user_sel_fort.fort_longitude
                            user_sel_fort_id = user_sel_fort.fort_id
                            user_sel_fort_name = user_sel_fort.fort_name

                            # converting key string
                            id = str(user_sel_fort_id)

                            temp_visits = {
                                id: {
                                    "location": {
                                        "name": user_sel_fort_name,
                                        "lat": user_sel_fort_lat,
                                        "lng": user_sel_fort_long
                                    }
                                }
                            }

                            visits.update(temp_visits)

                        # Prepare data payload
                        data = {
                            "visits": visits,
                            "fleet": fleet
                        }

                        # Put together request
                        # This is your demo token
                        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzdhZDQwZjRmZjE0MWYwMGQ3NGIyYmMiLCJpYXQiOjE3MzYxMDI5Mjd9.QqnUFDWkIoBuaD9GmGVJuViqxCuAun78iwTFysVTDWg'

                        http = urllib3.PoolManager()
                        req = http.request('POST', URL, body=json.dumps(data),
                                        headers={'Content-Type': 'application/json', 'Authorization': "bearer " + token})

                        # Get route
                        res = json.loads(req.data.decode('utf-8'))


                        # Extracting location_id and location_name pairs
                        locations = {}
                        for vehicle, visits in res['solution'].items():
                            for visit in visits:
                                locations[visit['location_id']] = visit['location_name']

                        # Printing location_id and location_name pairs
                        for location_id, location_name in locations.items():
                            path_id_name.append((location_id, location_name))
                            plan_sorted_locatons.append(location_name)
                            print(f"Location ID: {location_id}, Location Name: {location_name}")

                    # calling Function for path finding
                    optimal_path()

                    # ---------------------------------------------------------------------------
                    # adding values to database
                    global count
                    global old_value
                    count = 0
                    old_value = ""

                    for new_id, name in path_id_name:
                        if new_id == "depot":
                            # print(new_id)
                            print("got user location ")
                        else:
                            # print(new_id)
                            print("got plan functionality")
                            user_sel_fort1 = Forts.objects.filter(fort_id=new_id).first()
                            user_sel_fort_lat1 = user_sel_fort1.fort_latitude
                            user_sel_fort_long1 = user_sel_fort1.fort_longitude

                            # for updating lt/lg in database for planning tour

                            user_g_lat_long1 = latitude_longitude.objects.filter(user=request.user).first()
                            if user_g_lat_long1 is not None and count == 0:
                                user_g_lat_long1.destination_latitude = user_sel_fort_lat1
                                user_g_lat_long1.destination_longitude = user_sel_fort_long1
                                user_g_lat_long1.save()

                                new_user_lat_long1 = latitude_longitude.objects.create(user=request.user, origin_latitude=user_sel_fort_lat1,
                                                                        origin_longitude=user_sel_fort_long1)
                                new_user_lat_long1.save()

                                old_value = str(user_sel_fort_lat1)
                                count = count + 1
                                print(f"Plan {count} Uploaded to database")

                            else:
                                new_plan = latitude_longitude.objects.filter(origin_latitude=old_value).first()
                                new_plan.destination_latitude = user_sel_fort_lat1
                                new_plan.destination_longitude = user_sel_fort_long1
                                new_plan.save()

                                new_plan_lat_long = latitude_longitude.objects.create(user=request.user, origin_latitude=user_sel_fort_lat1,
                                                                    origin_longitude=user_sel_fort_long1)
                                new_plan_lat_long.save()

                                old_value = str(user_sel_fort_lat1)
                                count = count + 1
                                print(f"New plan {count} Uploaded to database")

                    # -----------------------------------------------------------------------------------------------------------------------
                    # Using distance matrix api

                    # filling values in th table to be used in function
                    # filling values in the table to be used in the function
                    table_fill = latitude_longitude.objects.filter(user=request.user)
                    print(table_fill)

                    for row in table_fill:
                        o_lt, o_lg, d_lt, d_lg = row.origin_latitude, row.origin_longitude, row.destination_latitude, row.destination_longitude
                        if d_lt is not None and d_lg is not None:
                            o_lt_lg = f"{o_lt},{o_lg}"
                            d_lt_lg = f"{d_lt},{d_lg}"

                            fill_data = Route.objects.create(user=request.user, origin=o_lt_lg, destination=d_lt_lg, mode="driving",
                                            traffic_model="best_guess",
                                            departure_time="now")
                            fill_data.save()

                    # Commit once after all the additions
                    # db.session.commit()

                    # ------------------------------------------------------#
                    # main function to calculate distance
                    BASE_URL = "https://api.distancematrix.ai"

                    API_KEY = 'XAApAsen6SsKxTH0GPHUSVACCzRpHCYdgg9pKuVETQiuTRWvmVnU2iMjEiEVMRvi' 
                    #h7umDGRk3n0JI4RA1Zm1fkFRFnp1sFiEUYAysjrURSuPBZpZh2Db4gMPSHLTSUdc#
                    # Loading data from database
                    def load_data():
                        count_rows = 0
                        data = []

                        # Query data from the Route table
                        routes = Route.objects.filter(user=request.user)

                        for route in routes:
                            origin = route.origin
                            destination = route.destination
                            mode = route.mode
                            traffic_model = route.traffic_model
                            departure_time = route.departure_time

                            data.append({
                                "origin": "%s" % origin.replace('&', ' '),
                                "destination": "%s" % destination.replace('&', ' '),
                                "mode": "%s" % mode.replace('&', ' '),
                                "traffic_model": "%s" % traffic_model.replace('&', ' '),
                                "departure_time": "%s" % departure_time.replace('&', ' ')
                            })
                            count_rows += 1

                        print(" \nTotal rows in the database = %s \n" % (count_rows))
                        return data

                    # craeting a request
                    def make_request(base_url, api_key, origin, destination, mode, traffic_model, departure_time):
                        url = "{base_url}/maps/api/distancematrix/json" \
                            "?key={api_key}" \
                            "&origins={origin}" \
                            "&destinations={destination}" \
                            "&mode={mode}" \
                            "&traffic_model={traffic_model}" \
                            "&departure_time={departure_time}".format(base_url=base_url,
                                                                        api_key=api_key,
                                                                        origin=origin,
                                                                        destination=destination,
                                                                        mode=mode,
                                                                        traffic_model=traffic_model,
                                                                        departure_time=departure_time)
                        # logging.info("URL: %s" % url)
                        result = requests.get(url)
                        return result.json()

                    def main():
                        data = load_data()
                        n = 0
                        for t in data:
                            time.sleep(0)
                            # request_time = datetime.datetime.now()
                            dm_res = make_request(BASE_URL, API_KEY, t['origin'], t['destination'], t['mode'],
                                                t['traffic_model'],
                                                t['departure_time'])

                            if dm_res['status'] == 'REQUEST_DENIED':
                                if dm_res['error_message'] == 'The provided API key is invalid or token limit exceeded.':
                                    print(dm_res['error_message'])
                                    break
                            n += 1
                            try:
                                dm_distance = dm_res['rows'][0]['elements'][0]['distance']
                                dm_duration = dm_res['rows'][0]['elements'][0]['duration']
                                dm_duration_in_traffic = dm_res['rows'][0]['elements'][0]['duration_in_traffic']
                                origin_addresses = dm_res['origin_addresses']
                                destination_addresses = dm_res['destination_addresses']

                            except Exception as exc:
                                print("%s) Please check if the address or coordinates in this line are correct" % n)
                                # continue
                                print(t['destination'], "is faulty")
                                raise
                                # If the you dont see print then just look at how many rows are added to database
                                # the print statement is not printing bcoz of raise
                                

                            result = Result.objects.create(
                                user = request.user,
                                # request_time=request_time,
                                origin=t['origin'],
                                destination=t['destination'],
                                origin_addresses=origin_addresses,
                                destination_addresses=destination_addresses,
                                mode=t['mode'],
                                traffic_model=t['traffic_model'],
                                departure_time=t['departure_time'],
                                distance_value=dm_distance['value'],
                                distance_text=dm_distance['text'],
                                duration_value=dm_duration['value'],
                                duration_text=dm_duration['text'],
                                duration_in_traffic_value=dm_duration_in_traffic['value'],
                                duration_in_traffic_text=dm_duration_in_traffic['text']
                            )
                            result.save()

                    # calling function
                    main()


                    # ----------------------------------------------------------------------------------------------------------#
                    # Adding values to box container
                    global info_box
                    global data
                    info_box = []
                    l_names = []
                    d_t_val = []

                    # list containing  sorted loc coordinates for direction
                    data = []
                    # for temp total time
                    total = []

                    # ---- used for getting distance value separated for using it in fuel cost function ----#
                    d_val = []
                    # - end -#

                    # filling sorted location names and there values for loopng to work
                    for name in range(len(plan_sorted_locatons) - 1):
                        l_names.append((plan_sorted_locatons[name], plan_sorted_locatons[name + 1]))

                    plan_box = Result.objects.filter(user=request.user)
                    for dt in plan_box:
                        org = dt.origin
                        dis = dt.destination
                        dist = dt.distance_text
                        t_time = dt.duration_in_traffic_text
                        d_t_val.append((dist, t_time))
                        data.append((org, dis))   # look here for get directions
                        total.append(t_time)
                        d_val.append(dist)

                    print("this is data in data :", data)
                    # -------------------------------------------------------------#
                    # For showing Fuel required and cost for trip

                    fuel_n_cost = []
                    total_f_c = []
                    t_f = 0
                    t_c = 0

                    # Define average fuel efficiency for petrol cars in India
                    # milage = request.form['milage']
                    # p_liter = request.form['liter']

                    if milage :
                        AVERAGE_MILEAGE = int(milage)
                    else:
                        AVERAGE_MILEAGE = 20  # kilometers per liter

                    if p_liter:
                        price_per_liter = int(p_liter)
                    else:
                        price_per_liter = 104.89  # price per liter


                    for d in d_val:
                        # d = "25.7 km"
                        # Split the string to isolate the numeric part
                        numerical_value = d.split()[0]
                        distance = float(numerical_value)

                        def calculate_petrol_cost(distance, price_per_liter):
                            # Calculate required petrol in liters
                            required_petrol = distance / AVERAGE_MILEAGE

                            # Calculate total cost
                            cost = required_petrol * price_per_liter

                            return required_petrol, cost

                        # Calculate and display results
                        required_petrol, total_cost = calculate_petrol_cost(distance, price_per_liter)

                        # for getting total
                        t_f = t_f + required_petrol
                        t_c = t_c + total_cost


                        fuel = f"Required Fuel: {required_petrol:.2f} liters"
                        cost = f"Travel cost: ₹{total_cost:.2f}"
                        fuel_n_cost.append((fuel, cost))

                    print(fuel_n_cost)

                    # for getting total values in list
                    total_f_c.append(round(t_f, 2))
                    total_f_c.append(round(t_c, 2))

                    print(f"This is list for total f and c : {total_f_c}")

                    # appending all in one list
                    print(f"l_names_len: {len(l_names)}, d_t_val_len: {len(d_t_val)}, fuel_n_cost_len: {len(fuel_n_cost)}")
                    min_length = min(len(l_names), len(d_t_val), len(fuel_n_cost))
                    for i in range(min_length):
                    #for i in range(len(l_names)): 
                        location_info = l_names[i]
                        distance_info = d_t_val[i]
                        fuel_and_cost = fuel_n_cost[i]
                        info_box.append((*location_info, *distance_info, *fuel_and_cost))
                    print(info_box)

                    #-------------------------------------------------------------------------------------------------------#
                    # for getting values in all_trips table
                    raw_data = []
                    if len(info_box) > 1:
                        for tuple_data in info_box[1:]:
                            first_string = tuple_data[0]
                            second_string = tuple_data[1]
                            last_string = tuple_data[-1]
                            raw_data.append((first_string, second_string, last_string))
                    else:
                        raw_data.append((info_box[0][1], info_box[0][-1]))
                    # print(raw_data)
                    # print(len(raw_data))

                    fort_names = []
                    cost = []


                    if len(raw_data) == 1:
                        if len(raw_data[0]) == 3:
                            # Get first and second string of the first tuple
                            fort_names.append(raw_data[0][0])
                            fort_names.append(raw_data[0][1])

                            # Extract travel cost values and calculate total cost
                            for _, _, travel_cost in raw_data:
                                cost.append(float(travel_cost.split('₹')[-1]))

                            total_cost = sum(cost)

                        else:
                            fort_names.append(raw_data[0][0])
                            # Extract travel cost values and calculate total cost
                            for _, travel_cost in raw_data:
                                cost.append(float(travel_cost.split('₹')[-1]))

                            total_cost = sum(cost)

                    else:
                        # Get first and second string of the first tuple
                        fort_names.append(raw_data[0][0])
                        fort_names.append(raw_data[0][1])

                        # Get second string of each tuple from the second tuple onwards
                        for i in range(1, len(raw_data)):
                            fort_names.append(raw_data[i][1])

                        # Extract travel cost values and calculate total cost
                        for _, _, travel_cost in raw_data:
                            cost.append(float(travel_cost.split('₹')[-1]))

                        total_cost = sum(cost)

                    # -----------------------------------------------------------------------------------------#
                    # Getting total time for showing user
                    # Aceesing total list which stores all times

                    print(total)
                    # total = ['50 mins', '2 hour 14 mins']

                    # Initialize variables to store total hours and minutes
                    total_hours = 0
                    total_minutes = 0

                    # Iterate through each travel time
                    for time_str in total:
                        # Split the string to extract hours and minutes
                        time_parts = time_str.split()

                        # Convert hours and minutes to integers
                        hours = 0
                        minutes = 0
                        if 'hour' in time_parts:
                            hours = int(time_parts[0])
                        if 'mins' in time_parts:
                            minutes = int(time_parts[time_parts.index('mins') - 1])

                        # Update total hours and minutes
                        total_hours += hours
                        total_minutes += minutes

                    # Adjust total hours and minutes
                    total_hours += total_minutes // 60
                    total_minutes = total_minutes % 60

                    # Format the total travel time
                    total_travel_time = f"{total_hours} hour {total_minutes} mins"
                    print("Total Travel Time:", total_travel_time)

                    def calculate_estimated_days(total_travel_time, overnight_break_duration_range=(8, 13)):

                        # Extract travel time in hours
                        hours = int(total_travel_time.split()[0])

                        # Check if trip can be completed in one day (considering lower bound of overnight break range)
                        if hours <= overnight_break_duration_range[0]:
                            return 1

                        # Calculate estimated days based on lower bound of overnight break range
                        estimated_days = math.ceil(hours / overnight_break_duration_range[0])

                        return estimated_days

                    estimated_days = calculate_estimated_days(total_travel_time)
                    print(f"Estimated days required for the trip: {estimated_days}")
                    #----------------------End-----------------------------#


                    # let see we can acces all fields required for all_trips

                    if estimated_days < 2:
                        req_time = f"1 day"
                    else:
                        req_time = f"{estimated_days} days"

                    # Converting list to string for database
                    forts_visited_string = ','.join(fort_names)
                    #Getting current Date
                    current_date = datetime.datetime.now().date()
                    # print(current_date)

                    
                    user_data = UserData.objects.get(user=request.user)
                    district_name = user_data.user_district
                    user = request.user

                    trip_data = all_trips.objects.create(user=user, user_name=str(user), trip_district=district_name, forts_visited=forts_visited_string, required_time=req_time, minimum_cost=total_cost, date=current_date)
                    trip_data.save()

                    triggerplan = "trigger"
                    ltlg = "none"

                    return render(request, "index.html", context= {"triggerplan":triggerplan, "active1":"active", "ltlg":ltlg, "fort_sel":fort_sel, "info_box":info_box, "items":data, "total_travel_time":total_travel_time, "estimated_days":estimated_days, "fuel_n_cost":fuel_n_cost, "total_f_c":total_f_c})

                else:
                    print("no lt-lg")
                    ltlg = "nolocation"

                    return render(request, "index.html", context= {"active1":"active", "ltlg":ltlg, "fort_sel":fort_sel})

    except Exception as e:
        print(e)
        return render(request, "504.html")
