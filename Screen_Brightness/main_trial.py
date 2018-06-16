import os
import time

from Settings import Settings
from BrightnessManager import BrightnessManager

class PowerSaver:
    def __init__(self, args=None):
        self.setup(args)

    def setup(self, args=None):
        '''Set up arguments to be used, and initialize Battery and Brightness mangager.'''

        arguments = {
            "verbose": False,
            "manual": False,
            "fade": .25,
            "time": 2,
            "profile": None
        }

        if args is not None:
            for arg in args.keys():
                if arg in arguments:
                    arguments[arg] = args[arg]

        self.arguments = arguments

        self.level = None

        self.brightness_manager = BrightnessManager()
        
        self.brightness = self.brightness_manager.get_brightness()


        #self.charging = self.battery.is_charging()
        #self.percent = self.battery.percent()

        self.level = None
        self.min_percent = None
        self.max_percent = None

        if self.arguments["profile"] is None:
            cur_dir = os.path.abspath(os.path.dirname(__file__))
            #if self.arguments["verbose"]:
            #    print("Default settings loaded", flush=True)
            self.settings = Settings(os.path.join(cur_dir, "settings.json"))

        else:
            self.settings = Settings(arguments["profile"])

    def poll(self):
        '''Poll the battery and brightness. If the battery level defined in settings
        has changed, update the screen brightness.'''

        poll_time = self.arguments["time"]

        while True:
            time.sleep(poll_time)
            update = False
	    
            brightness = self.brightness_manager.get_brightness()
            print (brightness)

            brightness_level = 50
            self.brightness_manager.set_brightness(brightness_level)
            if brightness_level <= 50:
                self.brightness_manager.set_brightness(75)

            else:
                self.brightness_manager.set_brightness(25)
    
            brightness = self.brightness_manager.get_brightness()
            print ("New brightness",brightness)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbose",
        help="Display messages in the terminal each time the battery is polled.\n"
        "Default: Off",
        action="store_true"
    )

    parser.add_argument(
        "-m",
        "--manual",
        help="Keep the program open if the brightness is manually changed.\n"
        "Default: Off",
        action="store_true"
    )

    parser.add_argument(
        "-f",
        "--fade",
        help="The speed to fade the brightness in or out.\n"
        "Higher is slower. Default: .25",
        type=float,
        default=.25
    )

    parser.add_argument(
        "-t",
        "--time",
        help="The time to sleep between each poll on the battery. (in seconds)\n"
        "Default: 2",
        type=float,
        default=2
        )

    parser.add_argument(
        "-p",
        "--profile",
        help="The json file to use for battery levels and percentages.",
        type=str
    )

    args = parser.parse_args()

    arguments = {
        "verbose": args.verbose,
        "manual": args.manual,
        "fade": args.fade,
        "time": args.time,
        "profile": None if not args.profile else args.profile,
    }

    powersaver = PowerSaver(arguments)
    powersaver.poll()
