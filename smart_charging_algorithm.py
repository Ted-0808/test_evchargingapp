#this is a comment
import random
from copy import deepcopy

Norminal_Power_CP = 11  # max charging power of the CP
charging_Request = []
flexibility_to_offer = []
Power_Supply = 33
charging_Pool = []
charging_list = []
charging_list_n =[]
flexibility_record =[]
charging_electricity_total =0
current_power = 0
SIM_TIME = 600      # start for 10 hours simulation
TIME_STEP = 15     # time interval as 15 mins
num_acc = 0
num_rej = 0

# generate random charging requests for the whole simulation
for i in range (100):
    id_n = i
    energy_needed = random.randint(10,40)
    charging_time_n = energy_needed/Norminal_Power_CP* 60
    charging_time = random.randint(1,12)*15
    if energy_needed/ (charging_time/60) <=  Norminal_Power_CP:
        charging_Request.append([id_n, energy_needed,charging_time,charging_time_n])

for i in range(len(charging_Request)):
    flexibility = charging_Request[i][2]-(charging_Request[i][1]/Norminal_Power_CP)*60
    if (flexibility >= 15) :
        flexibility_next = Norminal_Power_CP
    else:
        flexibility_next = flexibility * Norminal_Power_CP/15
    flexibility_to_offer.append([flexibility,flexibility_next])

# step 0: push a new charging request to the charging pool for next step calculation
charging_event_0 = {"id": charging_Request[0][0],"E":charging_Request[0][1], "E_rec":charging_Request[0][1],"T":charging_Request[0][2], "F_t": flexibility_to_offer[0][0],"F_p":flexibility_to_offer[0][1],"flex_rec":0,"Y/N": 1, "End":0}
charging_event_0_n = {"id": charging_Request[0][0],"E":charging_Request[0][1], "E_rec":charging_Request[0][1],"T":charging_Request[0][3], "F_t": flexibility_to_offer[0][0],"F_p":flexibility_to_offer[0][1],"flex_rec":0,"Y/N": 1, "End":0}
charging_list.append(charging_event_0)
charging_list_n.append(charging_event_0_n)

## normal charging
num_acc_n = 0
num_rej_n = 0
charging_finished =[]
n = 0
total_electricity = 0
for item in range( 0, SIM_TIME, TIME_STEP):
    print("simulation at %d mins" % item)
    num_charging = 0

#    print(len(charging_list_n))
    i = 0
    while i < len(charging_list_n):
        print("simulation runs")
        if charging_list_n[i]["T"] ==0:
            charging_finished.append(charging_list_n[i]["id"])
            charging_list_n.pop(i)
            i -=1

        elif charging_list_n[i]["T"] <=15:
            charging_list_n[i]["T"] = 0
            charging_list_n[i]["E"] = 0

        else:
            charging_list_n[i]["T"] -=15
            charging_list_n[i]["E"] -= Norminal_Power_CP*(0.25)
            num_charging +=1

        i +=1

    n = n + 1

    if (n< len(charging_Request)):
        new_charging_event_n = {"id":charging_Request[n][0],"E":charging_Request[n][1], "T":charging_Request[n][3], "F_t": flexibility_to_offer[n][0],"F_p":flexibility_to_offer[n][1],"flex_rec":0,"Y/N": 1,"End":0}
        print ("New charging event arrives")

        if num_charging < (Power_Supply/ Norminal_Power_CP):
            print ("New charging event accept EV %d"% charging_Request[n][0])
            charging_list_n.append(new_charging_event_n)
            num_acc_n +=1
        else:
            print("New charging event rejected")
            num_rej_n +=1






# smart charging case
# the time resolution is in minute

simutaneity = 0
n = 0

