import simpy as SIMP
import random
random.seed(10217240)
class Qstats:
    def __init__(self, show_full_output=True, trace_sample_path=False):
        # Doctor
        self.doc_resus_room_waiting_time = 0
        self.doc_no = 0
        self.doc_usage = 0
        self.doc_waiting_time = 0

        # Resus Room
        self.resus_room_no = 0
        self.resus_room_usage = 0
        self.resus_room_waiting_time = 0

        # Waiting room
        self.waiting_room_no = 0
        self.waiting_room_usage = 0

        # Beds
        self.beds_no = 0
        self.beds_usage = 0
        self.cat2_beds_waiting_time = 0
        self.cat3_beds_waiting_time = 0

        # Consult Time
        self.cat2_consult_time = 0
        self.cat3_consult_time = 0

        # Treatment Time
        self.cat2_treatment_time = 0
        self.cat3_treatment_time = 0

        # Other
        self.cat1_no_of_total_patients = 0
        self.cat2_no_of_total_patients = 0
        self.cat3_no_of_total_patients = 0
        self.no_of_total_patients = 0

        self.cat1_time = 0
        self.cat2_time = 0
        self.cat3_time = 0
        self.total_mins = 0
        self.total_hours = 0

        self.patients_diverted = 0

        self.stats_array = []

        # timestamps is a list of increasing length consisting of [t_start_stn1, t_end_stn1, t_start_stn2, t_depart]

    def notify_event(self, category, timestamps):

        if category == 1:
            self.doc_usage += timestamps[3] - timestamps[1]  # doc utilisation
            self.doc_resus_room_waiting_time += timestamps[1] - timestamps[0]  # wait time for doc
            self.resus_room_usage += timestamps[3] - timestamps[2]  # Resus Room utilisation
            self.resus_room_waiting_time += timestamps[2] - timestamps[1]  # wait time for resus room

            self.cat1_no_of_total_patients += 1  # patient throughput
            self.cat1_time += timestamps[3] - timestamps[0]  # time spent in system

        else:
            self.doc_usage += (timestamps[4] - timestamps[3]) + (timestamps[8] - timestamps[7])
            self.waiting_room_usage += timestamps[3] - timestamps[2]
            self.beds_usage += timestamps[8] - timestamps[2]
            if category == 2:
                self.cat2_beds_waiting_time += timestamps[3] - timestamps[2]
                self.cat2_consult_time += timestamps[4] - timestamps[3]
                self.cat2_treatment_time += timestamps[7] - timestamps[6]
                self.cat2_time += timestamps[8] - timestamps[0]
                self.cat2_no_of_total_patients += 1
            else:
                self.cat3_beds_waiting_time += timestamps[3] - timestamps[2]
                self.cat3_consult_time += timestamps[4] - timestamps[3]
                self.cat3_treatment_time += timestamps[7] - timestamps[6]
                self.cat3_time += timestamps[8] - timestamps[0]
                self.cat3_no_of_total_patients += 1

    def display_summary_stats(self, sim_end, doc_no, resus_room_no, beds_no, waiting_room_no):

        self.total_mins = sim_end
        self.no_of_total_patients = self.cat1_no_of_total_patients + self.cat2_no_of_total_patients \
                                    + self.cat3_no_of_total_patients

        #Performance measures

        print('Average time waiting for Doctor in mins (Category 1)  =', self.doc_resus_room_waiting_time /
              self.cat1_no_of_total_patients)
        print('Average time waiting for Resus Room in mins (Category 1)  =', self.resus_room_waiting_time /
              self.cat1_no_of_total_patients)
        print('Average throughput of patients (Category 1) = ', self.cat1_no_of_total_patients /
              self.no_of_total_patients)
        print('Average total length of stay in mins (Categroy 1) = ', self.cat1_time/ self.cat1_no_of_total_patients)

        print('Average time waiting for bed in mins (Category 2)  =', self.cat2_beds_waiting_time /
              self.cat2_no_of_total_patients)
        print('Average time waiting for consult in mins (Category 2)  =', self.cat2_consult_time /
              self.cat2_no_of_total_patients)
        print('Average time waiting for treatment in mins (Category 2)  =', self.cat2_treatment_time /
              self.cat2_no_of_total_patients)
        print('Average throughput of patients (Category 2) = ', self.cat2_no_of_total_patients /
              self.no_of_total_patients)
        print('Average total length of stay in mins (Categroy 2) = ', self.cat2_time / self.cat2_no_of_total_patients)

        print('Average time waiting for bed in mins (Category 3)  =', self.cat3_beds_waiting_time /
              self.cat3_no_of_total_patients)
        print('Average time waiting for consult in mins (Category 3)  =', self.cat3_consult_time /
              self.cat3_no_of_total_patients)
        print('Average time waiting for treatment in mins (Category 3)  =', self.cat3_treatment_time /
              self.cat3_no_of_total_patients)
        print('Average throughput of patients (Category 3) = ', self.cat3_no_of_total_patients /
              self.no_of_total_patients)
        print('Average total length of stay in mins (Categroy 3) = ', self.cat3_time / self.cat3_no_of_total_patients)

        print('Proportion of patients diverted =', self.patients_diverted)


        # Utilisation's
        print('Resus room utilisation =', self.resus_room_usage / (resus_room_no * self.total_mins))
        print('Bed utilisation =', self.beds_usage / (beds_no * self.total_mins))
        print('Doctor utilisation =', self.doc_usage / (doc_no * self.total_mins))
        print('Waiting room utilisation =', self.waiting_room_usage / (waiting_room_no * self.total_mins))

        self.stats_array = [ self.cat1_time/ self.cat1_no_of_total_patients, self.doc_resus_room_waiting_time /
              self.cat1_no_of_total_patients, self.resus_room_waiting_time /
              self.cat1_no_of_total_patients, self.cat1_no_of_total_patients /
              self.no_of_total_patients, self.cat2_time / self.cat2_no_of_total_patients,
              self.cat2_beds_waiting_time / self.cat2_no_of_total_patients, self.cat2_consult_time /
              self.cat2_no_of_total_patients, self.cat2_treatment_time /
              self.cat2_no_of_total_patients, self.cat2_no_of_total_patients /
              self.no_of_total_patients, self.cat3_time / self.cat3_no_of_total_patients,
              self.cat3_beds_waiting_time / self.cat3_no_of_total_patients,
              self.cat3_consult_time /self.cat3_no_of_total_patients, self.cat3_treatment_time /
              self.cat3_no_of_total_patients, self.cat3_no_of_total_patients /
              self.no_of_total_patients,  self.patients_diverted,
              self.resus_room_usage / (resus_room_no * self.total_mins), self.beds_usage / (beds_no * self.total_mins),
              self.doc_usage / (doc_no * self.total_mins), self.waiting_room_usage / (waiting_room_no * self.total_mins)]


