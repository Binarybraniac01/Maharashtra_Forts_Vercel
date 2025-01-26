from django.shortcuts import render

from .models import *
from home.models import *
from user.models import *

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


import random
from datetime import datetime

#other imports
import urllib3
import json
import requests
import time
import datetime
import math
import os


@login_required(login_url="/login-page/")
def ourplans(request):
    active2 = "active"

    planned_trips = all_trips.objects.filter(user=request.user).order_by('-trip_id')
    
    if not planned_trips:
        return render(request, "not_enough_data.html", context={"active2":active2})
    else:
        # To Add pagination in table
        paginator = Paginator(planned_trips, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    
    ############################ For Randomized Recommendations #########################################
    # # Add below code block if you want to 1 day limit to recom data creation for user
    # # check for the date constraints so that same day you dont make double recom for same user
    # date_check = all_recommendations.objects.filter(user=request.user).first()
    # if date_check is not None:
    #     first_date_obj = date_check.date
    #     current_date = datetime.now().date() # Convert the date string to a datetime object
    #     if first_date_obj != current_date:
    #         all_recommendations.objects.filter(user=request.user).delete()  
    #     else:
    #         print("dates Matched") 

    # Make sure the previous records are deleted and then procced to execution
    # Below block add new recom each time user visits the end point
    all_recommendations.objects.filter(user=request.user).delete()
    data_availability = all_recommendations.objects.filter(user=request.user).first()
    if data_availability is None:
            # Retrieve unique trip districts using Django's ORM
            planned_trips_dist = list(
                all_trips.objects.filter(user=request.user)
                      .values_list('trip_district', flat=True)
                    .distinct()
            )
            # print(planned_trips_dist)

            random_dist = random.sample(planned_trips_dist, min(5, len(planned_trips_dist)))
            recommend_dist_fort = []
            # Loop either 5 times or the number of unique districts, whichever is smaller
            for a in random_dist:
                f_names = []
                district_forts = Forts.objects.filter(fort_district= a)
                for b in district_forts:
                    f_names.append(b.fort_name)

                if f_names:
                    fort_names = random.sample(f_names, min(random.randint(4, 8), len(f_names)))

                    recommend_dist_fort.append((a, fort_names))
            
            print(recommend_dist_fort)

            n = 1
            for i in recommend_dist_fort:

                district = i[0]
                fort_names = i[1]
                title = f"Explore More of {i[0]}"
                details =(
                            f"Enjoy the historic beauties of {i[0]} district with personalised forts suggested for you. "
                            "Each fort holds tales of Maratha valor and offers breathtaking views, scenic drives, and a unique piece of history. "
                            "Perfect for adventurers and history lovers, this journey brings Maharashtra’s rich heritage to life with every stop. "
                        )
                # To choose random element from list (fortname)
                img_name = random.choice(fort_names)
                img_obj = Forts.objects.filter(fort_name=img_name).first()
                recom_img = img_obj.fort_image
                n += 1 
                
                recommendation = all_recommendations.objects.create(
                    user = request.user,
                    recom_district = district,
                    recom_forts = fort_names,
                    recom_title = title,
                    recom_details = details,
                    image_name = recom_img
                )
                recommendation.save()

    tbl_data = all_recommendations.objects.filter(user=request.user)
    
    return render(request, "ourplans.html", context={"active2":active2, "planned_trips":planned_trips, "tbl_data":tbl_data, "page_obj":page_obj})


@login_required(login_url="/login-page/")
def recommdirection(request):
    active2 = "active"

    # To show all recommendations in slider
    tbl_data = all_recommendations.objects.filter(user= request.user)

    # Code for after clicking get directions
    recom_id = request.POST.get('rec_id')
    print(recom_id)

    direc_data = all_recommendations.objects.filter(recommendation_id=recom_id).first()
    print(direc_data)

    # for checking in html page
    found = "found"

    # getting fort names and id
    fort_string = direc_data.recom_forts
    forts_list = eval(fort_string) # fort_string contaions list as string eg. "[..data..] ", so converts it to list
    print(forts_list)

    fortsname =[]

    for i in forts_list:
        get_data = Forts.objects.filter(fort_name=i).first()
        fortsname.append((get_data.fort_id, get_data.fort_name)) # todo: Unable to get fort id or any data

    return render(request, "ourplans.html", context= {"active2":active2, "tbl_data":tbl_data, "direc_data":direc_data, "found":found, "fortsname":fortsname})



@login_required(login_url="/login-page/")
def recom_generateplan(request):

    try:
        triggerplan = "none"
        found = "none"
        ltlg = "none"
        fort_sel = "none"

        if request.method == "POST":

            # To show all recommendations in slider
            tbl_data = all_recommendations.objects.filter(user= request.user)

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

                return render(request, "ourplans.html", context= {"active2":"active", "ltlg":ltlg, "fort_sel":fort_sel, "tbl_data":tbl_data})


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
                        data.append((org, dis))   # look here for get directions  # changed here 
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
                    # Note the occurs here if the distance matrix does not get the locations
                    print(f"l_names_len: {len(l_names)}, d_t_val_len: {len(d_t_val)}, fuel_n_cost_len: {len(fuel_n_cost)}")
                    min_length = min(len(l_names), len(d_t_val), len(fuel_n_cost)) # add this and below line that 
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

                    return render(request, "ourplans.html", context= {"tbl_data":tbl_data, "triggerplan":triggerplan, "active2":"active", "ltlg":ltlg, "fort_sel":fort_sel, "info_box":info_box, "items":data, "total_travel_time":total_travel_time, "estimated_days":estimated_days, "fuel_n_cost":fuel_n_cost, "total_f_c":total_f_c})

                else:
                    print("no lt-lg")
                    ltlg = "nolocation"

                    return render(request, "ourplans.html", context= {"active2":"active", "ltlg":ltlg, "fort_sel":fort_sel, "tbl_data":tbl_data})

    except Exception as e:
        print(e)
        return render(request, "504.html")
    