for T in range(0,SIM_TIME, TIME_STEP):       ###this is where loop for every timestep (real loop)###
    print ("simulation time is %d minutes" %T)

    ongoing_charging = len(charging_list)
    no_flex_offer = 0
    power_supply = 33 # initial value for every loop
    flex_supply = 0 # aggregate flex_offer
    flex_demand = 0 # total overload
    flex_offer = 0
    flex_group1 = 0
    finished_list =[]

    if simutaneity >= len(charging_list):
        pass
    else:
        simutaneity = len(charging_list)

    item = 0
    while (item <len(charging_list)):
        if charging_list[item]["T"] == 0 or charging_list[item]["E"] <= 0:
            flexibility_record.append([charging_list[item]["id"],charging_list[item]["E_rec"],charging_list[item]["flex_rec"]]) #record all flexibility contribution for finished charging events
            print("Charging finished")
            charging_list.pop(item)
            item-=1
        item +=1




    for i in range(len(charging_list)):
        charging_list[i]["F_t"] = charging_list[i]["T"] - (charging_list[i]["E"]/Norminal_Power_CP*60)
        if charging_list[i]["F_t"]>= 15:
            charging_list[i]["F_p"] = Norminal_Power_CP
        else:
            charging_list[i]["F_p"] = charging_list[i]["F_t"]*Norminal_Power_CP/15

    for i in range(len(charging_list)):

        if charging_list[i]["T"] ==15:     #although for such case thses is no flecxibility, but we already deduct the needed power from the total supplyb
            required_charging_power = 4*charging_list[i]["E"]
            charging_list[i]["Y/N"] = 10  # 10 means last step case
            power_supply -= required_charging_power

        elif charging_list[i]["F_t"]<=1:
            charging_list[i]["Y/N"] = 0  # 0 means no flexibility
            no_flex_offer +=1
        elif charging_list[i]["F_p"] == Norminal_Power_CP:
            flex_group1 +=1
            flex_offer += 1
        else:
            flex_offer += 1

    flex_demand = (no_flex_offer + flex_offer)*Norminal_Power_CP - power_supply
    group1_sum = flex_group1 * Norminal_Power_CP

    for i in range(len(charging_list)):
        if charging_list[i]["Y/N"] ==1:
            flex_supply += charging_list[i]["F_p"]
        else:
            continue;
             ##all charging events are processed & get updated
    if flex_demand < 0:

        for i in range(len(charging_list)):
            charging_list[i]["T"] -= 15
            if charging_list[i]["T"] ==0:
                charging_list[i]["E"] =0
            else:
                charging_list[i]["E"] -= (0.25)*Norminal_Power_CP

    elif flex_demand <= group1_sum:
#            print ("charging accepted! ")
        ##all charging event get updated
        for i in range (len(charging_list)):
            charging_list[i]["T"] -= 15
            if charging_list[i]["T"] == 0:   #last step charging
                charging_list[i]["E"] =0
            elif charging_list[i]["F_p"] != Norminal_Power_CP:    #group2 & no flexibility charging
                charging_list[i]["E"] -= (0.25)*Norminal_Power_CP
            else:                            #group1 charging
                charging_list[i]["E"] -= (1 - flex_demand / group1_sum) * Norminal_Power_CP *(0.25)
                charging_list[i]["flex_rec"] += flex_demand / group1_sum * Norminal_Power_CP *(0.25) # flex allocation

    else:  # flexibility_demand <= flexibility_supply:
         for i in range (len(charging_list)):
            charging_list[i]["T"] -= 15
            if charging_list[i]["T"] == 0:   #last step charging
                charging_list[i]["E"] = 0
            elif charging_list[i]["F_p"] == Norminal_Power_CP:   # group1 &
                charging_list[i]["flex_rec"] += Norminal_Power_CP   # flex allocation
                continue  #no energy reduction
            elif charging_list[i]["Y/N"] ==0:     #charging events with no flexibility
                charging_list[i]["E"] -= (0.25)*Norminal_Power_CP
            else:                                #group2 charging
                charging_list[i]["E"] -= (0.25)*(Norminal_Power_CP - ((flex_demand - group1_sum)/(flex_supply - group1_sum) * charging_list[i]["F_p"]))
                charging_list[i]["flex_rec"] +=((flex_demand - group1_sum)/(flex_supply - group1_sum) * charging_list[i]["F_p"])* 0.25



