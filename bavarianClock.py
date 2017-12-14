#!/usr/bin/python3
import argparse
from time import localtime, strftime

class BavarianClock():
    # constants
    hourNames = ["_", # a dummy to let the hours start at 1
        "Oans",
        "Zwoa",
        "Drei",
        "Viere",
        "Fümwe",
        "Sechse",
        "Siemme",
        "Ochte",
        "Neine",
        "Zehne",
        "Eife",
        "Zweife"
    ]
    relMarkers = {
        "last": [
            "vddl noch",
            "hoib noch",
            "dreivddl noch"
        ],

        # "next": [
        #     "¼",
        #     "½",
        #     "¾"
        # ],
        "next": [
            "vddl",
            "hoibe",
            "dreivddl"
        ],

        "nextTo": [
            "dreivddl vor",
            "hoibe vor",
            "vddl vor"
        ]
    }
    intro = "Ezzad iss grod"
    AM    = "in da Friah"
    MM    = "am Mittog"
    PM    = "aufd Nocht"

    dateFormat        = None
    addIntro          = None
    addDayTag         = None
    quarterStyle      = None
    halfStyle         = None
    threeQuarterStyle = None

    # quarterStyle, halfStyle and threeQuarterStyle want one of 'last', 'next' or 'nextTo'
    def __init__(self, dateFormat, addIntro, addDayTag, quarterStyle, halfStyle, threeQuarterStyle):
        # settings
        self.dateFormat        = dateFormat
        self.addIntro          = addIntro
        self.addDayTag         = addDayTag
        self.quarterStyle      = quarterStyle
        self.halfStyle         = halfStyle
        self.threeQuarterStyle = threeQuarterStyle

    def getHourName(self, h):
        while h < 1:  h += 12
        while h > 12: h -= 12
        return self.hourNames[h]

    def getTime(self):
        # get the current time
        now = localtime()
        # convert it to the 1..12 range
        h = ((now.tm_hour-1) % 12) + 1
        # convert the minutes to fractions, i.e. 1min 30sec becomes 1.5 mins
        mm = now.tm_min + now.tm_sec/60.0
        # do the same for hours
        hh = now.tm_hour + mm/60

        # assemble the result
        ret = ""
        # add the intro
        if self.addIntro:
            ret += self.intro + " "

        # create the actual time
        if mm <= 7.5:
            # close to the current hour, no relative string at all
            ret += self.getHourName(h)
        elif mm <= 22.5:
            # minutes around 15
            if self.quarterStyle == "last":
                ret += self.relMarkers["last"][0] + " " + self.getHourName(h)
            elif self.quarterStyle == "next":
                ret += self.relMarkers["next"][0] + " " + self.getHourName(h+1)
            else: # nextTo
                ret += self.relMarkers["nextTo"][0] + " " + self.getHourName(h+1)
        elif mm <= 37.5:
            # minutes around 30
            if self.halfStyle == "last":
                ret += self.relMarkers["last"][1] + " " + self.getHourName(h)
            elif self.halfStyle == "next":
                ret += self.relMarkers["next"][1] + " " + self.getHourName(h+1)
            else: # nextTo
                ret += self.relMarkers["nextTo"][1] + " " + self.getHourName(h+1)
        elif mm <= 52.5:
            # minutes around 45
            if self.threeQuarterStyle == "last":
                ret += self.relMarkers["last"][2] + " " + self.getHourName(h)
            elif self.threeQuarterStyle == "next":
                ret += self.relMarkers["next"][2] + " " + self.getHourName(h+1)
            else: # nextTo
                ret += self.relMarkers["nextTo"][2] + " " + self.getHourName(h+1)
        else: # mm > 52.5
            # close to next hour -> use that
            ret += self.getHourName(h+1)

        # add AM/MM/PM tags
        if self.addDayTag:
            if hh <= 0.5:
                # [00:00..00:30]
                ret += " " + self.PM
            elif hh < 10.5:
                # [00:30..10:30[
                ret += " " + self.AM
            elif hh < 15.5:
                # [10:30..15:30[
                ret += " " + self.MM
            else:
                # [15:30..00:00[
                ret += " " + self.PM

        # append the date (without a space in between, to give the user full control)
        if self.dateFormat:
            ret += strftime(self.dateFormat, now)

        return ret



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A very precise bavarian clock.\n"
        "Relative markers can be set individually for all times around 15, 30 and 45 minute.\n"
        "The choices are (for the example of 18:15): 'last' means relate it to the last full hour, i.e. 'quarter past 6'. 'next' means relate it to the next hour (first style), i.e. 'quarter 7'. 'netxtTo' means relate it to the next hour (second style), i.e. 'three quarters to 7'.")
    parser.add_argument("-d", "--dateFormat",                                                            help="Apppend the date to the time using this strftime format string")
    parser.add_argument("-i", "--addIntro",          action="store_true",                                help="Add a short intro prefix")
    parser.add_argument("-p", "--addDayTag",         action="store_true",                                help="Add an AM/MM/PM suffix (MM means middle of the day)")
    parser.add_argument("-1", "--quarterStyle",      choices=["last", "next", "nextTo"], default="last", help="Relative marker type for the minutes around 15.")
    parser.add_argument("-2", "--halfStyle",         choices=["last", "next", "nextTo"], default="next", help="Relative marker type for the minutes around 30.")
    parser.add_argument("-3", "--threeQuarterStyle", choices=["last", "next", "nextTo"], default="next", help="Relative marker type for the minutes around 45.")
    args = parser.parse_args()

    b = BavarianClock(dateFormat=args.dateFormat, addIntro=args.addIntro, addDayTag=args.addDayTag, quarterStyle=args.quarterStyle, halfStyle=args.halfStyle, threeQuarterStyle=args.threeQuarterStyle)
    print(b.getTime())
