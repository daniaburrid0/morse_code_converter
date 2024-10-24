class ProgressTracker:
    """
    Monitors and records user progress in Morse code practice.

    Methods:
        record_progress(exercise: str, success: bool) -> None
            Records the result of a practice exercise.
        
        get_statistics() -> dict
            Retrieves progress statistics.
    """

    def record_progress(self, exercise: str, success: bool) -> None:
        """
        Records the result of a practice exercise.

        Parameters:
            exercise (str): The exercise attempted.
            success (bool): Whether the exercise was completed successfully.

        Example:
            >>> tracker = ProgressTracker()
            >>> tracker.record_progress('... --- ...', True)
        """
        pass

    def get_statistics(self) -> dict:
        """
        Retrieves progress statistics.

        Returns:
            dict: A dictionary containing progress statistics.

        Example:
            >>> tracker = ProgressTracker()
            >>> tracker.get_statistics()
            {'completed': 10, 'success_rate': 0.8}
        """
        pass