# step 1: add one more charging request, and evaluate if it can be accepted
#if (Power_Supply_Max - current_power) >= Norminal_Power_CP:
    charging_Pool= deepcopy(charging_list)

    n = n + 1
    if (n< len(charging_Request)):
        new_charging_event = {"id":charging_Request[n][0],"E":charging_Request[n][1],"E_rec":charging_Request[n][1], "T":charging_Request[n][2], "F_t": flexibility_to_offer[n][0],"F_p":flexibility_to_offer[n][1],"flex_rec":0,"Y/N": 1,"End":0}
        charging_Pool.append(new_charging_event)
        print ("New charging event arrives")

        t = 0
        #####################################################
        while True:   ## this is where evaluation for certain charging request begins (evaluation loop)##
            #step 2: pick out all charging events in the last time step, and make corresponding modification
            count_last_step = 0
            power_supply_s =  30
            no_flexibility = 0
            flexibility_charging = 0
            num_group1 = 0
            flexibility_demand = 0
            flexibility_supply = 0
            t = t+ 1
            considered_charging = len(charging_Pool)
            print("the simulation %d loop" %t)
            drop_list =[]

            i = 0
            while (i<len(charging_Pool)):

                if charging_Pool[i]["T"] == 0 or charging_Pool[i]["E"] <= 0:
                    charging_Pool[i]["End"] =1
                    charging_Pool.pop(i)
                    print("simulation: Charging finished")
                i+=1

            # update all flexibility offer of charging pool
            for i in range(len(charging_Pool)):
                charging_Pool[i]["F_t"] = charging_Pool[i]["T"] - (charging_Pool[i]["E"]/Norminal_Power_CP*60)
                if charging_Pool[i]["F_t"]>= 15:
                    charging_Pool[i]["F_p"] = Norminal_Power_CP
                else:
                    charging_Pool[i]["F_p"] = charging_Pool[i]["F_t"]*Norminal_Power_CP/15


            for i in range(len(charging_Pool)):

                if charging_Pool[i]["T"] ==15:
                    required_charging_power = 4*charging_Pool[i]["E"]

                    charging_Pool[i]["Y/N"] = 10
                    power_supply_s -= required_charging_power
                    count_last_step +=1
                elif charging_Pool[i]["F_t"]<=1:
                    charging_Pool[i]["Y/N"] = 0
                    no_flexibility +=1
                elif charging_Pool[i]["F_p"] == Norminal_Power_CP:
                    num_group1 +=1
                    flexibility_charging += 1
                else:
    #                active_charging_events.append(charging_Pool[i])
                    flexibility_charging += 1

            # step 3: calculate flexibility demand, if less than 0, accept the new charging request; if larger than 0, follow step 4 and onwards.
            flexibility_demand = (no_flexibility + flexibility_charging)*Norminal_Power_CP - power_supply_s
            first_sum = num_group1 * Norminal_Power_CP

            for i in range(len(charging_Pool)):
                    if charging_Pool[i]["Y/N"] ==1:
                        flexibility_supply += charging_Pool[i]["F_p"]
                    else:
                        continue;

            if flexibility_demand < 0:
                charging_list.append(new_charging_event)
                num_acc +=1
                print ("simulation: charging accepted! ")
                break

            elif flexibility_demand <= first_sum:
    #            print ("charging accepted! ")
                ##all charging event get updated
                for i in range (len(charging_Pool)):
                    charging_Pool[i]["T"] -= 15
                    if charging_Pool[i]["T"] == 0:   #last step charging
                        continue
                    elif charging_Pool[i]["F_p"] != Norminal_Power_CP:    #group2 & no flexibility charging
                        charging_Pool[i]["E"] -= (0.25)*Norminal_Power_CP
                    else:                            #group1 charging
                        charging_Pool[i]["E"] -= (1 - flexibility_demand / first_sum) * Norminal_Power_CP *(0.25)

            elif flexibility_demand <= flexibility_supply:
                 for i in range (len(charging_Pool)):
                    charging_Pool[i]["T"] -= 15
                    if charging_Pool[i]["F_p"] == Norminal_Power_CP or charging_Pool[i]["T"] == 0:  # group1 & last step charging
                        continue  #no energy reduction
                    elif charging_Pool[i]["Y/N"] ==0:     #charging events with no flexibility
                        charging_Pool[i]["E"] -= (0.25)*Norminal_Power_CP
                    else:                                #group2 charging
                        charging_Pool[i]["E"] -= (0.25)*(Norminal_Power_CP - ((flexibility_demand - first_sum)/(flexibility_supply - first_sum) * charging_Pool[i]["F_p"]))
            else:
                print("simulation: charging rejected")
                charging_Pool.pop()
                num_rej +=1
                break


## comparison and conclusion
print("Simulation for %d hours " % (SIM_TIME/60), "with power limit at %d kW, " % Power_Supply )
for i in charging_finished:
    for j in range(len(charging_Request)):
        if i == charging_Request[j][0]:
            total_electricity += charging_Request[j][1]
print("with normal charging:")
print("total electricity: ",total_electricity)
print("accepted request: ", num_acc_n, "rejected request: ", num_rej_n)


total_electricity =0
total_flexibility =0

for i in range(len(flexibility_record)):
    total_electricity += flexibility_record[i][1]
    total_flexibility += flexibility_record[i][2]
print("With smart charging:")
print("total eletricity:", total_electricity, "   total flexibility: ", total_flexibility)
print("accepted request: ", num_acc, "rejected request: ", num_rej)
print("maximum charing events at the same time: ",simutaneity)
