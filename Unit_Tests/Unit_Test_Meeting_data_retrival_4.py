import unittest
import json

# Loading meeting meta data from form_data.json
def load_audio_transcripts_data():
    meeting_file = open("form_data.json")
    meeting_data = json.load(meeting_file)
    
    host_ip = meeting_data[0]["main"]["ipaddress"]
    host_email = meeting_data[0]["main"]["email"]
    host_port_address = meeting_data[0]["main"]["port"]
    host_name = meeting_data[0]["main"]["name"]
    
    #print(host_ip, host_email, host_port_address, host_name)
    
    parasite_ip = meeting_data[1]["others"][0]["ipaddress"]
    parasite_email = meeting_data[1]["others"][0]["email"]
    parasite_port_address = meeting_data[1]["others"][0]["port"]
    parasite_name = meeting_data[1]["others"][0]["name"]
    
    print(host_ip, host_email, host_port_address, host_name)
    
    print(parasite_ip, parasite_email, parasite_port_address, parasite_name)
    
    #return host_ip, host_email, host_port_address, host_name, parasite_ip, parasite_email, parasite_port_address, parasite_name
    return parasite_port_address

# validating receiver port address
class TestAdd(unittest.TestCase):
    def test_add(self):
        actual = load_audio_transcripts_data()
        expected = "9998"
        self.assertEqual(actual, expected)