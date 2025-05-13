# coding=utf-8
from typing import Any

import subprocess

TyClsName = Any
TyModName = Any
TyPacName = Any
TyPacModName = Any
TyFncName = Any


class Srv:

    @staticmethod
    def get_start_time(service_name):
        """
        show module name of function
        """
        try:
            # Run the systemctl command to get service details
            result = subprocess.run(
                ["systemctl", "show", service_name, "--property=ExecMainStartTimestamp"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            # Extract the start timestamp from the output
            output = result.stdout.strip()
            if output.startswith("ExecMainStartTimestamp="):
                start_time = output.split("=", 1)[1]
                return start_time
            else:
                msg = "Start time not available or service not running."
                raise Exception(msg)
        except subprocess.CalledProcessError as e:
            msg = f"Error retrieving service information: {e}"
            raise Exception(msg)
