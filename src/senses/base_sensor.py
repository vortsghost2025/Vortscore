class BaseSensor:
    """
    Abstract base class for all FSI sensory inputs.
    Defines the interface for dynamic data ingestion.
    """
    def capture(self):
        raise NotImplementedError("Sensory capture method must be implemented.")