class ED:

    def arrivals(env, cat, arrival_rate, doctors, resus_room, triage_nurse, beds, qstats):
        i = 0
        if cat == 1:
            while True:
                i += 1
                cat1_iat = random.expovariate(arrival_rate)

                # random.triangular(min, max, mode)
                resus_room_TO = random.triangular(30, 125, 70)
                timeouts = [resus_room_TO]

                yield env.timeout(cat1_iat)
                env.process(ED.patient(env,doctors, resus_room, triage_nurse, beds,  cat, timeouts, qstats))

        elif cat == 2:
            while True:
                i += 1
                cat2_iat = random.expovariate(arrival_rate)

                # random.triangular(min, max, mode)
                triage_TO = random.triangular(3, 5, 3.5)
                consultation_TO = random.triangular(8, 20, 15)
                observation_TO = random.triangular(20, 185, 40)
                treatment_TO = random.triangular(10, 30, 20)
                timeouts = [triage_TO, consultation_TO, observation_TO, treatment_TO]

                yield env.timeout(cat2_iat)
                env.process(ED.patient(env, doctors, resus_room, triage_nurse, beds, cat, timeouts, qstats))

        elif cat == 3:
            while True:
                i += 1
                cat3_iat = random.expovariate(arrival_rate)

                # random.triangular(min, max, mode)
                triage_TO = random.triangular(3, 5, 3.5)
                consultation_TO = random.triangular(8, 20, 15)
                observation_TO = random.triangular(20, 185, 40)
                treatment_TO = random.triangular(10, 30, 20)
                timeouts = [triage_TO, consultation_TO, observation_TO, treatment_TO]

                yield env.timeout(cat3_iat)
                env.process(ED.patient(env, doctors, resus_room, triage_nurse, beds, cat, timeouts, qstats))


    def patient(env, doctors, resus_room, triage_nurse, beds, cat, timeouts , qstats):

        if cat == 1:
            timestamps = [0, 0, 0, 0]
            doctors_requests = [doctors[i].request(cat) for i in range(len(doctors))]

            timestamps[0] = env.now
            doctors_available = yield env.any_of(doctors_requests)
            doctors_available_list = list(doctors_available.keys())
            for i in range(len(doctors)):
                if doctors_available_list[0] != doctors_requests[i]:
                    doctors_requests[i].cancel()
                    doctors[i].release(doctors_requests[i])
                else:
                    doc_id = i

            resus_room_request = resus_room.request()
            timestamps[1] = env.now
            yield resus_room_request

            timestamps[2] = env.now
            yield env.timeout(timeouts[0])

            doctors[doc_id].release(doctors_requests[doc_id])
            resus_room.release(resus_room_request)
            timestamps[3] = env.now
            qstats.notify_event(cat, timestamps)

        else:

            timestamps = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            while True:
                # Triage Nurse
                triage_request = triage_nurse.request()
                timestamps[0] = env.now
                yield triage_request
                timestamps[1] = env.now
                yield env.timeout(timeouts[0])

                triage_nurse.release(triage_request)
                # BEDS - if capacity is full, queue
                beds_request = beds.request(cat)
                if len(beds.queue) >= totals[4]:
                    print('Wait room full: Patient Diverted')
                    qstats.patients_diverted += 1
                    break
                timestamps[2] = env.now
                yield beds_request

                doctors_requests = [doctors[i].request(cat) for i in range(len(doctors))]
                timestamps[3] = env.now
                doctors_available = yield env.any_of(doctors_requests)
                doctors_available_list = list(doctors_available.keys())

                doc_id = 0
                for i in range(len(doctors)):
                    if doctors_available_list[0] != doctors_requests[i]:
                        doctors_requests[i].cancel()
                        doctors[i].release(doctors_requests[i])

                    else:
                        doc_id = i
                timestamps[4] = env.now
                yield env.timeout(timeouts[1])
                doctors[doc_id].release(doctors_requests[doc_id])
                timestamps[5] = env.now
                yield env.timeout(timeouts[2])

                repeat_request = doctors[doc_id].request(cat)
                timestamps[6] = env.now
                yield repeat_request
                timestamps[7] = env.now
                yield env.timeout(timeouts[3])
                doctors[doc_id].release(repeat_request)
                beds.release(beds_request)
                timestamps[8] = env.now
                qstats.notify_event(cat, timestamps)
                break


