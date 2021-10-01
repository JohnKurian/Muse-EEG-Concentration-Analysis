from muselsl import record
import uuid
username = "avi"
activity = "lostinmigration"

filename = "./" + username + "_" + activity + "_ " + str(uuid.uuid4()) + ".csv"


record(47, data_source="EEG", dejitter=False, filename= filename)