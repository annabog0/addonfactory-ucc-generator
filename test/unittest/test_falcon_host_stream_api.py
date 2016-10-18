import datetime
import json
import os
import sys
import time
import unittest

folder_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(folder_path, '../../package/bin/splunk_ta_crowdstrike'))


class TestFalconHostStreamAPI(unittest.TestCase):
    events = [
        """{"event":{"Success":true,"UTCTimestamp":_TIMESTAMP_,"OperationName":"twoFactorAuthenticate","UserId":"_USER_EMAIL_","ServiceName":"CrowdStrikeAuthentication","UserIp":"_IP_ADDRESS_"},"metadata":{"customerIDString":"7614db1615b91c3caf1809991bc061a1","eventType":"AuthActivityAuditEvent","offset":_OFFSET_}}""",
        """{"event":{"UserName":"_USERNAME_","ProcessId":103152535310,"ProcessStartTime":_TIMESTAMP_,"Severity":2,"ParentProcessId":103133469329,"CommandLine":"_FILE_PATH_","FilePath":"_FILE_PATH_","ComputerName":"_HOSTNAME_","DetectName":"KnownMalware","FileName":"_FILE_PATH_","ScanResults":[{"Engine":"K7AntiVirus","Detected":true,"Version":"9.220.19189","ResultName":"Unwanted-Program(004bc56d1)"},{"Engine":"AegisLab","Detected":true,"Version":"4.2","ResultName":"Hktl.Netcat.Gen!c"}],"SeverityName":"Low","MD5String":"5dcf26e3fbce71902b0cd7c72c60545b","SHA1String":"970bbe298c8ec673fe2257ad6363d29942171fd1","FalconHostLink":"https://falcon.crowdstrike.com/detects/8935647444343480192","MachineDomain":"_HOSTNAME_","SensorId":"1f841c21db914ce15ea81fa7a184f6b9","SHA256String":"e8fbec25db4f9d95b5e8f41cca51a4b32be8674a4dea7a45b6f7aeb22dbc38db","DetectDescription":"Afilesurpassedanantivirusdetectionthresholdaspotentialadware","ProcessEndTime":0},"metadata":{"customerIDString":"7604dbe615b94c3caf280999ebc06aa1","eventType":"DetectionSummaryEvent","offset":_OFFSET_}}""",
        """{"event":{"Success":true,"UTCTimestamp":_TIMESTAMP_,"AuditKeyValues":[{"Key":"detects","ValueString":"1378213310953669400"},{"Key":"new_state","ValueString":"true_positive"}],"OperationName":"UpdateDetectState","UserId":"_USER_EMAIL_","ServiceName":"Detects","UserIp":"_IP_ADDRESS_"},"metadata":{"customerIDString":"7604dbe615b94c3caf280999ebc06aa1","eventType":"UserActivityAuditEvent","offset":_OFFSET_}}""",
        """{"event":{"ProcessId":"25917476803","ProcessStartTime":_TIMESTAMP_,"FilePath":"_FILE_PATH_","AgentIdString":"f2c76aa30f40454064d4ecbdaecfd2ca","ParentProcessId":"25826055931","ComputerName":"_HOSTNAME_","MD5String":"2f0eaaf91fc7a5c70d1f4be9b18a1cf5","FileName":"_FILE_PATH_","DeviceId":"f2c76aa30f40454064d4ecbdaecfd2ca","CommandLine":"_FILE_PATH_"},"metadata":{"customerIDString":"5ddb0407bef249c19c7a975f17979a1f","eventType":"CustomerIOCEvent","offset":_OFFSET_}}""",
        """{"event":{"SensorCount":"4,FalconStreamingAPIReference","MD5String":"","FileName":"_FILE_PATH_","AlertTime":_TIMESTAMP_,"Signer":"","Sensors":[{"AgentIdString":"4ed403275e38aef276f2f479a21e5ccb","Filename":"_FILE_PATH_","HostnameField":"Unavailable-at-this-time","LastWriteTime":1464973200},{"AgentIdString":"7248482c6f59cb3f4b3ba8d9dd653a04","Filename":"_FILE_PATH_","HostnameField":"Unavailable-at-this-time","LastWriteTime":1464973200},{"AgentIdString":"80e436a2e6231733079eb6f8d860410e","Filename":"_FILE_PATH_","HostnameField":"Unavailable-at-this-time","LastWriteTime":1464973200},{"AgentIdString":"892e9ea45b73bb4794c346924cafa808","Filename":"_FILE_PATH_","HostnameField":"Unavailable-at-this-time","LastWriteTime":1464973200}],"ExecutionType":"PeWritten","SHA256String":"ccdc215f8f6d3d9877ba31290269bc38610453aad595dc60b48a2266d5428eb4"},"metadata":{"customerIDString":"e498338f24d64189a72f86b879a80401","eventType":"HashSpreadingEvent","offset":_OFFSET_}}"""
    ]

    def test_falcon_convert_raw_event_to_event(self):
        from falcon_host_stream_api import _convert_raw_event_to_event
        t_length = len('2016-09-26T14:11:37')
        unix_time = time.time()
        iso_time = datetime.datetime.utcfromtimestamp(int(unix_time)).isoformat()[:t_length]
        offset = 10000
        for event in self.events:
            event = event.replace('_TIMESTAMP_', str(unix_time))
            event = event.replace('_OFFSET_', str(offset))
            stream_event = _convert_raw_event_to_event(json.loads(event), event, 'test-source')
            self.assertEquals(event, stream_event.data)
            self.assertEquals(iso_time, stream_event.time[:t_length])
            self.assertEquals('test-source', stream_event.source)

if __name__ == "__main__":
    unittest.main()