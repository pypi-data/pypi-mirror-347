import inspect
import os
import abc
import time
import sys
import logging
import platform
import traceback
import re

from QuarchpyQCS.Drive_wrapper import DriveWrapper
from QuarchpyQCS.hostInformation import HostInformation
from QuarchpyQCS.driveTestCore import DiskStatusCheck, is_tool, get_module_from_choice, get_quarch_modules_qps, comms
from QuarchpyQCS.dtsComms import DTSCommms
from QuarchpyQCS.dtsGlobals import dtsGlobals
from QuarchpyQCS.Custom_test_variable import CustomVariable

from quarchpy.qps.qpsFuncs import isQpsRunning
from quarchpy.qis.qisFuncs import check_remote_qis
from quarchpy.device.scanDevices import scanDevices
import inspect

ABC = abc.ABCMeta('ABC', (object,), {})


def check_stop(func):
    def inner(*args, **kwargs):
        if dtsGlobals.continueTest:
            return func(*args, **kwargs)
        return
    return inner

# This could use a comment
class IdGenerator:
    def __init__(self, base_test_point):
        # Why not track number of tiers as len(unique_ID)?

        # Array of "tiers" for ID's
        self.unique_ID = [0]
        # what 'tier' we are one / changing
        self.tier_level = 0

        self.first_call = True

        self.test_ids = []
        # tier_levels : 0   1   2   3
        # tier_Values : 0 , 0 , 0 , 0
        self.base = base_test_point

        if self.base is None:
            self.base = print

    def reset(self):
        self.unique_ID = [0]
        self.tier_level = 0
        self.first_call = True

    @check_stop
    def up_tier(self, description=None, singular=False, add_to_current_tier=False):

        if add_to_current_tier:
            self.base(self.gen_next_id(), test_description=description)

        # Auto add another tier level if required
        if self.tier_level is (len(self.unique_ID) - 1):
            self.unique_ID.append(0)
        self.tier_level += 1

        if description and not add_to_current_tier:
            self.base(self.gen_next_id(), test_description=description)

        if not singular:
            if self.tier_level is (len(self.unique_ID) - 1):
                self.unique_ID.append(0)
            self.tier_level += 1

    @check_stop
    def down_tier(self, singular=False, description=None):
        # Cannot decrease more than 0'th tier
        if self.tier_level == 0:
            return
        self.tier_level -= 1

        if description:
            self.base(self.gen_next_id(), test_description=description)

        if not singular:
            self.tier_level -= 1

    @check_stop
    def return_current(self):
        strings = [str(tier_value) for tier_value in self.unique_ID]
        unique_id = ".".join(strings)

        return str(unique_id)

    @check_stop
    def return_parent_id(self):
        strings = [str(tier_value) for tier_value in self.unique_ID]
        unique_id = ".".join(strings)

        # Return itself if no parent
        if "." not in unique_id:
            return str(unique_id)

        # remove last tier value
        unique_id = unique_id[:unique_id.rfind(".")]

        return str(unique_id)

    @check_stop
    def gen_next_id(self):

        for i in range(len(self.unique_ID)):
            if i is self.tier_level:
                if self.first_call:
                    self.first_call = False
                    break
                self.unique_ID[self.tier_level] += 1

        # reset all additional tiers to 0
        while (len(self.unique_ID) - 1) > self.tier_level:
            # Remove last index
            self.unique_ID.pop()

        strings = [str(tier_value) for tier_value in self.unique_ID]
        unique_id = ".".join(strings)

        self.test_ids.append(unique_id)
        return str(unique_id)

    @check_stop
    def check_valid_test_id(self, range, unique_id):
        """
        This may add some noticable delay to the test points due to having to search through ID's

        To counter this we want to be able to return from the method as soon as possible

        """

        """
        Accepted formats to parse:

        1.1.1 = String
            Compare with ID. True if exact OR child of this ID (e.g. 1.1.1.1)

        1.2-1.3 = String
            Split the string at '-'
            True if unique id starts with EITHER of the 2 strings

        1.*.4 = String
            Check against Unique id for [1,*,4]
            True if matches regex 1.\d*.4(.?\d?)*    
            must be 1.?.4 with optional amount of .n.n.n where n is digit.     

        """

        if isinstance(range, str):
            if "-" in range:
                return self.check_range(range, unique_id)
            elif "*" in range:
                return self.check_sequence(range, unique_id)
            else:
                return self.check_equal(range, unique_id)

        if isinstance(range, list):
            for sequence in range:

                if "-" in sequence:
                    if self.check_range(sequence, unique_id):
                        return True

                if "*" in str(sequence):
                    if self.check_sequence(sequence, unique_id):
                        return True

                if self.check_equal(sequence, unique_id):
                    return True


        # Not of type list of str - must be false
        return False

    @check_stop
    def check_equal(self, item, unique_id):
        if unique_id == item:
            return True
        return False

    @check_stop
    def check_start_or_equal(self, item, unique_id):
        if self.check_equal(item, unique_id):
            return True
        if str(unique_id).startswith(item):
            return True
        return False

    @check_stop
    def check_sequence(self, range, unique_id):
        """
        1.*.1
        Anything that is of sequence 1.\d*.1

        but need to replace the * with \d*

        """
        reg = range

        if "**" in reg:
            # Don't allow multiple consecutive asterisk
            return False

        reg = str(reg).replace("*", "\d*")
        # Regex '\d*' means any number of digits.
        if re.match(reg, unique_id):
            if "." in reg:
                # only accepting an exact match, no children
                reg2 = reg.split(".")
                if len(reg2) == len(str(unique_id).split(".")):
                    return True
            else:
                return True
        return False

    @check_stop
    def check_range(self, range_values, unique_id):
        # this looks complex. Will require testing!
        IDs = range_values.split("-")
        """
        e.g. 1.1 - 1.3
        means:
        anything with 1.1 or 1.2 start.
        
        how to compare?

        [ 1 - 7 ] =? 6.2.3
        [ 2.3.5 - 7.8.9 ] =? 6.2.4
        
        if > smallest range && < biggest range = good.
            for each item inside we just keep doing this
            
        7 - 1 = 6. Valid.
        
        we need to make tehm all equal one another in terms of length of the list.
        
        """

        smallest = IDs[0]
        largest = IDs[1]
        biggest_list_length = 0

        if "." in smallest:
            smallest_list = IDs[0].split(".")
            biggest_list_length = len(smallest_list)
        if "." in largest:
            largest_list = IDs[1].split(".")
            if len(largest_list) > biggest_list_length:
                biggest_list_length = len(largest_list)
        if "." in unique_id:
            unique_id_list = unique_id.split(".")
            if len(unique_id_list) > biggest_list_length:
                biggest_list_length = len(unique_id_list)

        if biggest_list_length > 0 :
            smol_str = ""
            big_str = ""
            id_str = ""
            if len(str(smallest.replace(".", ""))) <= biggest_list_length:
                smol_str = smallest.replace(".", "")
                while (len(smol_str)) < biggest_list_length:
                    smol_str = smol_str + "0"
            if len(str(largest.replace(".", ""))) <= biggest_list_length:
                big_str = largest.replace(".", "")
                while (len(big_str)) < biggest_list_length:
                    big_str = big_str + "0"
            if len(str(unique_id.replace(".", ""))) <= biggest_list_length:
                id_str = unique_id.replace(".", "")
                while (len(id_str)) < biggest_list_length:
                    id_str = id_str + "0"

            smallest = smol_str
            largest = big_str
            unique_id = id_str

        if largest > unique_id >= smallest:
            return True

        return False


