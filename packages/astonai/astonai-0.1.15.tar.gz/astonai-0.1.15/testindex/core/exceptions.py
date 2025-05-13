"""
Exception handling framework for the Test Intelligence Engine.

This module defines a hierarchy of custom exceptions used throughout the application.
Each exception type includes an error code and standardized message format to
provide consistent error reporting and handling.
"""
from typing import Any, Dict, Optional


class TestIntelligenceError(Exception):
    """Base exception class for all application-specific exceptions."""
    
    def __init__(
        self, 
        message: str,
        error_code: str = "E000",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new TestIntelligenceError.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (default: "E000")
            details: Additional details about the error (default: None)
        """
        self.error_code = error_code
        self.details = details or {}
        self.message = message
        super().__init__(f"[{error_code}] {message}")


class ConfigurationError(TestIntelligenceError):
    """Exception raised for configuration-related errors."""
    
    def __init__(
        self, 
        message: str,
        error_code: str = "E100",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new ConfigurationError.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (default: "E100")
            details: Additional details about the error (default: None)
        """
        super().__init__(message=message, error_code=error_code, details=details)


class StorageError(TestIntelligenceError):
    """Exception raised for storage-related errors."""
    
    def __init__(
        self, 
        message: str,
        error_code: str = "E200",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new StorageError.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (default: "E200")
            details: Additional details about the error (default: None)
        """
        super().__init__(message=message, error_code=error_code, details=details)


class CLIError(TestIntelligenceError):
    """Exception raised for CLI-related errors."""
    
    def __init__(
        self, 
        message: str,
        error_code: str = "E300",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new CLIError.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (default: "E300")
            details: Additional details about the error (default: None)
        """
        super().__init__(message=message, error_code=error_code, details=details)


class LoggingError(TestIntelligenceError):
    """Exception raised for logging-related errors."""
    
    def __init__(
        self, 
        message: str,
        error_code: str = "E400",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new LoggingError.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (default: "E400")
            details: Additional details about the error (default: None)
        """
        super().__init__(message=message, error_code=error_code, details=details)


class ValidationError(TestIntelligenceError):
    """Exception raised for data validation errors."""
    
    def __init__(
        self, 
        message: str,
        error_code: str = "E500",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new ValidationError.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (default: "E500")
            details: Additional details about the error (default: None)
        """
        super().__init__(message=message, error_code=error_code, details=details)
