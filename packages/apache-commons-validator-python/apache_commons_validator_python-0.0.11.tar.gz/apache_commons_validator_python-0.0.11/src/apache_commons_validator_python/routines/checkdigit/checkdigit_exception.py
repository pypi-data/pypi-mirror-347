""" 
Module Name: checkdigit_exception.py

Description: 
    This module provides a Python exception class translating the behavior of
    Apache Commons Validator’s `CheckDigitException.java` for errors during check
    digit calculation or validation. It captures an optional underlying cause.
    Original link at: 
        https://github.com/apache/commons-validator/blob/master/src/main/java/org/apache/commons/validator/routines/checkdigit/CheckDigitException.java    
         
Author: Juji Lau

License (Taken from apache.commons.validator.routines.checkdigit.CheckDigitException.java):
    Licensed to the Apache Software Foundation (ASF) under one or more
    contributor license agreements. See the NOTICE file distributed with
    this work for additional information regarding copyright ownership.
    The ASF licenses this file to You under the Apache License, Version 2.0
    (the "License"); you may not use this file except in compliance with
    the License. You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Changes:
    - Added self.__cause__ to allow propogation of Python's base Exceptions.
"""

class CheckDigitException(Exception):
    """Exception raised for errors in check digit calculation or validation.

    Attributes:
        value (str): The error message explaining the error.
        serializable (bool): Indicates if the object is serializable.
        clone (bool): Indicates if the object can be cloned.
    """

    # Attributes to manage serialization and cloning capabilities
    serializable = True   # class is serializable
    clone = False

    def __init__(self, msg:str = None, cause:Exception = None):
        """
        Initializes CheckDigitException.

        Args:
            msg (str, optional): The error message.
            cause (Exception, optional): The underlying cause of the error.
        """
        super().__init__(msg)
        self.value = msg  # Makes it compatible with Java-style `.value` access
        if isinstance(cause, BaseException):
            self.__cause__ = cause