def _create_scan_dict(use_qps, ip_lookup, filter_module):
    """
    :return: A dictionary of arguments appropriate for module search function
    """
    if not use_qps:
        return {"ipAddressLookup": ip_lookup, "module_type_filter": filter_module}
    else:
        return {}


class BaseTest(ABC):
    def __init__(self):
        # pass base_test, so ID generator can add test points.
        self.test_id = IdGenerator(self.test_point)

        # Saving the last executed checkpoint's ID - for use to add extra checkpoint debug
        self.last_checkpoint_id = None

        # Iterator for check point ID's - Incremented on every check point
        self.check_point_id = 1

        # Pulling in functionality of other classes to be used throughout program
        self.comms = None                       # QCS communications
        self.my_host_info = HostInformation()   # Drive detection

        # Current test name
        self.test_name = ""
        # Current test QCS number
        self.test_number = ""

        # Iterative counter for # of test points - Set during 'seek' test mode - used for QCS test completion bar
        self.number_of_test_points = 0

        # Dictionart of items to report to QCS for report (e.g. drive name, module name, test name...)
        self.report = {}

        # Custom variables dictionary - Used for adding custom values to test values
        self.custom_variable_dict = {}
        # List of variables changes by user for test.
        self.user_vars = []

        # NOT FULLY IMPLEMENTED! - List of test points to 'skip'
        self.skipped_tests = []

        # List containing test any test errors - will be reported to user in GUI as a pop-up
        self.test_errors = []

        # (semi-depricated) Was an old feature to just show test points of test without running tests
        self.document_mode = False
        # Execution mode string checks if the test is to be run fully, or just quickly iterated test points.
        self.execution_mode = "run"

        # Current test point, statistic point and repeat for ongoing tests. Updated as needed.
        # Used to sort the QCS report and test comparisons
        self.test_group = ""
        self.test_sub_group = ""
        self.test_repeat = 1


        # ------------------------------------------
        # Generic custom values used for every test
        # ------------------------------------------

        self.cv_stop_on_first_fail = self.declare_custom_variable(custom_name="Stop on fail", type="bool",
                                                                  default_value="False", var_group="Generic",
                                                                  description="Stop test at first failure point",
                                                                  accepted_vals=["True", "False"])

        self.cv_custom_code = self.declare_custom_variable(custom_name="Custom Python Code", type="File",
                                                           default_value=None, var_group="CustomCode",
                                                           description="Custom code to run in test")

        self.cv_run_custom_code = self.declare_custom_variable(custom_name="Custom code start", type="choice",
                                                               default_value="after", var_group="CustomCode",
                                                               description="Run custom code before or after check points",
                                                               accepted_vals=["before", "after"])

        self.cv_custom_code_id = self.declare_custom_variable(custom_name="Custom code ID", type="str",
                                                              default_value="", var_group="CustomCode",
                                                              description="Checkpoint ID to run custom code on")



    def _set_documentation_mode(self, document_mode=False):
        if "seek" in str(document_mode):
            # Mode to seek number of test points
            self.execution_mode = "seek"
            self.number_of_test_points = 0
            self.document_mode = True
            return
        if document_mode:
            # Legacy
            self.execution_mode = "document"
            self.document_mode = True
            self.test_errors = []
        else:
            # Start the tests
            self.execution_mode = "run"
            self.document_mode = False

    def ask_for_user_vars(self):
        """
        Function to request user values for custom variables
        :return:
        """
        # _get_custom_variables will send user vars to client and return a dict of { var_name : var_value } pairs
        self.custom_variable_dict = self._get_custom_variables()

        # Not fully implemented - List of test id's to skip
        self.skipped_tests = self._list_test_to_skip()

        # go through each var returned from client and swap test's custom var values with ones returned from client
        self.__change_custom_vars()

    def __change_custom_vars(self):
        """
        Change the current custom variables in use for the test with that which was returned from the client

        """
        # If there's no changes, then there's nothing this function need do
        if not self.custom_variable_dict:
            return

        # Loop through each custom variable - It's a list of objects so should be mutable
        for variable in self.user_vars:
            # Check if variable name in return dictionary
            if variable.custom_name in self.custom_variable_dict.keys():
                # replace custom variable value with new value
                if self.custom_variable_dict[variable.custom_name]:
                    variable.custom_value = self.custom_variable_dict[variable.custom_name]
                    if variable.custom_value.isdigit():
                        variable.custom_value = int(variable.custom_value)
                if str(variable.type).lower() == "file":
                    dict_key = variable._name_of_file_path_key()
                    if dict_key in self.custom_variable_dict.keys():
                        variable.file_path = self.custom_variable_dict[dict_key]

                logging.debug(f"Swapping {variable.custom_name} value to {variable.custom_value}")


    def declare_custom_variable(self, default_value, custom_name, description="", var_purpose=None, accepted_vals=None,
                                numerical_max=None, type=None, var_group="Test"):
        """

        :param default_value: Default value of custom variable
        :param custom_name: Custom value is added by user in java GUI
        :param description: Short description of variable use in test
        :param var_purpose: > USED LIKE AN ENUM > Tells us if custom variable is user editable
        :param accepted_vals: List of accepted values for item ( Shown as dropdown in GUI )
        :param numerical_max: Allows a maximum value to be applied to variable (MINIMUM VALUE ALWAYS 0)
        :return:
        """

        new_var = CustomVariable(name=custom_name, description=description, default_value=default_value, type=type,
                                 var_purpose=var_purpose, accepted_vals=accepted_vals, numerical_max=numerical_max,
                                 var_group=var_group)

        # Add to user variables list
        if not var_purpose:
            self.user_vars.append(new_var)
        else:
            # If parameter passed for internal variables to be shown, show all variables
            # Note - Can't send an obj variable as it makes no sense
            if dtsGlobals.show_internal_variables and type != "obj":
                self.user_vars.append(new_var)

        # return a new custom variable instance
        return new_var

    def _list_test_to_skip(self):
        """
        Tests to skip included inside custom variables - NOT FULLY IMPLEMENTED

        Format:
        1-3 --> Skip all tests points beginning with 1,2 or 3
        1.3 --> Skip test point 1.3
        1.4,1.5 --> Skip test points 1.4 and 1.5

        :return: List of all ID's / tests to be skipped
        """
        if "skip_tests" in self.custom_variable_dict.keys():
            # return list of id's to skip
            return self._return_skipable_tests(self.custom_variable_dict["skip_tests"])
        else:
            return []  # Return an empty list

    def _return_skipable_tests(self, string_list):
        """
        Function to return the string of tests to skip as a list of test ID's

        :param string_list: String input of the test id's to skip
        :return: List of strings - containing full or beggining portion of test id's to skip
        """
        # split them at a comma
        string_divide = string_list.split(",")

        items_to_skip = []

        for item in string_divide:
            if "-" in item:
                # should only ever be in form '1-4'
                range_split = item.split("-")
                # Consider smaller form below. Also does range_split need to be forced to int?
                # This could probably also use a try/catch statement in case user enters an
                # incorrect range
                temp_val = []
                items_to_skip += range(int(range_split[0]), int(range_split[1]) + 1)
                for new_item in temp_val:
                    items_to_skip.append(str(new_item))

            else:
                # if item isn't a range, it's just a test point to skip > '4.7
                items_to_skip.append(str(item).strip())

        # converting everything to string
        for index, item in enumerate(items_to_skip):
            if isinstance(item, int):
                items_to_skip[index] = str(item)

        return items_to_skip

    def _skip_test(self, unique_id):
        """
        Not fully implemented!

        :param unique_id: ID to check against skipped tests
        :return: boolean - true if test point is to be skipped, else false
        """
        for item in self.skipped_tests:
            if str(unique_id[:1]) == str(item):
                return True
            else:
                if unique_id == item:
                    return True
        return False

    def start_test(self, document_mode=False):
        """
            Base function for starting a test.
            All tests passed from QCS are required to override this function

            Is overridden in every test
        """
        pass

    def check_prerequisites(self):
        """
            Base function for checking any import modules of a test
            All tests require LSPCI / WMIC for windows
            All tests require LSPCI / LSSCSI for linux
        """
        # if not on windows, check lspci and lsscsi are installed
        if os.name != 'nt':
            if not is_tool("lsscsi"):
                self.test_errors.append("Lsscsi not found on server machine, please install and restart server")
            if not is_tool("lspci"):
                self.test_errors.append("Lspci not found on server machine, please install and restart server")

    def _get_custom_variables(self):
        """
            Base function, once a test class is instantiated, this method is called
            All tests passed from QCS will call this in order to get dictionary of custom variables
        """

        return self.comms.sendMsgToGUIwithResponse(self.comms.create_request_variable(self.user_vars),
                                                   timeToWait=None)

    def gather_initial_report_values(self):
        """
        Function to clear last report variables and append some of the 'header' / test details for the new test

        """

        # Clear all the items from the previous test.
        self.report.clear()

        # add custom variables in test
        # self.report["custom_variables"] = self.custom_variable_dict
        self.report["custom_variables"] = self.user_vars

        # add hardware information
        self.report["cpu"] = platform.processor()
        self.report["operating_system"] = platform.system() + " " + platform.version()
        self.report["host_platform"] = platform.node()

    def seek_test_values(self):
        # Run through test, counting up all the test / check points
        try:
            self.start_test(document_mode="seek")
        except Exception as e:
            traceback.print_exc()
            self.test_errors.append("Error during seek of test : " + str(e))
        # send a message to say test consists of x amount of test points
        self.comms.sendMsgToGUI(self.comms.create_request_status(number_of_test_points=self.number_of_test_points))
        # gui will auto increment counter / progress with every log sent over

    def test_point(self, unique_id=None, function=None, function_args={}, function_description=None, debug=None,
                   warning=None, test_description=None, has_return=False, stop_timeout=False):

        """
        :param stop_timeout: Indicates whether function needs to stop QCS timeout
        :param test_description: Relays only a test description to QCS
        :param debug: Relays only debug information to QCS
        :param has_return: Whether to return item from function
        :param unique_id: test point ID
        :param function_description: describes what function to be executed is doing
        :param function: name of function to execute
        :param function_args: Arguments for function being executed

        :return: pass / fail
        """

        # Skipping tests, adding to tally - Used primarily in progress bar.
        if self.execution_mode == "seek":
            self.number_of_test_points += 1

            if has_return:
                self.number_of_test_points += 1
                return "Unused String"
            return None

        if not dtsGlobals.continueTest:
            return

        return_obj = ReturnObject()

        # checking whether to skip test
        if self._skip_test(unique_id):
            return False

        if function:
            # Return obj will contain any caught exceptions.
            return_obj = self._execute_test_function(function_description, function, function_args, has_return,
                                                     unique_id, stop_timeout)

            # TODO : Add any caught exception as 'error' log for QCS

        if debug:
            self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "Debug", debug,
                                                                  sys._getframe().f_code.co_name, uId=""))
        if warning:
            self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "warning", warning,
                                                                  sys._getframe().f_code.co_name, uId=""))

        if test_description:
            self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "testDescription",
                                                                  test_description, sys._getframe().f_code.co_name,
                                                                  uId=unique_id))

        # return object if there is one, else return True.
        if return_obj.return_item is None:
            return True

        return return_obj.return_item

    def check_point(self, unique_id, description, function, function_args, has_return=False):

        if self.execution_mode == "seek":
            self.number_of_test_points += 2
            return

        if not dtsGlobals.continueTest:
            return

        # checking whether to skip test
        if self._skip_test(unique_id):
            return

        self.last_checkpoint_id = unique_id

        if str(self.cv_run_custom_code.custom_value).strip() == "before":
            if self.cv_custom_code.custom_value:
                if self.test_id.check_valid_test_id(self.cv_custom_code_id.custom_value, unique_id):
                    self.execute_custom_code(self.cv_custom_code.custom_value)

            # self.cv_run_custom_code

            #self.cv_custom_code_id

        return_obj = ReturnObject()

        if not self.document_mode:
            return_obj.return_item = function(**function_args)
        else:
            return_obj.return_item = True

        if str(self.cv_run_custom_code.custom_value).strip() == "after":
            if self.cv_custom_code:
                if self.test_id.check_valid_test_id(self.cv_custom_code_id.custom_value, unique_id):
                    self.execute_custom_code(self.cv_custom_code.custom_value)

        self.comms.sendMsgToGUI(
            self.comms.create_request_log(
                time.time(), "testResult", description, sys._getframe().f_code.co_name,
                messageData={"Test Result ": str(return_obj.return_item)}, test_result=str(return_obj.return_item),
                uId=unique_id, group=self.test_group, sub_group=self.test_sub_group, check_point_id=self.check_point_id))
                # group=group, sub_group=sub_group,

        self.check_point_id += 1

        if bool(return_obj.return_item) is False:
            if str(self.cv_stop_on_first_fail.custom_value).lower() == "true":
                dtsGlobals.continueTest = False

        if has_return:
            return return_obj.return_item

    def check_point_add_info(self, parent_checkpoint_id, info_to_add):
        self.comms.sendMsgToGUI(
            self.comms.create_request_log(
                time.time(), "TESTRESULTINFO", str(info_to_add), sys._getframe().f_code.co_name,
                {"parent_checkpoint_id": parent_checkpoint_id}, uId=""))

    def statistics_point(self, unique_id, description, value, units, category):
        """
        Added 04/01/2023.
        Creating a statistics point function.
        Will be used as the default way of sending a stats point going forward
        # Added as the program needs to separate the statistics using addition data #

        :param unique_id: String - Standard unique id
        :param description: String - description of statistic
        :param group: String - Group to include it under (e.g. BlocksizeTest)
        :param sub_group: String - Sub-group of stats point (e.g. Blocksize4k)
        :param value: Int/String - Value of the statistic
        :param units: String - Units value (e.g. mW / uW / W)
        :param category: String - Catergory to group stats in each sub-group. (e.g. throughput, IOPS)
        :return:
        """

        if self.execution_mode == "seek":
            self.number_of_test_points += 1
            return

        if not dtsGlobals.continueTest:
            return

        # Sending the logs over in a consistent way so every test just needs to call the function, not this monster
        self.comms.sendMsgToGUI(
            self.comms.create_request_log(
                time.time(), "result_statistic", description, sys._getframe().f_code.co_name,
                uId=unique_id, group=self.test_group, sub_group=self.test_sub_group, category=category,
                messageData={"value": str(value), "units": units}))

    def _add_quarch_command(self, command, quarch_device, expected_response="OK", retry=True):
        result = quarch_device.sendCommand(command)

        if isinstance(expected_response, str):
            if result != expected_response:
                if retry:
                    return self._add_quarch_command(command, quarch_device, expected_response=expected_response,
                                                    retry=False)
                if "run" in str(command).lower():
                    expected_response = "FAIL: 0x41 -Failed to change state of action"
        if isinstance(expected_response, list):
            found = False
            for item in expected_response:
                if str(item).lower() in str(result).lower():
                    found = True
                    expected_response = result
                    break


        self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "quarchCommand",
                                                              "Quarch Command: " + command + " - Response: " +
                                                              result.replace("\r\n", "").strip(),
                                                              sys._getframe().f_code.co_name,
                                                              {"debugLevel": 1,
                                                               "textDetails": "Executing command on module"},
                                                              uId=""))
        # Verify that the command executed as expected
        if result != expected_response:

            self.comms.sendMsgToGUI(
                self.comms.create_request_log(time.time(), "error",
                                              f"Error executing module command : {command}",
                                              sys._getframe().f_code.co_name,
                                              {"debugLevel": 2, "response_type": str(type(result)),
                                               "response": result.replace("\r\n", "").strip(),
                                               "command": command}, uId=""))

            result = False

        return result

    def _execute_test_function(self, function_description, function, function_args, has_return, unique_id,
                               stop_timeout):

        return_value = ReturnObject()

        if function_description:
            self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "testDescription",
                                                                  str(function_description),
                                                                  sys._getframe().f_code.co_name,
                                                                  uId=unique_id))

        # Will need to check - if it has a return i may need said results
        if not self.document_mode:
            if stop_timeout:
                self.comms.send_stop_timeout()
            try:
                return_value.return_item = function(**function_args)
            except Exception as e:
                return_value.error = e
                print(traceback.format_exc())
                print(e)
                self.comms.create_request_log(time.time(), "error", "Error executing Function",
                                              sys._getframe().f_code.co_name,
                                              {"debugLevel": 2, "response_type": str(type(e)),
                                               "exception": str(e),
                                               "function": str(function)}, uId="")
                logging.warning("Exception caught during execution of function : " + str(function))
                return_value.return_item = None
            if stop_timeout:
                self.comms.send_start_timeout()

        if has_return:
            # All items that return dictionary as
            return_desc = None
            if self.document_mode:
                return_desc = "Document Mode Placeholder value"
            elif isinstance(return_value.return_item, dict):
                if "key_return" in return_value.return_item.keys():
                    return_desc = return_value.return_item["key_return"]
                    return_value.return_item = return_value.return_item["value_return"]
                # else:
                #     return_desc = str(return_value.return_item)

            if return_desc is not None:
                self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "TestReturn",
                                                                      "Return value of Function : " + return_desc,
                                                                      sys._getframe().f_code.co_name,
                                                                      uId=unique_id))

        return return_value

    def test_check_link_speed(self, drive, link_speed=None):
        """
        Checks if the device has expected link speed

        :param drive: (DriveWrapper)            Current drive object to be compared.
        :param link_speed: (Optional - String)  If another link speed is expected, compare it against this
        :return: Boolean - true if consistent else false
        """
        if isinstance(drive, DriveWrapper):
            if str(drive.system_cmd).lower() != "lspci":
                self.test_point(debug="QCS does not currently support Link Speed detection on {0} found drives"
                                .format(drive.system_cmd))
                return True

            if str(link_speed).strip() == "auto":
                # replace with the drive's original link speed
                link_speed = drive.link_speed

            link_speed_current = self.my_host_info.return_wrapped_drive_link(drive)
            self.test_point(debug="Drive link speed currently : {0}".format(link_speed_current))

            if self.my_host_info.verify_wrapped_drive_link(drive, link_speed):
                return True

        return False

    def test_check_lane_width(self, drive, lane_width=None):
        """
        Checks if the device has expected lane width

        :param drive: (DriveWrapper)            Current drive object to be compared.
        :param lane_width: (Optional - String)  If another lane width is expected, compare it against this
        :return: Boolean - true if consistent else false
        """

        if isinstance(drive, DriveWrapper):
            if str(drive.system_cmd).lower() != "lspci":
                self.test_point(debug="QCS does not currently support Lane Width detection on {0} found drives"
                                .format(drive.system_cmd))
                return True

            if str(lane_width).strip() == "auto":
                # replace with the drive's original link speed
                lane_width = drive.lane_width

            width = self.my_host_info.return_wrapped_drive_width(drive)
            self.test_point(debug="Drive Lane width currently : {0}".format(width))

            if self.my_host_info.verify_wrapped_drive_width(drive, lane_width):
                return True

        return False

    def test_wait_for_enumeration(self, enumeration, drive, ontime=0, offtime=0, report_enum_time=True):

        if enumeration:
            enum_time = self.checkDriveState(drive, True, ontime)
        else:
            enum_time = self.checkDriveState(drive, False, offtime)

        if report_enum_time:
            if isinstance(enum_time, float):
                description = "Device {0} after {1}s (+/- 1s)".format("discovered" if enumeration else "removed", str(enum_time))
                self.test_point(self.test_id.gen_next_id(), debug=description)
            else:
                self.test_point(self.test_id.gen_next_id(), debug="No change to drive state detected in allocated {0}s"
                                .format(str(ontime) if enumeration else str(offtime)))

        return enum_time

    def request_qps(self):

        if self.document_mode:
            return True

        self.test_id.up_tier(singular=True)

        self.test_point(self.test_id.gen_next_id(), test_description="Checking quarchpy installed on client PC.")

        self.comms.sendMsgToGUIwithResponse(self.comms.create_request_function("check_program", "quarchpy"))

        while dtsGlobals.quarchpy_installed is None and dtsGlobals.continueTest is True:
            self.comms.getReturnPacket()
            time.sleep(0.25)

        if not dtsGlobals.quarchpy_installed:
            self.test_point(self.test_id.gen_next_id(), test_description="Could not find quarchpy on client pc!")
        else:
            self.test_point(self.test_id.gen_next_id(), test_description="Quarchpy discovered on client pc.")

        if not check_remote_qis(host=dtsGlobals.GUI_TCP_IP, timeout=0):
            self.test_point(self.test_id.gen_next_id(), test_description="Attempting to automatically launch QPS from quarchpy...")

            self.comms.sendMsgToGUI(self.comms.create_request_function("start_program", "qis"))
            if not check_remote_qis(host=dtsGlobals.GUI_TCP_IP, timeout=25):
                self.comms.send_stop_test(reason="Failed to start QIS instance. Please start this manually on Client machine")
                self.test_id.down_tier(singular=True)
                return False

        self.test_point(self.test_id.gen_next_id(), test_description="Connected to QIS")

        if not isQpsRunning(host=dtsGlobals.GUI_TCP_IP, timeout=0):
            self.test_point(self.test_id.gen_next_id(), test_description="Attempting to automatically launch QPS from quarchpy...")
            self.comms.sendMsgToGUI(self.comms.create_request_function("start_program", "qps"))
            if not isQpsRunning(host=dtsGlobals.GUI_TCP_IP, timeout=25):
                self.comms.send_stop_test(reason="Failed to start QPS instance. Please start this manually on Client machine.")
                self.test_id.down_tier(singular=True)
                return False

        self.test_point(self.test_id.gen_next_id(), test_description="Connected to QPS")
        self.test_id.down_tier(singular=True)
        return True

    def _reset_device(self, module, power_down=False):
        self.test_id.up_tier(singular=True, description="Resetting Quarch module to default state")

        if power_down:

            self.test_point(self.test_id.gen_next_id(), function=self._add_quarch_command,
                            function_args={"command": "run:power down", "quarch_device": self.cv_quarchname.custom_value})

            self.test_delay(3, "Powered down module for full drive reset.")

        self.test_point(self.test_id.gen_next_id(), function=self._add_quarch_command,
                        function_args={"command": "conf def state", "quarch_device": module})

        self.test_delay(3, "Waiting for Quarch module to fully reset.")

        self.test_id.down_tier(singular=True)

    '''
    Callback: Run when a test invokes UTILS_VISUALSLEEP.  This allows user feedback when a delay function is required. Specified
    delay time is in seconds
    '''

    def checkDriveState(self, driveObject, deviceState, waitTime):
        # DeviceState 0 : Wait for device to be cleared from list
        # DeviceState 1 : Wait for device to appear in list

        start = time.time()
        loop = 0
        end = time.time() - start

        poll_message = self.comms.create_request_poll("drive_state")

        while end < float(waitTime):
            end = time.time() - start
            # Should be the only time that we don't want to check lane speeds
            if DiskStatusCheck(driveObject, deviceState, check_lanes=False, poll=True):
                # printText("device new state after " + str(end) + " seconds" )
                return end

            loop += 1
            if loop == 3:
                # QCS deadman timeout is default 20 seconds
                # System command timeouts are 5 seconds..
                # This covers a single 'problematic' system command.
                loop = 0
                self.comms.sendMsgToGUI(poll_message)

        return None

    def select_drive(self, drive_type=None):
        """
        :param drive_type: Accepted values : "sas", "pcie", "all"
        :return:
        """
        temp_id = self.test_id.unique_ID

        self.test_id.up_tier("User drive selection", add_to_current_tier=True, singular=True)

        logging.debug("Attempting to find available drives using specified method : " + str(drive_type))

        drive_list = self.test_point(self.test_id.gen_next_id(), function_description="Finding available drives",
                                     function=self.my_host_info.return_wrapped_drives, has_return=True,
                                     function_args={'drive_type': drive_type})

        if not drive_list:
            logging.debug("No drives were discovered")
        else:
            logging.debug("Sending drives discovered on system to Java client")

        user_choice = self.test_point(self.test_id.gen_next_id(), has_return=True,
                                      function_description="Asking user to select drive",
                                      function=self.select_item,
                                      function_args={"description": "",
                                                     "window_mode": "drive",
                                                     "drive_dictionary": drive_list})

        if "rescan" in str(user_choice):
            logging.debug("User requested rescan")
            self.test_id.unique_ID = temp_id
            self.test_id.down_tier(singular=True)
            return self.select_drive(drive_type)
        if "abort" in str(user_choice):
            logging.debug("User requested abourt")
            return None

        logging.debug("Response returned from client: " + str(user_choice))

        drive = self.test_point(self.test_id.gen_next_id(), has_return=True,
                                function_description="Finding chosen drive from drive list",
                                function=self.my_host_info.get_wrapped_drive_from_choice,
                                function_args={"selection": user_choice})

        if drive:
            logging.debug("Found drive from list of drives on system")

        if isinstance(drive, DriveWrapper):
            self.report["drive"] = drive.description
            self.report["drive_type"] = str(drive.drive_type)
            self.report["drive_path"] = drive.drive_path
            self.report["link_speed"] = "Unsupported for " + str(drive.system_cmd)
            self.report["lane_width"] = "Unsupported for " + str(drive.system_cmd)

            self.comms.sendMsgToGUI(
                self.comms.create_request_log(time.time(), "testReturn",
                                              "User Select drive : {0} , {1}".format(drive.identifier_str,
                                                                                     drive.description),
                                              sys._getframe().f_code.co_name,
                                              uId=self.test_id.gen_next_id()))

            if str(drive.system_cmd).lower() in ["wmic", "lsscsi", "smartctl"]:
                self.test_point(
                    warning="QCS does not currently support link speed / lane width operation with drives found via {0}"
                .format(drive.system_cmd))
                self.test_point(unique_id=self.test_id.gen_next_id(),
                                test_description="Initial Link Speed = Not Supported for " + str(drive.system_cmd))
                self.test_point(unique_id=self.test_id.gen_next_id(),
                                test_description="Initial Lane Width = Not Supported for " + str(drive.system_cmd))

            elif str(drive.system_cmd).lower() in "lspci":
                self.test_point(self.test_id.gen_next_id(), has_return=True,
                                function_description="Gathering initial drive link speed and lane width from LSPCI",
                                function=self.my_host_info.store_initial_drive_stats,
                                function_args={"drive": drive})

                # Reporting link speed / lane width to user and adding to the report dict - ( used if report requsted )
                self.report["link_speed"] = drive.link_speed
                self.test_point(unique_id=self.test_id.gen_next_id(),
                                test_description="Initial Link Speed = " + str(drive.link_speed))
                self.report["lane_width"] = drive.lane_width
                self.test_point(unique_id=self.test_id.gen_next_id(),
                                test_description="Initial Lane Width = " + str(drive.lane_width))

            else:
                self.test_point(warning="QCS does not currently support unknown system commands")

        if self.document_mode:
            drive = DriveWrapper()
        else:
            # Sending over drive report variables after module selection
            self._send_report_vars()

        self.test_id.down_tier(singular=True)

        return drive


    def _send_report_vars(self):
        """
        Added in 1.12 QCS release -
        Required for test comparison, added here so all tests report their drive/module information
            - If the test crashes, this will still be reported and files can still be made

        """
        self.comms.sendMsgToGUI(
            comms.create_request_gui(title="report generation", description="Test Report",
                                     window_type="SelectionGrid", window_mode="report",
                                     report_dict=self.report))

    def select_quarch_module(self, use_qps=False, ip_lookup=None, filter_module=None, power_on=True):
        """
        :param use_qps: whether to use python or qps
        :param ip_lookup: IP to send discovery packet to - utilized by running test only.
        :param filter_module:
        :return:
        """
        temp_id = self.test_id.unique_ID

        function = get_quarch_modules_qps if use_qps else scanDevices

        function_args_dict = _create_scan_dict(use_qps, ip_lookup, filter_module)

        software_type = "qps" if use_qps else "py"

        self.test_id.up_tier("User module selection", add_to_current_tier=True, singular=True)

        module_list = self.test_point(self.test_id.gen_next_id(), has_return=True,
                                      function_description="Retrieving all found quarch modules",
                                      function=function, function_args=function_args_dict)

        user_choice = self.test_point(self.test_id.gen_next_id(), has_return=True,
                                      function_description="User selection – Quarch module to use",
                                      function=self.select_item,
                                      function_args={"description": "",
                                                     "window_mode": software_type,
                                                     "module_dictionary": module_list})
        # check for rescan / rescan with ip lookup
        if "abort" in str(user_choice):
            return None
        if "rescan" in str(user_choice):
            if "==" in str(user_choice):
                ip_lookup = user_choice[user_choice.index("==") + 2:]
            self.test_id.unique_ID = temp_id
            self.test_id.down_tier(singular=True)
            return self.select_quarch_module(use_qps=use_qps, ip_lookup=ip_lookup, filter_module=filter_module)

        return_val = self.test_point(self.test_id.gen_next_id(), has_return=True, function=get_module_from_choice,
                                     function_description="Creating module connection from user choice",
                                     function_args={"self": self, "connection": user_choice, "is_qps": use_qps,
                                                    "report_dict": self.report, "return_val": True})

        if self.document_mode:
            return_val = "placeholder"
        else:
            self.comms.sendMsgToGUI(
                self.comms.create_request_log(time.time(), "testReturn", "User Select module : {0}".format(user_choice),
                                              sys._getframe().f_code.co_name, uId=self.test_id.gen_next_id()))


        if use_qps:
            self.test_point(self.test_id.gen_next_id(), has_return=True, function=self._check_output_mode,
                            function_description="Checking and setting QPS module output mode, if required",
                            function_args={"my_qps_device": return_val})

        # Check power up here
        if power_on:
            self.test_point(self.test_id.gen_next_id(), has_return=True, function=self._power_on_module,
                            function_description="Checking power state of module",
                            function_args={"myQuarchDevice": return_val, "is_qps": use_qps})



        if isinstance(return_val, bool):
            logging.error("Returned quarch device as boolean ")
            return None

        # Sending over module report variables after module selection
        if not self.document_mode:
            self._send_report_vars()

        self.test_id.down_tier(singular=True)

        return return_val

    def _power_on_module(self, myQuarchDevice, is_qps=True):
        # hd will reply with off if no power
        expected_on_response = "plugged"

        if is_qps:
            expected_on_response = "on"

        self.test_id.up_tier(singular=True)

        power_status = self.test_point(function=self._add_quarch_command, has_return=True,
                                     function_args={"command": "run pow?", "quarch_device": myQuarchDevice,
                                                    "expected_response": ["ON", "OFF", "PLUGGED", "PULLED"]})
        # power_status = myQuarchDevice.sendCommand("run pow?")
        self.test_point(self.test_id.gen_next_id(), test_description="Power status : " + str(power_status))

        if expected_on_response not in str(power_status).lower():
            self.test_point(self.test_id.gen_next_id(), test_description="Powering on Quarch module")

            self.test_point(function=self._add_quarch_command,
                            function_args={"command": "run:pow up", "quarch_device": myQuarchDevice})

            self.test_point(self.test_id.gen_next_id(), test_description="Waiting 5 seconds for drive power on")
            time.sleep(5)

        self.test_id.down_tier(singular=True)

    def _check_output_mode(self, my_qps_device):

        # QCS V1.09 - Left this in.
        # Need to check idn and return if the qtl number contains pam name
        output_mode_value = my_qps_device.sendCommand("conf:out:mode?")
        if not "QTL1999" in str(output_mode_value).lower():
            return

        output_mode_value = self.test_point(function=self._add_quarch_command, has_return=True,
                                            function_args={"command": "conf:out:mode?",
                                                           "quarch_device": my_qps_device,
                                                           "expected_response": ["disabled", "3V3", "5V"]})
        if "DISABLED" in output_mode_value:
            self.test_point(function=self._add_quarch_command, has_return=True,
                            function_args={"command": "conf:out:mode 3v3", "quarch_device": my_qps_device})
            output_mode_value = "3v3"

        my_qps_device.output_mode = output_mode_value

    def _check_can_stream(self, my_qps_device):
        if self.document_mode:
            return True

        can_stream = True

        self.test_id.up_tier(singular=True, description="Checking module can stream")

        can_stream = my_qps_device.sendCommand("rec?")
        if "fail" in str(can_stream).lower():
            can_stream = False

        self.test_id.down_tier(singular=True)

        return can_stream


    def select_item(self, description, window_mode, drive_dictionary=None, module_dictionary=None):

        dtsGlobals.choiceResponse = None

        """
        :param description: Description of selection
        :param window_mode: qps / py / drive
        :param module_dictionary:
        :param drive_dictionary:
        :return: Selected item from the user
        """

        if window_mode == "qps":
            formatted_qps_modules_dict = {}
            for quarch_module in module_dictionary:
                if "no devices found" in str(quarch_module).lower():
                    # Assign it to empty dict
                    break
                if "rest" in str(quarch_module).lower():
                    continue
                connection_without_interface = quarch_module[quarch_module.rindex(":") + 1:]
                formatted_qps_modules_dict[quarch_module.replace("::", ":")] = connection_without_interface
            module_dictionary = formatted_qps_modules_dict

        self.comms.sendMsgToGUIwithResponse\
            (self.comms.create_request_gui(title="user selection", description=description, window_type="SelectionGrid",
                                           window_mode=window_mode, dict_of_drives=drive_dictionary,
                                           dict_of_modules=module_dictionary), timeToWait=None)

        while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
            self.comms.getReturnPacket()
            time.sleep(0.25)

        choice = str(dtsGlobals.choiceResponse)
        selection = choice.split("::")
        selection = selection[1]
        if window_mode == "qps":
            selection = selection.replace(":", "::")

        return selection

    def execute_custom_code(self, custom_code):
        loc = {}
        try:
            exec(custom_code, globals(), loc)
            return_workaround = loc['main']
            return return_workaround()
        except Exception as e:
            logging.warning("Caught exception with custom user code")

    def test_delay(self, delay=5, description=None):
        desc = "" if not description else " : reason : " + description

        # Adding a quick way to add test delays
        self.test_point(self.test_id.gen_next_id(), function_description=f"{delay} second test delay {desc}",
                        function=self._delay, function_args={'delay': delay})

    def set_test_group(self, test_group):
        self.test_group = test_group

    def set_test_sub_group(self, sub_group):
        self.test_sub_group = sub_group

    def set_test_repeat(self, repeat):
        self.test_repeat = repeat

    def _delay(self, delay):
        # Generic QCS test delay function
        time.sleep(delay)


class ReturnObject:
    def __init__(self):
        self.return_item = None
        self.error = None
        self.additional_info = None
        self.user_choice = None

class stats_obj:
    def __init__(self, value, units, name, category):
        self.value = value
        self.units = units
        self.name = name
        self.category = category