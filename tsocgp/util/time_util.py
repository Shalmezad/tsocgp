
import re
class TimeUtil(object):
    ONE_SECOND = 1
    ONE_MINUTE = 60 * ONE_SECOND
    ONE_HOUR = 60 * ONE_MINUTE

    @staticmethod
    def ddi_duration_to_seconds(duration:str):
        """
        Coverts a DDI duration (ex: PT3M) to seconds (ex: 180)
        https://www.ddialliance.org/Specification/DDI-Lifecycle/3.1/XMLSchema/FieldLevelDocumentation/reusable_xsd/simpleTypes/DateTypeCodeType.html
        """
        # So, now the fun part:
        duration = duration.upper()
        time = 0
        pieces = re.findall(r'[^A-Z]*[A-Z]+', duration)
        for piece in pieces:
            if piece == "PT":
                continue
            #import pdb; pdb.set_trace()
            i_piece_str = re.sub(r"\D", "", piece)
            i_piece = int(i_piece_str)
            if "M" in piece:
                time += 60 * i_piece
            elif "S" in piece:
                time += i_piece
        return time

    
    @staticmethod
    def seconds_since_midnight_to_hms(duration:int):
        """
        Converts seconds since 00:00:00 to HH:MM:SS
        """
        s = duration % 60
        m = (duration / 60) % 60
        h = (duration / 60 / 60) % 24
        return "%02d:%02d:%02d" % (h, m, s)

    
    @staticmethod
    def hms_to_seconds_since_midnight(hms:str):
        """
        Converts  HH:MM:SS to seconds since 00:00:00
        """
        pieces_s = hms.split(":")
        pieces_i = list(map(int, pieces_s))
        h = pieces_i[0]
        m = pieces_i[1]
        s = pieces_i[2]
        return s + m * 60 + h * 60 * 60