def simulation_run(arrival_rates, sim_end, totals, show_full_output):

    qstats = Qstats(show_full_output)
    env = SIMP.Environment()

    # RESOURCES
    # 5 resources including Doctors, Resuscitation Rooms, Triage Nurses, Beds
    doctors = [SIMP.PriorityResource(env, 1) for i in range(totals[0])]
    resus_room = SIMP.Resource(env, totals[1])
    triage_nurse = SIMP.Resource(env, totals[2])
    beds = SIMP.PriorityResource(env, totals[3])

    Category = [1, 2, 3]
    for i in range(3):
        env.process(
            ED.arrivals(env, Category[i], arrival_rates[i], doctors, resus_room, triage_nurse, beds,  qstats))

    env.run(until=sim_end)
    qstats.display_summary_stats(sim_end, totals[0], totals[1], totals[2], totals[4])
    return qstats


def simulation_reps(arrival_rates, sim_end, num_replications, totals, show_full_output):
    avg_stats_array = []
    repf = open('test.csv', 'w')
    repf.write('Avg time of stay Cat 1, Avg Doctor Waiting Time Cat 1, Avg Resus Waiting Time Cat 1, '
               + 'Avg throughput Cat 1, Avg time of stay Cat 2, Avg bed waiting time Cat 2, Avg consult waiting time Cat 2,'
               + 'Avg treatmnet time Cat 2, Avg throughput Cat 2, Avg time of stay Cat 3, Avg bed waiting time Cat 3,'
               + ' Avg consult waiting time Cat 3, Avg treatmnet time Cat 3, Avg throughput Cat 3, '
               + 'Proportion of patients diverted, resus room utilisations, bed utilisations,'
               + 'doctor utilisations, waiting room utilisations' + '\n')

    for rep in range(num_replications):
        print('*** REP', rep + 1, 'of', num_replications, '*****')
        qstats = simulation_run(arrival_rates, sim_end, totals,  show_full_output)
        for i in range(len(qstats.stats_array)):
            repf.write(str(qstats.stats_array[i]) + ',')
        repf.write( '\n')
        avg_stats_array.append(qstats.stats_array)

    repf.write('\n \n Average stats across all repetitions \n'
               + 'Avg time of stay Cat 1, Avg Doctor Waiting Time Cat 1, Avg Resus Waiting Time Cat 1, '
               + 'Avg throughput Cat 1, Avg time of stay Cat 2, Avg bed waiting time Cat 2, Avg consult waiting time Cat 2,'
               + 'Avg treatment time Cat 2, Avg throughput Cat 2, Avg time of stay Cat 3, Avg bed waiting time Cat 3,'
               + ' Avg consult waiting time Cat 3, Avg treatment time Cat 3, Avg throughput Cat 3, '
               + 'Proportion of patients diverted, resus room utilisation, bed utilisation,'
               + 'doctor utilisation, waiting room utilisation' + '\n')
    avg_stat = [0] * len(qstats.stats_array)
    for i in range(len(avg_stats_array)):
        for j in range(len(qstats.stats_array)):
            avg_stat[j] += avg_stats_array[i][j]

    for k in range(len(qstats.stats_array)):
        avg_stat[k] = avg_stat[k]/num_replications
    repf.write(str(avg_stat) + ',')
    repf.close()


# Main simulation and data settings

show_full_output = True
num_replications = 100
SIM_END = 6000

arrival_rate_CAT1 = 0.5/ 60
arrival_rate_CAT2 = 2 / 60
arrival_rate_CAT3 = 3 /60
arrival_rates = [arrival_rate_CAT1, arrival_rate_CAT2, arrival_rate_CAT3]

tot_doctors = 5
tot_resus_rooms = 2
tot_t_nurse = 1
tot_beds = 15
waiting_room_cap = 20
totals = [tot_doctors, tot_resus_rooms, tot_t_nurse, tot_beds, waiting_room_cap]

simulation_reps(arrival_rates, SIM_END, num_replications, totals,  show_full_output)