from unittest import TestCase


class APITestCase(TestCase):

    def assertDictStructure(self, expect: dict, actual: dict, path: list = []) -> None:
        """
        Compare function to check if expected dict with types equals the actual dict. If a dict has a dict as field
        the function call it self recursive.

        :raise AssertionError: if actual type and expected types are not same
        :raise AssertionError: if keys in actual and expected are not same

        :param expect: dict with types
        :param actual: dict with values
        :param path: current path(list with keys)
        :return: None
        """
        self.assertEqual(expect.keys(), actual.keys(),
                         msg=f"Expected field keys are not same: {self.path_to_dict_path(path)}")
        for key in actual:
            if isinstance(expect[key], dict):
                self.assertIsInstance(actual[key], dict,
                                      msg=f"Expected field {self.path_to_dict_path(path+[key])} to be type dict, "
                                          f"got type {type(actual[key])} instead")
                self.assertDictStructure(expect[key], actual[key], path + [key])
            elif isinstance(expect[key], list):
                self.assertIsInstance(actual[key], list,
                                      msg=f"Expected field {self.path_to_dict_path(path+[key])} to be type list, "
                                          f"got type {type(actual[key])} instead")
                if isinstance(expect[key][0], dict):
                    for i, entry in enumerate(actual[key]):
                        self.assertDictStructure(expect[key][0], entry, path + [key, i])
                else:
                    for i, entry in enumerate(actual[key]):
                        self.assertIsInstance(entry, expect[key][0],
                                              msg=f"Expected field {self.path_to_dict_path(path+[key, i])} "
                                                  f"to be type {expect[key][0]}, got type {type(entry)} instead")
            else:
                self.assertIsInstance(actual[key], expect[key],
                                      msg=f"Expected field {self.path_to_dict_path(path+[key])} "
                                          f"to be type {expect[key]}, got type {type(actual[key])} instead")

    @staticmethod
    def path_to_dict_path(path: list) -> str:
        """
        This method returns the dict path to a field.

        path_to_dict_path(["layer1", "layer2, "key"])
        -> "['layer1']['layer2']['key']"

        :param path: list with keys(path)
        :return: dict path as str
        """
        return "".join([f"['{key}']" for key in path])
